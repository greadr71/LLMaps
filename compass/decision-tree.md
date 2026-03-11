# Compass Decision Tree

This document defines how Compass selects a recipe and generates `build_map.py`.

## Root

1. Data file provided?
- Yes: run Survey stage.
- No: switch to Manual Intent stage (ask what user wants to map, expected geometry, and preferred interaction).

2. Survey output required:
- Geometry type: `Point`, `MultiPoint`, `Polygon`, `MultiPolygon`, `LineString`, `MultiLineString`, or mixed.
- Feature count.
- Fields and inferred types.
- Numeric fields and ranges.
- Categorical fields and unique counts.
- Bounding box.

## CHECKPOINT: Survey Confirmation

Before routing, present the survey summary to the user and wait for acknowledgment.
Do not continue to recipe routing until this checkpoint is complete.

## Geometry Routing

### A) POINTS Branch (`Point`, `MultiPoint`)

1. Count threshold:
- `< 10,000`: use `CircleLayer` path.
- `>= 10,000`: use `H3Layer` path.

2. For `< 10,000`:
- Numeric field chosen for style?
- Yes: `recipes/points-sized.md`.
- No: `recipes/points-basic.md`.

3. For `>= 10,000`:
- Use `recipes/hexagons.md` with compression enabled.

### B) POLYGONS Branch (`Polygon`, `MultiPolygon`)

1. Before/after intent detected?
- Yes: `recipes/comparison.md`.
- No: continue.

2. Primary styling field type:
- Numeric: `recipes/choropleth.md`.
- Categorical: `recipes/categorical.md`.
- No suitable field: fallback to single-color fill based on `recipes/categorical.md` with default category mapping.

### C) LINES Branch (`LineString`, `MultiLineString`)

LLMaps does not have a dedicated `LineLayer` in the core scenario table used by Compass recipes.

1. If line dataset includes representative points or centroids:
- Treat as points and route to POINTS branch.

2. If user requests area comparison/story narrative around line context:
- Route to `recipes/storytelling.md` or `recipes/comparison.md` when appropriate.

3. Otherwise:
- Ask for conversion preference (keep as lines outside current Compass recipes, or derive points/polygons for Compass flow).

### D) MIXED Geometry

1. Ask user to split by dominant geometry, or select dominant type automatically when one type is >80%.
2. Route dominant subset through POINTS/POLYGONS/LINES branch.

## Component Adaptation Branch

After recipe selection, apply adaptive defaults:

1. Legend
- Default: enabled.

2. Popup vs Sidebar
- Simple detail needs: `Popup`.
- Multi-field or long-form detail: `Sidebar` (optionally with `FeatureSearch`).

3. FeatureSearch
- Enable if at least one searchable identifier-like field exists (`name`, `id`, code fields) and user indicates lookup intent.

4. BasemapSwitcher
- Enable when user asks to compare visual context across styles.

5. Storytelling
- Enable when user needs sequence, explanation, or narrative scenes.

6. Controls
- Default: `Controls(zoom=True, scale=True)`.

## Style Branch

1. Tiles by bbox and intent:
- Dense urban context or POI map: `osm` or `carto-light`.
- Dark emphasis or seismic/night-like context: `carto-dark`.
- Regional preference can override to `yandex` or `2gis`.

2. Locale:
- Default `en-US`.
- Use user locale when explicitly requested (for number formatting in Popup/Sidebar).

3. Compression:
- Default `use_compression=True`.
- Keep enabled for large GeoJSON/H3 workflows.

## CHECKPOINT: Intent Confirmation

Before terminal generation, ask required questions from `compass/question-bank.md` and any adaptive follow-up questions based on geometry and intent.
Then present the selected recipe path and wait for user confirmation.

## Terminal

Precondition:
- The user has acknowledged survey summary.
- Required questions have been asked and answered (or defaults accepted explicitly).
- The selected recipe has been confirmed by the user.

If any precondition is missing, stop and return to survey/intent steps.

1. Select final recipe.
2. Fill placeholders from survey + user answers.
3. Generate `build_map.py`.
4. Include `m.auto_extent()` when center/zoom are unknown.
5. Save map to `map.html`.
