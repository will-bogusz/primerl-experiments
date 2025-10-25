# AI Agent Primer: Hub of RL Environments

This repo is a hub for creating, installing, and evaluating RL “environment modules” aligned with Prime Intellect and the Verifiers spec. Treat environment packages as the single unit of modularity and interoperability. Prefer the official CLI for evaluation and artifact saving; keep any custom runner minimal and schema‑compatible.

## **Guiding Principles**
- Use environment modules (installable Python packages exposing `load_environment(**kwargs)`) for everything: local experiments and Hub‑installed envs look the same.
- Run via `uv` for reproducibility. Use `uv run` for all commands.
- Prefer official tooling (`vf-eval`, `vf-tui`, and the Prime CLI for init/publish). Keep outputs in a standard dataset schema.
- Keep the repo organized so new envs can be added, evaluated, and optionally published without bespoke glue.

## **Repository Layout**
- `environments/` — local, editable environment modules. Each module is a tiny Python package with its own `pyproject.toml`, README, and a module exporting `load_environment(**kwargs)`.
- `experiments/` — lightweight run configs (JSON/TOML) describing `vf-eval` runs: model, `num_examples`, `rollouts`, sampling args, and any environment args. These are reference-only for now; they are not executed by a command yet.
- Artifacts live under each environment module’s `outputs/evals/` directory by default (e.g., `environments/<env>/outputs/evals/...`) when using `vf-eval -s`. Prefer that layout to keep runs co-located with the env.
- `main.py` — optional programmatic runner for ablations or extra logging; must write artifacts in the same dataset schema as `vf-eval -s`.

Current repo note: some folders may not exist yet; treat this file as the contract for how we organize future additions.

## **Official vs. Custom**
- Official (default): use `vf-eval` for standardized metrics, consistent saving (`-s`), and easy browsing via `vf-tui`. Use this for baselines, regressions, and anything you’ll share.
- Custom (optional): use `main.py` only when you need extra logs or bespoke probes.
  - Example: `uv run python main.py <env> -m <model> -n 1 -r 1 -c 8 -t 256 -T 0.7 -a '{"use_think": true}'`
  - It writes `environments/<env>/outputs/evals/<env>--<model>/<timestamp>/`.
  - Custom outputs don’t auto-appear on the Hub; prefer `vf-eval -s` + push for Hub Evals.

## **Starting A New Experiment**
1. Scaffold an environment module in `environments/<env-name>/` using the Prime CLI or Verifiers template.
2. Implement `load_environment(**kwargs)` returning a Verifiers environment (e.g., `MultiTurnEnv`/`ToolEnv`) plus a `Rubric` for scoring.
3. Install locally in editable mode and run a small `vf-eval` sanity check.
4. Save artifacts with `-s` (they will be written under the environment’s `outputs/evals/`). Optionally publish the environment via the Prime CLI when ready.

## **Environment Module Contract**
- Packaging: each env is a proper Python package with `pyproject.toml` (name, version, short description, dependencies) and a README.
- Entry point: `load_environment(**kwargs)` accepts your exposed knobs (e.g., `use_think`, dataset size, tools) and returns a Verifiers environment.
- Protocol and parsing: single‑turn or multi‑turn, tool usage as needed; parsers must enforce the expected output shape.
- Rubric: compute rewards and enforce anti‑cheat; include clear labels for primary/secondary metrics.
- Dataset shape: follow Verifiers conventions (core columns like `prompt`/`question`, optional `answer`/`info`/`task`). Keep outputs compatible with dataset emitters and `vf-tui`.

## **Artifacts & Outputs**
- Use `vf-eval -s` to save standardized artifacts; they are written under the evaluated environment’s `outputs/evals/` directory and appear on the Hub after the next push.
- If running programmatically (e.g., `main.py`), note that custom outputs do not automatically show on the Hub. Emit JSON/JSONL matching the Verifiers dataset schema and choose a non-conflicting output path.
- Keep small text summaries optional; the dataset files are the source of truth.

## **uv Workflow**
- Install deps: `uv sync`
- Add deps: `uv add <package>` (and `--dev` for dev tooling)
- Run evals: `uv run vf-eval <environment-name> -m <model> -n <N> -r <R> -s`
- Run custom: `uv run python main.py`

### Saved Results → Hub Evals
- To have results appear under the environment’s Evals tab on the next push: (1) run an eval with `-s` to save a dataset, then (2) push the env. Saved files will live under that env’s `outputs/evals/` folder.
- Make target: `make smoke` runs a 1‑example saved eval (defaults to `vb-wordle-proxy`).

Always run commands with `uv run` to ensure the correct virtual environment.

## **Configuration**
- `.env` (gitignored) holds secrets and optional defaults.
  - Minimal keys: `OPENAI_API_KEY` (required).
  - Optional defaults: `OPENAI_MODEL`, `NUM_EXAMPLES`, `ROLLOUTS_PER_EXAMPLE`.
    - Used by `make smoke` as overrides (model, -n, -r) and by the optional custom runner (`main.py`) as defaults.
- `.env.example` documents these keys; do not store secrets in JSON configs.

## **Baselines**
- For smoke/baseline comparisons we often use `will/wordle` or the local `vb-wordle-proxy` wrapper.
- Use `make smoke` for the quickest saved run that will appear on the Hub after the next push.
- Optionally keep reproducible configs in `experiments/<env>/*.json` (see `experiments/README.md`).

## **Housekeeping & Conventions**
- Use `uv` everywhere; do not call `python` directly in docs or scripts.
- Keep `verifiers` and any inference SDKs declared in `pyproject.toml`.
- Never commit `.env`. Commit `.env.example` with placeholders.
- Prefer JSON/JSONL for artifacts; name files with model, N, date/time where helpful.
- Keep module names readable and scoped (e.g., `vf-<short-task>` if you want a prefix).
- Make targets in use: `install`, `smoke`, `push-private`, `push-public`, `pull`.

### Make Targets (Standardized)
- `install` — sync dependencies via uv
- `smoke` — 1‑example saved eval (`-s`) to seed the Hub Evals tab after a push
- `push-private` / `push-public` — publish env to the Hub; requires `ENV_ID` (e.g., `vb-wordle-proxy`)
- `pull` — pull upstream env sources; requires `ENV_SLUG` (e.g., `will/wordle`)

Targets with IDs enforce variables explicitly; only `smoke` has a default env.

## **Roadmap**
See `docs/ROADMAP.md` (local, gitignored) for the detailed feature roadmap and milestones.

## **Agent Operating Rules (For Future Sessions)**
- Favor official CLI flows for evals and artifact creation; only fall back to custom runs when necessary.
- Save evaluation outputs under each environment’s `outputs/evals/` and keep them schema‑compatible.
- When adding a new experiment, prefer scaffolding an environment module rather than extending ad‑hoc scripts.
- Use concise preambles before running commands and keep plans short and check‑pointed.

This file is the source of truth for style and workflow in this repo. Keep it current as we add environments and refine our evaluation practices.
