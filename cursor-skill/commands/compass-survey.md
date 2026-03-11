---
description: Standalone Compass data survey for map planning
---

# /llmaps.compass-survey

Analyze a user dataset and recommend the best LLMaps visualization path without immediately generating code.

## Inputs

- Data file path (`.geojson`, `.csv`, `.parquet`)
- Optional user goal (explore, compare, storytelling)

## Procedure

1. Read and profile the dataset.
2. Detect geometry profile:
- Point / MultiPoint
- Polygon / MultiPolygon
- LineString / MultiLineString
- Mixed
3. Build a structured report:
- Feature count
- Bounding box
- Field inventory with inferred types
- Numeric stats (min, max, typical spread)
- Categorical cardinality and top categories
- Data quality notes (missing geometry, null-heavy columns, malformed values)
4. Recommend visualization approach using `compass/decision-tree.md`.
5. Propose one primary recipe and one fallback recipe from `compass/recipes/`.
6. Suggest next 3 questions from `compass/question-bank.md`.

## Output Format

Use this structure:

1. `Dataset Summary`
2. `Field Analysis`
3. `Risks And Data Quality`
4. `Recommended Recipe`
5. `Fallback Recipe`
6. `Next Questions`

## References

- `compass/decision-tree.md`
- `compass/question-bank.md`
- `compass/recipes/`
- `llmaps/LLM_CONTEXT.md`
