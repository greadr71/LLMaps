# Compass

Compass is an AI map-building assistant for LLMaps.

## Hard Rules

These rules are mandatory for any Compass run:

1. Never generate or write `build_map.py` before completing both Survey and Intent phases.
2. Always present a short survey summary to the user before selecting a recipe.
3. Always ask required intent/style/component questions before code generation.
4. Always present the selected recipe and wait for user confirmation before code generation.

Wrong workflow:
- Read data -> pick a recipe -> generate code -> collect corrections in many follow-up turns.

Correct workflow:
- Survey data -> ask adaptive required questions -> confirm recipe -> generate code -> refine.

It does not change the LLMaps Python API. Compass is a documentation layer that helps an AI agent do four things consistently:

1. Survey the user's dataset.
2. Ask only relevant questions.
3. Select the right mapping recipe.
4. Generate a working `build_map.py` with placeholders filled.

## Purpose

Compass solves the cold start problem for users who have data but do not know which layer, components, and style options to choose.

The assistant relies on:

- `compass/decision-tree.md` for routing logic.
- `compass/question-bank.md` for adaptive follow-up questions.
- `compass/recipes/*.md` for ready-to-fill `build_map.py` templates.

## Activation

Compass supports two activation paths:

- Implicit activation: the user asks naturally, for example "Create a map from cafes.geojson".
- Explicit activation: the user invokes a dedicated command such as `/llmaps.compass`.

Both paths use the same Compass knowledge base files.

## Typical Workflow

1. Survey
- Read data file metadata and content profile: geometry type, feature count, fields, numeric ranges, categorical cardinality, and bounding box.
2. Intent
- Ask focused questions from `question-bank.md` based on the survey.
 - Required before code generation: ask questions marked `Required: Yes`.
3. Generate
 - Select a recipe from `compass/recipes/`, confirm the recipe with the user, then write `build_map.py`.
4. Refine
- Iterate on style, components, and interaction behavior.

## Example Dialogue

User:
"Create an interactive map from `examples/real-world/cafes/data/paris_cafes.geojson`."

Assistant:
"I analyzed your file. It contains Point features (2,143 records), fields include `name`, `amenity`, `cuisine`, and `opening_hours`. Do you want fixed-size points or size/color driven by a numeric field?"

User:
"Fixed-size points, color by amenity, popup on hover, and search by name."

Assistant:
"Great. I will use the points-basic recipe and add FeatureSearch configuration. I will now generate `build_map.py`."

Result:
- A runnable `build_map.py` that uses `CircleLayer`, `Popup`, `Legend`, `Controls`, and optional search/sidebar components.

## Files In This Folder

- `README.md`: high-level Compass overview.
- `decision-tree.md`: deterministic recipe selection logic.
- `question-bank.md`: adaptive interview prompts.
- `recipes/`: recipe templates with `{PLACEHOLDER}` markers.
