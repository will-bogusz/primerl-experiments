Local environment modules live here. Each module should be a small Python package with:

- `pyproject.toml` (name, version, description, dependencies)
- a module exporting `load_environment(**kwargs)`
- optional README with usage notes

Scaffold with the Prime CLI or Verifiers template, then install locally in editable mode to iterate.

