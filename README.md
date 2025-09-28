# Primerl Experiments — Hub of RL Environments

This repo is a small hub for installing and evaluating Prime Intellect/Verifiers environments. Use environment modules as the unit of modularity; prefer the official CLI for evaluation and artifacts.

## Quickstart
- Install deps: `uv sync`
- Copy `.env.example` → `.env` and set `OPENAI_API_KEY`
- Smoke test + save: `make smoke` (defaults to `SMOKE_ENV=vb-wordle-proxy`, 1 example). Artifacts are written under the environment’s own `outputs/evals/` folder (e.g., `environments/<env>/outputs/evals/...`).

## Local Proxy Environment
We include a thin proxy env `vb-wordle-proxy` that delegates to the canonical `wordle` environment.

Common commands:
- Smoke + save: `make smoke` (defaults to `SMOKE_ENV=vb-wordle-proxy`, 1 example). Artifacts are written under the env’s `outputs/evals/`.
- Push to Hub (PRIVATE): `make push-private ENV_ID=vb-wordle-proxy`
- Push to Hub (PUBLIC): `make push-public ENV_ID=vb-wordle-proxy`
- Pull upstream env sources: `make pull ENV_SLUG=will/wordle` (downloads into `environments/`)

Experiments configs
- The files in `experiments/` are currently reference-only (not wired to a command). We’ll add a `make run-config CONFIG=...` in a later step to execute them.

Notes:
- The proxy simply calls `verifiers.load_environment("wordle", **kwargs)`. It has no custom rubric; it mirrors upstream behavior.
- For private testing on the Hub, push the env and open it in the web UI to inspect the metadata, versions, and install instructions.

## Make Targets
- `install` — `uv sync`
- `smoke` — run a 1‑example `vf-eval` with `-s` to produce a dataset that appears on the Hub after the next push
- `push-private` — build/push `ENV_ID` from `environments/<id>` with private visibility
- `push-public` — same as above, public visibility
- `pull` — pull `ENV_SLUG` sources into `environments/` (owner/name[@version])

See `AGENTS.md` for style and operating rules (uv usage, artifact locations, and environment module contract). For reproducible run recipes, see `experiments/README.md`.

## Optional: Custom Runner
For ablations or extra logging, you can run the programmatic runner:

```
uv run python main.py <env> -m <model> -n 1 -r 1 -c 8 -t 256 -T 0.7 -a '{"use_think": true}'
```

Notes:
- Writes a dataset under `environments/<env>/outputs/evals/<env>--<model>/<timestamp>/`.
- Results from the custom runner do not automatically show up on the Hub; use `make smoke` + `make push-private` for Hub Evals.
