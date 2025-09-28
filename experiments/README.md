# Experiments Configs

This folder holds small, versioned “run recipes” for `vf-eval`.

Status
- Not yet functional as commands. These JSON files are documentation/placeholders for reproducible runs and future UI integration. For now, run `vf-eval` directly (or `make smoke`).

Intent
- Make evaluations reproducible without remembering flags.
- Act as inputs to a future local hub UI (pick config → launch run).

Suggested JSON schema
{
  "environment": "vb-wordle-proxy",
  "model": "gpt-4o-mini",
  "num_examples": 10,
  "rollouts_per_example": 1,
  "max_concurrent": 32,
  "args": { "use_think": true },
  "api_key_var": "OPENAI_API_KEY",
  "api_base_url": "https://api.openai.com/v1",
  "max_tokens": 512,
  "temperature": 0.7,
  "sampling_args": { },
  "notes": "Baseline sanity run"
}

CLI mapping (vf-eval flags)
- environment → positional `env`
- model → `-m, --model`
- num_examples → `-n, --num-examples`
- rollouts_per_example → `-r, --rollouts-per-example`
- max_concurrent → `-c, --max-concurrent`
- args (env args JSON) → `-a, --env-args`
- api_key_var → `-k, --api-key-var`
- api_base_url → `-b, --api-base-url`
- max_tokens → `-t, --max-tokens` (or via sampling_args)
- temperature → `-T, --temperature` (or via sampling_args)
- sampling_args (JSON) → `-S, --sampling-args` (overrides -t/-T)
- endpoints_path → `-e, --endpoints-path` (optional)
- env_dir_path → `-p, --env-dir-path` (optional)
- save dataset → `-s, --save-dataset` (always pass when you want Hub Evals)

Example command from a config
uv run vf-eval vb-wordle-proxy \
  -m gpt-4o-mini -n 10 -r 1 -c 32 \
  -a '{"use_think": true}' -k OPENAI_API_KEY \
  -b https://api.openai.com/v1 -t 512 -T 0.7 -s

Naming
- `<env>/<purpose>.json` (e.g., `vb-wordle-proxy/smoke.json`).

Next step
- Add a `make run-config CONFIG=experiments/<path>.json` target to parse JSON and call `vf-eval` with the matching flags.
