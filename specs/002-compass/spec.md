# Feature Specification: Compass — AI Map-Building Assistant

**Feature Folder**: `specs/002-compass`  
**Created**: 2026-03-11  
**Status**: Draft

## Why This Change Exists

New llmaps users face a cold-start problem: they have data (GeoJSON, CSV, Parquet) and want an interactive map, but must manually choose the right layer type, components, color scheme, and tile provider. This requires reading LLM_CONTEXT.md, docs/api/, and examples before writing a single line of `build_map.py`.

Compass solves this by providing an AI-assisted workflow that surveys the user's data, asks focused contextual questions, and generates an optimal `build_map.py` script. It is implemented as **agent-agnostic reference documents** (decision tree, question bank, code recipes) plus **agent-specific command files** (Cursor first, Claude/Copilot later).

Compass does NOT change the llmaps Python API. It is a knowledge layer that helps AI agents use the existing API correctly.

## User Scenarios And Testing

### User Story 1 — Newcomer Creates Map From GeoJSON (Priority: P1)

A developer has a GeoJSON file (e.g. cafes in Paris) and wants an interactive map. They invoke the Compass command in their AI agent. Compass reads their data, reports structure (geometry, fields, stats, bbox), asks 3–5 targeted questions, and generates a working `build_map.py`.

**Why this priority**: This is the core value proposition — zero-to-map for newcomers.

**Independent Test**: Invoke `/llmaps.compass` in Cursor with `examples/real-world/cafes/data/paris_cafes.geojson`. Verify the agent produces a data survey, asks relevant questions (sizing field, color field, components), and generates a runnable `build_map.py` that produces a valid `map.html`.

**Acceptance Scenarios**:

1. **Given** a user has a Point GeoJSON file with <10k features, **When** they invoke Compass and accept defaults, **Then** Compass generates a `build_map.py` using `CircleLayer` + `Popup` + `Legend` + `Controls` that produces a valid HTML map.
2. **Given** a user has a Point GeoJSON with a numeric field, **When** Compass surveys the data, **Then** it asks whether point size should reflect the numeric field and adjusts the recipe accordingly.
3. **Given** a Polygon GeoJSON with a numeric field, **When** Compass surveys the data, **Then** it recommends a choropleth recipe and asks about classification method and color palette.

### User Story 2 — Experienced User Refines Existing Map (Priority: P2)

A developer has an existing `build_map.py` and wants to adjust colors, add components, or change the base map. They invoke the refine command. Compass reads the existing script, understands the current configuration, and suggests targeted changes.

**Why this priority**: Refinement builds on the core flow and is the natural follow-up.

**Independent Test**: Provide Compass an existing `build_map.py` from `examples/real-world/cafes/`. Ask to change colors and add FeatureSearch. Verify the agent modifies the script correctly.

**Acceptance Scenarios**:

1. **Given** an existing `build_map.py` using `CircleLayer`, **When** the user invokes compass-refine and asks to add FeatureSearch, **Then** Compass adds the `FeatureSearch` component with appropriate field configuration.

### User Story 3 — Deep Data Survey (Priority: P2)

A developer wants a detailed data report before building a map. They invoke the survey command with a data file. Compass reads the file and outputs a structured summary: geometry type, field names and types, numeric ranges, unique counts, bounding box, and a visualization recommendation.

**Why this priority**: Survey is a building block of the main flow but also useful standalone.

**Independent Test**: Invoke `/llmaps.compass-survey` with `examples/real-world/world_population/data/world_population.geojson`. Verify the report includes geometry type (MultiPolygon), numeric fields (population, density), and recommends choropleth.

**Acceptance Scenarios**:

1. **Given** a GeoJSON file with MultiPolygon geometry and numeric fields, **When** the user invokes compass-survey, **Then** Compass outputs geometry type, field list with types, numeric ranges, feature count, bounding box, and a visualization recommendation.

## Edge Cases

