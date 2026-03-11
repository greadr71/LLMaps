# Tasks: Compass — AI Map-Building Assistant

**Input**: `spec.md` and `plan.md` from `specs/002-compass/`

## Task Format

- Use checkboxes.
- Include exact file paths.
- Mark parallel-safe tasks with `[P]`.
- Tasks grouped by delivery phase per llmaps convention.

## Phase 1: Intent And Validation Setup

- [ ] T001 Confirm spec scope: Compass is documentation-only, zero Python API changes. Review `spec.md` FR-001 through FR-008.
- [ ] T002 Confirm documentation targets: `README.md`, `cursor-skill/SKILL.md`, `llmaps/LLM_CONTEXT.md` (scenario table review).
- [ ] T003 Define verification path: smoke-test 4 existing examples (cafes, world_population, earthquakes, gerrymandering), recipe fill validation, decision tree walkthrough.

## Phase 2: Knowledge Base (Agent-Agnostic Reference Docs)

- [ ] T004 [P] Create `compass/README.md` — overview of Compass, purpose, how to activate, example dialogue (cafes.geojson → working map).
- [ ] T005 Create `compass/decision-tree.md` — full branching logic:
  - Root: data file provided? → Survey / Manual intent
  - POINTS branch: count threshold (<10k → CircleLayer, ≥10k → H3Layer), numeric/categorical field detection
  - POLYGONS branch: numeric → choropleth, categorical → match, before/after → comparison
  - COMPONENTS branch: adaptive defaults (Legend, Popup vs Sidebar, FeatureSearch, BasemapSwitcher, Storytelling, Controls)
  - STYLE branch: tiles (auto by bbox), locale, compression
  - Terminal: recipe selection → placeholder fill → generate `build_map.py`
- [ ] T006 Create `compass/question-bank.md` — ~20 questions in 5 groups (Data Discovery, Visualization Intent, Layer Config, Components, Style). Each question: ID (Q-GRP-NN), text, condition, options, default, effect on recipe selection.
- [ ] T007 [P] Create `compass/recipes/points-basic.md` — full `build_map.py` template: `CircleLayer` + `Popup` + `Legend` + `Controls` with `{PLACEHOLDER}` markers.
- [ ] T008 [P] Create `compass/recipes/points-sized.md` — `CircleLayer` with radius/color expressions, `{VALUE_FIELD}`, `{COLOR_PALETTE}`.
- [ ] T009 [P] Create `compass/recipes/hexagons.md` — `H3Layer`, `{AGGREGATION}`, `{RESOLUTION}`, compression enabled.
- [ ] T010 [P] Create `compass/recipes/choropleth.md` — `FillLayer` + `feature_state` + `compute_color_stops()`, `{CLASSIFICATION_METHOD}`, `{N_STOPS}`.
- [ ] T011 [P] Create `compass/recipes/categorical.md` — `FillLayer` with `match` expression, `{CATEGORY_FIELD}`, `{COLOR_MAP}`.
- [ ] T012 [P] Create `compass/recipes/comparison.md` — before/after slider, `enable_comparison()`, two sources.
- [ ] T013 [P] Create `compass/recipes/storytelling.md` — `Storytelling` component, `Scene` dataclasses, `{SCENES}` placeholder.
- [ ] T014 [P] Create `compass/recipes/search-sidebar.md` — `FeatureSearch` + `Sidebar`, `{SEARCH_FIELDS}`, `{DISPLAY_FIELDS}`.

## Phase 3: Agent Commands (Cursor-First)

Depends on Phase 2 (commands reference knowledge base files).

- [ ] T015 Create `cursor-skill/commands/compass.md` — main command with YAML frontmatter (description, handoffs to compass-refine and compass-survey). Body: 4-phase workflow (Survey → Intent → Generate → Refine), explicit references to `compass/decision-tree.md`, `compass/question-bank.md`, `compass/recipes/`.
- [ ] T016 [P] Create `cursor-skill/commands/compass-survey.md` — standalone data analysis command. Reads user file (GeoJSON/CSV/Parquet), outputs structured report (geometry, fields, stats, bbox), recommends visualization approach.
- [ ] T017 [P] Create `cursor-skill/commands/compass-refine.md` — iteration command. Reads existing `build_map.py`, suggests targeted changes (colors, components, style, tile provider).

## Phase 4: Documentation Sync

Parallel with Phase 3.

- [ ] T018 Update `cursor-skill/SKILL.md` — add "Compass Assistant" section with brief description and link to `compass/README.md`.
- [ ] T019 [P] Update `README.md` — add "Getting Started with Compass" section for newcomers (after Quick Start, before Examples).
- [ ] T020 [P] Review `llmaps/LLM_CONTEXT.md` scenario lookup table — verify all 8 Compass recipes map to existing scenarios. If any recipe covers a scenario not in the table, flag for update.

## Phase 5: Validation

- [ ] T021 Smoke-test: invoke `/llmaps.compass` in Cursor with `examples/real-world/cafes/data/paris_cafes.geojson` → verify survey, questions, and generated `build_map.py` are correct.
- [ ] T022 [P] Recipe validation: manually fill placeholders in at least 4 recipes (points-basic, choropleth, hexagons, search-sidebar) → run `python build_map.py` → verify `map.html` renders.
- [ ] T023 [P] Decision tree walkthrough: trace 3 data profiles (points <10k, polygons numeric, points ≥10k) through `compass/decision-tree.md` → verify correct recipe is reached.
- [ ] T024 Verify `cursor-skill/SKILL.md`, `README.md`, and `LLM_CONTEXT.md` reflect Compass correctly.
- [ ] T025 Confirm all created files are in English (per PHILOSOPHY.md).

## Delivery Notes

- Stop after Phase 2 and re-check the plan if any recipe reveals a missing API capability in llmaps.
- Treat docs drift as an incomplete feature — `README.md` and `SKILL.md` updates are required, not follow-up.
- Cross-agent validation (Claude, Copilot) is deferred to a separate iteration after Cursor version is validated.
- MCP server, Dashboard recipe, and multi-agent command generation are explicitly out of scope per spec.md.
