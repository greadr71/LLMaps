# Implementation Plan: Compass — AI Map-Building Assistant

**Feature Folder**: `specs/002-compass`  
**Date**: 2026-03-11  
**Spec**: [spec.md](spec.md)

## Summary

Compass is an AI-assisted map-building workflow for llmaps. It adds a new `compass/` directory with agent-agnostic reference documents (decision tree, question bank, code recipes) and agent-specific command files under `cursor-skill/commands/`. No Python API changes are involved — this is purely a knowledge/documentation addition that helps AI agents guide users from raw data to a working `build_map.py`.

## Technical Context

- **Language/Version**: Markdown reference docs (no Python code changes)
- **Project Type**: Library documentation / AI agent skill extension
- **Core Stack**: Existing llmaps API (`Map`, layers, sources, components, expressions), Cursor Agent commands (YAML frontmatter + Markdown body)
- **Testing**: Manual smoke-tests with existing example data; recipe validation by running generated scripts
- **Constraints**: All files in English; reference docs must be agent-agnostic; must not duplicate content from `docs/recipes/` or `LLM_CONTEXT.md`

## Constitution Check

- [x] **Article I (Public API First)**: Compass does NOT change the Python API. No new classes, methods, or parameters. Public API scope is explicitly zero.
- [x] **Article I (Public API First)**: Backward compatibility is fully preserved. No existing behavior changes.
- [x] **Article III (Documentation Parity)**: Documentation impact is identified: `README.md`, `cursor-skill/SKILL.md`, and `LLM_CONTEXT.md` (scenario lookup table review). All updates are part of Phase 3 tasks.
- [x] **Article IV (Verification Before Merge)**: Verification path defined before implementation — smoke-test with 4 existing examples (cafes, world_population, earthquakes, gerrymandering), recipe validation, decision tree coverage walkthrough.
- [x] **Article VI (Simplicity Over Process)**: Compass uses the simplest structure that fits: Markdown reference docs + Cursor command files. No Python scripts, no MCP server, no new build tooling. The design adds a top-level `compass/` directory alongside the existing `cursor-skill/`, `docs/`, and `examples/` directories.

## Affected Code Paths

No Python code paths are affected. Compass is a documentation-only addition.

New directories and files created:

- `compass/README.md` — overview, purpose, example dialogue
- `compass/decision-tree.md` — branching logic for data → layer → style → components
- `compass/question-bank.md` — ~20 structured questions with conditions, defaults, and effects
- `compass/recipes/points-basic.md` — CircleLayer + Popup + Legend template
- `compass/recipes/points-sized.md` — CircleLayer with radius/color expressions
- `compass/recipes/hexagons.md` — H3Layer for large datasets
- `compass/recipes/choropleth.md` — FillLayer choropleth template
- `compass/recipes/categorical.md` — FillLayer match expression template
- `compass/recipes/comparison.md` — Before/after slider template
- `compass/recipes/storytelling.md` — Scrollytelling narrative template
- `compass/recipes/search-sidebar.md` — FeatureSearch + Sidebar template
- `cursor-skill/commands/compass.md` — main command (Survey → Intent → Generate → Refine)
- `cursor-skill/commands/compass-survey.md` — standalone data analysis command
- `cursor-skill/commands/compass-refine.md` — iteration on existing map command

## Affected Documentation

- [ ] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md) — review scenario lookup table for completeness against Compass recipes; add Compass mention if appropriate
- [ ] [README.md](../../README.md) — add "Getting Started with Compass" section for newcomers
- [ ] [cursor-skill/SKILL.md](../../cursor-skill/SKILL.md) — add Compass assistant reference and link to `compass/README.md`

Note on `docs/recipes/` vs `compass/recipes/`: These serve different purposes and are NOT duplicates. `docs/recipes/` contains human-facing how-to guides for specific llmaps patterns (storytelling, comparison, etc.). `compass/recipes/` contains AI-agent dialogue templates — full `build_map.py` scripts with `{PLACEHOLDER}` markers that the AI agent fills in during a Compass conversation. They are structured for machine consumption, not human reading.

## Verification Plan

### Automated Checks

No pytest tests needed — Compass is Markdown documentation, not Python code.

### Example Validation

Smoke-test each recipe against existing example data:

| Recipe | Test data | Expected layer |
|--------|-----------|----------------|
| points-basic | `examples/real-world/cafes/data/paris_cafes.geojson` | CircleLayer + Popup + Legend |
| points-sized | Same cafes data (use `rating` field for sizing) | CircleLayer with radius expression |
| hexagons | `examples/real-world/earthquakes/data/earthquakes_2024.csv` | H3Layer |
| choropleth | `examples/real-world/world_population/data/world_population.geojson` | FillLayer choropleth |
| categorical | Same world_population (use region field) | FillLayer with match expression |
| comparison | Requires two datasets — manual placeholder fill | Before/after slider |
| storytelling | `examples/real-world/gerrymandering/` data | Storytelling + Scenes |
| search-sidebar | Cafes data (use `name` field for search) | FeatureSearch + Sidebar |

Process: Fill placeholders manually → `python build_map.py` → open `map.html` → verify map renders.

### Browser Or Consumer Validation

- Open each generated `map.html` in Chrome/Firefox
- Verify: map loads, layers render, components (legend, popup, sidebar) function
- Check: no JS console errors

### Decision Tree Coverage

Walk through the decision tree with at least 3 data profiles:
1. Points, <10k, numeric field → should reach points-sized recipe
2. Polygons, numeric field → should reach choropleth recipe  
3. Points, ≥10k → should reach hexagons recipe

### Cross-Agent Validation (Post-Launch)

After Cursor validation: copy `compass.md` to Claude command format (`.claude/commands/compass.md`), verify the workflow transfers using the same reference docs.

## Implementation Notes

- **Two-layer architecture**: Knowledge base (`compass/`) is read-only reference material. Agent commands (`cursor-skill/commands/`) contain behavioral instructions that link to the knowledge base via file read instructions (e.g. "Read `compass/decision-tree.md` for branching logic").
- **Recipe placeholder convention**: Use `{UPPER_SNAKE_CASE}` markers (e.g. `{SOURCE_PATH}`, `{VALUE_FIELD}`, `{COLOR_PALETTE}`). The AI agent fills these during conversation.
- **Question bank is append-only**: New questions get new IDs (Q-xxx-NN), existing questions are not removed.
- **Decision tree grows with the library**: When new layer types or components are added to llmaps, the decision tree should be updated to include new branches.
- **English only**: All files created by Compass must be in English per PHILOSOPHY.md.

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|--------------------------------------|
| Separate `compass/` directory (not inside `docs/` or `cursor-skill/`) | Agent-agnostic knowledge must live outside any agent-specific directory; also distinct from `docs/` which is human-facing API docs | Putting recipes in `docs/recipes/` would conflate human how-to guides with machine-consumable placeholder templates |
| 8 separate recipe files (not one combined file) | Each recipe is a full `build_map.py` template; combining them would make the file too long and harder for AI agents to read selectively | A single file with sections would require the agent to parse and extract the right section, adding fragility |
| Question bank as a single file (not per-recipe) | Questions cross-cut recipes (e.g. component questions apply to all layer types); a single file with group headers is simpler | Per-recipe questions would cause duplication of shared questions (Legend, Popup, Controls, etc.) |
