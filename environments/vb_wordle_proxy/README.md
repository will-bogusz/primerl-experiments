# vb-wordle-proxy

Proxy environment that delegates to the canonical `wordle` env via Verifiers. It exposes the same interface and metrics as upstream; useful for testing Hub publishing and orchestration patterns.

## Overview
- Environment ID: `vb-wordle-proxy`
- Type: multi-turn game (delegated)
- Loader: returns `verifiers.load_environment("wordle", **kwargs)`

## Quickstart
Run a tiny evaluation (requires `OPENAI_API_KEY` in `.env`):

```bash
uv run vf-eval vb-wordle-proxy -m gpt-4o-mini -n 1 -r 1 -s -k OPENAI_API_KEY
```

Wordle-specific knobs
- Forward upstream args with `-a` JSON:
  - `num_train_examples` (default 2000)
  - `num_eval_examples` (default 20)
  - `use_think` (default true) — when false, the parser expects guess-only (no `<think>`).

Examples
```bash
# Guess-with-thinking (default)
uv run vf-eval vb-wordle-proxy -m gpt-4o-mini -n 1 -r 1 -s -k OPENAI_API_KEY -a '{"use_think": true}'

# Guess-only mode
uv run vf-eval vb-wordle-proxy -m gpt-4o-mini -n 1 -r 1 -s -k OPENAI_API_KEY -a '{"use_think": false}'
```

Metrics
- Saved datasets include `reward` and per-component metrics: `check_answer_reward_func`, `partial_credit_reward_func`, `count_turns_reward_func`, `format_reward_func`.

## Push to Hub
Publish privately to inspect the web experience:

```bash
make push-private ENV_ID=vb-wordle-proxy
```

Switch to public if desired:

```bash
make push-public ENV_ID=vb-wordle-proxy
```

## Notes
- This package does not bundle `wordle` as a dependency on the Hub; it assumes the upstream env is available in the runtime. Locally, ensure the `wordle` package is installed when evaluating.
- Since behavior is proxied, use it primarily to validate Hub metadata, versioning, and install flows.
