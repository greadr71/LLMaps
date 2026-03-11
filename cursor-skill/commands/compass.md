---
description: Compass main workflow for turning user data into a runnable LLMaps build_map.py
handoffs:
  - llmaps.compass-survey
  - llmaps.compass-refine
---

# /llmaps.compass

Use this command when the user wants to create an interactive map from data.

## Workflow

Follow this strict 4-phase workflow.

### 1) Survey

1. Read the provided data file (GeoJSON, CSV, or Parquet).
2. Produce a short structured survey:
- Geometry type(s)
- Feature count
- Field list with inferred types
- Numeric ranges and null rates
- Categorical unique counts
- Bounding box
3. If no file is provided, ask for file path or switch to manual intent intake.

Reference:
- `compass/decision-tree.md` (Root and Geometry Routing)
- `compass/question-bank.md` (Data Discovery group)

If the user wants only analysis and no map generation, hand off to `/llmaps.compass-survey`.

### 2) Intent

1. Ask only relevant questions from `compass/question-bank.md`.
2. Prefer 3 to 5 focused questions, not the entire bank.
3. Decide:
- Geometry branch
- Recipe family
- Components
- Style choices (tiles, locale, compression)

Reference:
- `compass/decision-tree.md` (POINTS, POLYGONS, COMPONENTS, STYLE)
- `compass/question-bank.md` (Visualization Intent, Layer Config, Components, Style)

### 3) Generate

1. Select exactly one base recipe from `compass/recipes/`.
2. Fill placeholders with concrete values from survey and user answers.
3. Generate runnable `build_map.py` using LLMaps API from `llmaps/LLM_CONTEXT.md`.
4. Ensure map output is saved to `map.html`.

Recipe references:
- `compass/recipes/points-basic.md`
- `compass/recipes/points-sized.md`
- `compass/recipes/hexagons.md`
- `compass/recipes/choropleth.md`
- `compass/recipes/categorical.md`
- `compass/recipes/comparison.md`
- `compass/recipes/storytelling.md`
- `compass/recipes/search-sidebar.md`

### 4) Refine

1. Offer one-step refinement options after generation:
- Colors/palette
- Popup vs sidebar details
- Search configuration
- Basemap changes
- Locale/compression tuning
2. Apply requested edits directly to `build_map.py`.

If the user already has `build_map.py` and requests iterative edits, hand off to `/llmaps.compass-refine`.

## Output Contract

Always provide:

1. Survey summary.
2. Chosen recipe and why.
3. Generated `build_map.py`.
4. Short run instruction (`python build_map.py`).

## Guardrails

- Do not invent new LLMaps APIs.
- Keep all generated content in English.
- Keep Compass knowledge base agent-agnostic by referencing `compass/*` instead of duplicating its logic.
