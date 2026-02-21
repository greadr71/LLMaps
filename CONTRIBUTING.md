# Contributing to LLMaps

Thank you for considering contributing to LLMaps.

## Development setup

1. Clone the repository and create a virtual environment (or use conda).
2. Install in editable mode:

   ```bash
   pip install -e .
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

## Documentation checklist

For any public API change, update the documentation. Below is a complete list of files and dependency matrix.

### Documentation files

| File | Purpose |
|------|---------|
| `llmaps/LLM_CONTEXT.md` | Compact reference for LLMs (`get_llm_context()`). **Most important** — update for ANY API change |
| `docs/api/map.md` | Map class API (constructor, methods) |
| `docs/api/layers.md` | Layer API (CircleLayer, FillLayer, H3Layer, VectorTileLayer) |
| `docs/api/sources.md` | Source API (FileSource, ApiSource, VectorTileSource) |
| `docs/api/components.md` | Component API (Legend, Popup, Sidebar, FeatureSearch, Search, Controls, BasemapSwitcher) |
| `docs/recipes/*.md` | Recipes: heatmap, embedded-map, comparison, feature-state-highlighting |
| `README.md` | Main page — tables of layers, components, tile providers |
| `examples/README.md` | Examples overview |
| Docstrings in `*.py` | Class and method documentation in source code |

**Note:** `CHANGELOG.md` is updated only on new releases, not on every commit.

### Matrix: what to update

| Change type | Must update |
|------------|-------------|
| Map parameter | `map.md`, `LLM_CONTEXT.md`, docstring in `map.py` |
| Map method | `map.md`, `LLM_CONTEXT.md`, docstring in `map.py` |
| New/changed layer | `layers.md`, `LLM_CONTEXT.md`, docstring, `layers/__init__.py` |
| New/changed source | `sources.md`, `LLM_CONTEXT.md`, docstring, `sources/__init__.py` |
| New/changed component | `components.md`, `LLM_CONTEXT.md`, docstring, `components/__init__.py` |
| Expression helper | `LLM_CONTEXT.md`, docstring in `expressions.py`, `feature-state-highlighting.md` |
| Tile provider | `map.md`, `LLM_CONTEXT.md`, `tiles.py` |
| JS API (frontend) | `LLM_CONTEXT.md`, `sources.md`, `feature-state-highlighting.md` |
| Embedded/compression | `embedded-map.md`, `map.md`, `LLM_CONTEXT.md` |
| Breaking change | All of the above + BREAKING mark |

### Quick pre-commit checklist

- [ ] Docstrings updated in modified classes/methods
- [ ] `LLM_CONTEXT.md` reflects the change (constructors, scenarios, JS API)
- [ ] Corresponding file in `docs/api/` updated
- [ ] `docs/recipes/` updated if pattern affected
- [ ] Examples in `examples/` work with new API

## Pull requests

- Describe the change and why it is needed.
- Ensure existing tests pass and add tests for new behaviour where appropriate.
- Update documentation (LLM_CONTEXT.md, docs/api, or recipes) if the public API or usage changes.

## Scope

LLMaps is a **library** for generating interactive web maps from Python. It is not a full GIS platform or a web application framework. Contributions that keep the API simple, predictable, and LLM-friendly are especially welcome.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
