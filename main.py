import os
import json
import argparse
from datetime import datetime

from dotenv import load_dotenv
from verifiers import load_environment
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Programmatic eval runner (optional).")
    parser.add_argument("env", help="Environment module name (e.g., vb-wordle-proxy, wordle)")
    parser.add_argument("-m", "--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("-n", "--num-examples", type=int, default=int(os.getenv("NUM_EXAMPLES", 1)))
    parser.add_argument(
        "-r",
        "--rollouts-per-example",
        type=int,
        default=int(os.getenv("ROLLOUTS_PER_EXAMPLE", 1)),
    )
    parser.add_argument("-c", "--max-concurrent", type=int, default=int(os.getenv("MAX_CONCURRENT", 32)))
    parser.add_argument("-a", "--env-args", default="{}", help="JSON for load_environment kwargs")
    parser.add_argument("-S", "--sampling-args", default=None, help="JSON for sampling args")
    parser.add_argument(
        "-t",
        "--max-tokens",
        type=int,
        default=int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None,
    )
    parser.add_argument(
        "-T",
        "--temperature",
        type=float,
        default=float(os.getenv("TEMPERATURE")) if os.getenv("TEMPERATURE") else None,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Load environment (forward any env-args JSON)
    try:
        env_kwargs = json.loads(args.env_args) if args.env_args else {}
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid --env-args JSON: {e}")

    env = load_environment(args.env, **env_kwargs)

    # Build sampling args by merging flags and provided JSON
    sampling = {}
    if args.sampling_args:
        try:
            sampling = json.loads(args.sampling_args)
        except json.JSONDecodeError as e:
            raise SystemExit(f"Invalid --sampling-args JSON: {e}")
    if args.max_tokens is not None:
        sampling["max_tokens"] = args.max_tokens
    if args.temperature is not None:
        sampling["temperature"] = args.temperature

    # Create OpenAI client (reads OPENAI_API_KEY)
    client = OpenAI()

    print(f"Running {args.env} with model={args.model}, n={args.num_examples}, r={args.rollouts_per_example}")

    results = env.evaluate(
        client=client,
        model=args.model,
        sampling_args=sampling or None,
        num_examples=args.num_examples,
        rollouts_per_example=args.rollouts_per_example,
        max_concurrent=args.max_concurrent,
    )

    # Save dataset next to the environment (or in environments/_external if not local)
    env_dir_name = args.env.replace("/", "_").replace("-", "_")
    if os.path.isdir(os.path.join("environments", env_dir_name)):
        base_env_dir = os.path.join("environments", env_dir_name)
    else:
        base_env_dir = os.path.join("environments", "_external", env_dir_name)

    run_dir = os.path.join(
        base_env_dir,
        "outputs",
        "evals",
        f"{args.env}--{args.model}",
        datetime.utcnow().strftime("%Y%m%d-%H%M%S"),
    )
    ensure_dir(run_dir)

    # Use Verifiers' dataset maker for schema compatibility
    ds = env.make_dataset(results)
    out_json = os.path.join(run_dir, "data.json")
    try:
        ds.to_json(out_json)
    except Exception:
        # Fallback: dump raw results if datasets export fails
        with open(out_json, "w") as f:
            json.dump(results, f, indent=2, default=str)

    with open(os.path.join(run_dir, "meta.json"), "w") as f:
        json.dump(
            {
                "env": args.env,
                "model": args.model,
                "num_examples": args.num_examples,
                "rollouts_per_example": args.rollouts_per_example,
                "max_concurrent": args.max_concurrent,
                "env_args": env_kwargs,
                "sampling_args": sampling,
            },
            f,
            indent=2,
        )

    print(f"Saved dataset to {run_dir}")


if __name__ == "__main__":
    main()
