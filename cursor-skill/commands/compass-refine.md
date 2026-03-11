---
description: Refine an existing LLMaps build_map.py with targeted Compass-guided improvements
---

# /llmaps.compass-refine

Use this command when the user already has a `build_map.py` and wants targeted improvements.

## Inputs

- Existing `build_map.py` path
- Requested changes (for example: palette, components, tile provider, interaction)

## Procedure

1. Read and summarize current map configuration:
- Source type and file path
- Layer type and style expressions
- Components in use
- Map settings (`tiles`, `locale`, `embedded`, `use_compression`)
2. Map current state to Compass branches from `compass/decision-tree.md`.
3. Suggest focused improvements in priority order:
- Visual clarity
- Interaction quality
- Performance and file size
- Accessibility/readability
4. Apply only requested changes unless user asks for broader refactor.
5. Return updated code and a brief change log.

## Typical Refinements

- Change color ramp or category colors.
- Add or remove `Popup`, `Sidebar`, `FeatureSearch`, `Legend`, `Controls`.
- Switch basemap (`osm`, `carto-light`, `carto-dark`, `yandex`, `2gis`).
- Tune H3 resolution/aggregation.
- Enable/disable `use_compression`.

## Output Contract

Always provide:

1. `Current Configuration` summary.
2. `Applied Changes` list.
3. Updated `build_map.py`.
4. Short verification instruction (`python build_map.py`).

## References

- `compass/decision-tree.md`
- `compass/question-bank.md`
- `compass/recipes/`
- `llmaps/LLM_CONTEXT.md`
