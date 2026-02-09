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
- Keep the public API stable and documented in `API_GUIDE.md` and `docs/api/`.

## Documentation

- **API_GUIDE.md** — Keep the index in sync with the public API; update Keywords, Related, Alternatives when adding or changing components.
- **docs/api/** — Update the relevant file (map.md, layers.md, sources.md, components.md) when changing parameters or behaviour.
- **docs/recipes/** — Add or update recipes when introducing new patterns (e.g. new layer type, new mode).

## Pull requests

- Describe the change and why it is needed.
- Ensure existing tests pass and add tests for new behaviour where appropriate.
- Update documentation (API_GUIDE, docs/api, or recipes) if the public API or usage changes.

## Scope

LLMaps is a **library** for generating interactive web maps from Python. It is not a full GIS platform or a web application framework. Contributions that keep the API simple, predictable, and LLM-friendly are especially welcome.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
