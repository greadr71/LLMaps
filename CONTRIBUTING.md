# Contributing to LLMaps

Thank you for considering contributing to LLMaps.

## Development setup

1. Clone the repository and create a virtual environment (or use conda).
2. Install in editable mode with optional dependencies:

   ```bash
   pip install -e ".[all]"
   ```

3. Run tests (when available):

   ```bash
   pytest tests/
   ```

## Code style

- Follow PEP 8.
- Use type hints for public API (constructors, method signatures).
- Prefer dataclasses for configuration objects (Map, layers, sources, components).
- Keep the public API stable and documented in `llmaps/LLM_CONTEXT.md` (and thus `get_llm_context()`) and `docs/api/`.

## Documentation

- **llmaps/LLM_CONTEXT.md** — Compact reference for LLMs; keep in sync with the public API (signatures, scenarios, JS utilities).
- **docs/api/** — Update the relevant file (map.md, layers.md, sources.md, components.md) when changing parameters or behaviour.
- **docs/recipes/** — Add or update recipes when introducing new patterns (e.g. new layer type, new mode).

## Pull requests

- Describe the change and why it is needed.
- Ensure existing tests pass and add tests for new behaviour where appropriate.
- Update documentation (LLM_CONTEXT.md, docs/api, or recipes) if the public API or usage changes.

## Scope

LLMaps is a **library** for generating interactive web maps from Python. It is not a full GIS platform or a web application framework. Contributions that keep the API simple, predictable, and LLM-friendly are especially welcome.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