- **Empty or invalid data file**: Compass should inform the user that the file cannot be parsed and ask for a valid file.
- **Mixed geometry types** (GeometryCollection): Compass should detect mixed geometry, recommend splitting by type, or default to the dominant geometry.
- **Very large datasets** (>100k features): Compass should recommend H3 aggregation with compression, and warn about browser performance limits.
- **CSV without geometry**: Compass should detect lat/lon columns or ask the user to specify coordinate columns.
- **No numeric or categorical fields**: Compass should default to fixed-style points or single-color polygons.
- **Non-English field names**: Compass should handle any field names (CJK, Cyrillic, etc.) and use them in popup/legend configuration.
- **Data file not provided**: Compass should ask what the user wants to show and guide toward manual intent specification.

## Public API Impact

- **Affected API surface**: None — Compass does NOT change the llmaps Python API.
- **New or changed symbols**: None. All new files are documentation/reference docs, not Python code.
- **Backward compatibility**: Fully compatible. No existing behavior is changed.
- **Migration note needed**: No.

## Documentation Impact

- [ ] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md) — update scenario lookup table if Compass recipes reveal missing scenarios
- [ ] [README.md](../../README.md) — add "Getting Started with Compass" section
- [ ] [cursor-skill/SKILL.md](../../cursor-skill/SKILL.md) — add Compass assistant reference

Note: `compass/` is a new top-level directory of reference docs, not API docs. It does NOT duplicate `docs/recipes/` — those are human-facing recipe guides, while `compass/recipes/` are AI-agent dialogue templates with `{PLACEHOLDER}` markers for code generation.

## Verification Impact

- **Pytest coverage**: No new pytest tests needed — Compass is documentation, not Python code.
- **Example validation**: Smoke-test Compass with existing examples (cafes, world_population, earthquakes, gerrymandering) to verify generated `build_map.py` scripts are runnable.
- **Consumer/browser validation**: Run each generated `build_map.py` → open `map.html` in browser → verify map renders correctly.
- **Cross-agent validation**: After Cursor validation, copy compass command to Claude format and verify workflow transfers.

## Requirements

### Functional Requirements

- **FR-001**: Compass MUST survey a user's data file and produce a structured report (geometry type, fields, stats, bounding box).
- **FR-002**: Compass MUST select questions adaptively based on the data survey — not ask all questions to every user.
- **FR-003**: Compass MUST generate a working `build_map.py` that uses the llmaps API correctly per the current `LLM_CONTEXT.md`.
- **FR-004**: Compass reference docs (`compass/`) MUST be agent-agnostic — readable by any AI agent or human.
- **FR-005**: Compass agent commands (`cursor-skill/commands/`) MUST reference the knowledge base, not duplicate it.
- **FR-006**: Decision tree MUST cover all geometry types supported by llmaps (Point, Polygon/MultiPolygon, LineString) and all layer types (CircleLayer, FillLayer, H3Layer).
- **FR-007**: Recipes MUST be consistent with the scenario lookup table in `LLM_CONTEXT.md`.
- **FR-008**: All created files MUST be in English (per PHILOSOPHY.md "English only" principle).

### Non-Functional Requirements

- **NFR-001**: Compass MUST NOT introduce any Python dependencies or runtime changes.
- **NFR-002**: Adding support for a new AI agent MUST require only new command files (3 files), not changes to the knowledge base.
- **NFR-003**: The knowledge base MUST be append-friendly — new recipes and questions can be added without restructuring existing ones.

## Success Criteria

- **SC-001**: A newcomer with a GeoJSON file can go from zero to a working `map.html` in a single Compass conversation (< 10 exchanges).
- **SC-002**: At least 4 of the 8 recipes produce valid `build_map.py` scripts when tested against existing example data.
- **SC-003**: `cursor-skill/SKILL.md`, `README.md`, and `LLM_CONTEXT.md` are updated to reference Compass.
- **SC-004**: The decision tree correctly routes at least 3 different geometry/data combinations (points, choropleth, hexagons) to the appropriate recipe.
