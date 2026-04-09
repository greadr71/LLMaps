---
name: llmaps
description: Guides using and contributing to LLMaps: Python library for interactive web maps (MapLibre, single HTML). Use when building maps with llmaps (pip or repo), when editing the llmaps repo, or when the user mentions llmaps, MapLibre, or map generation.
---

# LLMaps

## Compass Assistant

Compass is the default map-building workflow for data-to-map requests.

### Critical Gate

When building a map with LLMaps, do not generate or write `build_map.py` until all Compass pre-code steps are completed.

Required order:
1. Survey: inspect data and provide a short survey summary to the user.
2. Stop and ask: ask required intent/style/component questions from `compass/question-bank.md`.
3. Confirm: present selected recipe from `compass/decision-tree.md` and wait for user confirmation.
4. Generate: only then generate runnable `build_map.py` and refine on request.

### Question-First Planning Policy (Strict)

This policy is mandatory for plan generation and is designed to maximize clarifying questions before implementation details.

1. Never provide implementation steps, file-level edit plans, or code skeletons before Question phase is complete.
2. Always ask all questions marked `Required: Yes` from `compass/question-bank.md`.
3. In addition to required questions, ask at least 2 adaptive clarifying questions when candidates exist (style, components, popup/sidebar, tiles, locale, output path).
4. If defaults could be applied, still ask user confirmation instead of silently applying defaults during planning.
5. Recipe confirmation is a hard stop: do not proceed to generation planning until the user explicitly confirms the selected recipe.
6. If user request is ambiguous (geometry columns, ID field, output folder, map purpose), ask questions first and pause.

Preflight checklist before any `build_map.py` plan details:
- Survey summary shown and acknowledged.
- Required questions asked and answered.
- Adaptive questions asked or explicitly skipped by user.
- Recipe selected and explicitly confirmed by user.

- Overview: `compass/README.md`
- Decision logic: `compass/decision-tree.md`
- Adaptive questions: `compass/question-bank.md`
- Code templates: `compass/recipes/`

### Implicit Activation Rule

When a user asks to create a map from data (for example: "create an interactive map from X.geojson"), you MUST follow Compass workflow even if no explicit command is provided.

Required flow:

1. Survey data.
2. Ask focused intent questions (including all questions marked `Required: Yes` in `compass/question-bank.md`).
3. Select recipe via `compass/decision-tree.md` and confirm it with the user.
4. Generate runnable `build_map.py` and refine on request.

Behavioral guardrails for this flow:
- Do not jump from survey directly to recipe/code, even if the dataset looks straightforward.
- Do not embed hidden assumptions in plans; convert assumptions into explicit questions.
- If multiple valid outcomes exist, ask the user to choose (for example: popup vs sidebar, OSM vs Carto tiles, hover vs click popup).
- In planning mode, prefer one short question round before drafting implementation steps.

If user explicitly invokes command form, use:

- `/llmaps.compass`
- `/llmaps.compass-survey`
- `/llmaps.compass-refine`

## Using llmaps (pip install or without the repo)

Form context **as exhaustively as possible**. Do not limit context to a single file; when the user or the task needs full understanding, read the relevant files from the installed package.

**Package path:** `import llmaps; pkg_path = llmaps.__path__[0]`. Read files relative to `pkg_path`.

- **Always use:** `LLM_CONTEXT.md` (scenarios and API stubs).
- **When full context is needed**, also read from the package:
  - Source: `map.py`, `tiles.py`, `expressions.py`; directories `layers/`, `sources/`, `components/` (all `.py`); `core/` (generator, config, utils); optionally `optimizers/`.
  - Frontend: `templates/` (base.html, JS fragments, CSS).
- If the package exposes `export_docs(target_dir)`, calling it and using the exported docs/examples in the workspace is an option.
- You may use `get_llm_context()` for a compact reference, but for non-trivial tasks **add** context by reading the listed package files and directories.

**Rule:** Form context exhaustively; when needed, read the listed files and directories of the installed package via `llmaps.__path__[0]`, not only LLM_CONTEXT.md.

---

## Working in the llmaps repository

### Purpose

LLMaps is a Python library for interactive web maps: declarative API → single HTML with MapLibre. LLM-first design; all API is serializable via `to_dict()`.

### Repo structure

- **llmaps/** — package: `map.py`, `tiles.py`, `expressions.py`, `layers/`, `sources/`, `components/`, `core/` (generator, config), `optimizers/`, `templates/`.
- **examples/** — categorized example dirs: `technical/` and `real-world/`, each containing per-example dirs with `prepare_data.py`, `build_map.py`, `map.html` (or custom output HTML), `data/`.
- **docs/api/** — map, layers, sources, components; **docs/recipes/** — heatmap, embedded-map, comparison, feature-state-highlighting.
- **specs/** — lightweight feature specs for meaningful public API changes; includes `templates/` for spec, plan, and task documents.
- No CLI; use `Map`, `add_layer`, `add_component`, `auto_extent`, `save()` / `to_html()`.

### Documentation update rules

- For **any** public API change: update `llmaps/LLM_CONTEXT.md` (and thus `get_llm_context()`) and the corresponding file in `docs/api/` (map.md, layers.md, sources.md, components.md).
- **Matrix (from CONTRIBUTING):** Map param/method → map.md + LLM_CONTEXT + map.py docstring; new/changed layer → layers.md + LLM_CONTEXT + docstring + `layers/__init__.py`; same pattern for sources and components. Tile/expression/JS/embedded changes → listed docs + LLM_CONTEXT.
- Pre-commit checklist: docstrings, LLM_CONTEXT, docs/api, docs/recipes if pattern affected, examples still run.
- For meaningful public behavior changes, also consult `CONSTITUTION.md` and add a feature folder under `specs/` before implementation.

### Extending the library

- **New layer:** add in `llmaps/layers/`, implement `to_dict()`, export in `layers/__init__.py`; update LLM_CONTEXT + docs/api/layers.md.
- **New source:** `llmaps/sources/` + `sources/__init__.py`; same doc updates.
- **New component:** `llmaps/components/` + `components/__init__.py`; same doc updates.
- Flow: Python API → `to_dict()` → `core/generator.py` + Jinja2 templates → single HTML.

### Running and developing

- Install: `pip install -e .` from repo root.
- Examples: from an example dir (e.g. `examples/real-world/cafes/`), run `python prepare_data.py` then `python build_map.py`; open `map.html`. For technical examples like `examples/technical/dashboard/`, run `python build_map.py`.
- Tests: `pytest tests/` (currently only `.gitkeep` in tests).
- For planned public API work: create `specs/[###-feature-name]/spec.md`, `plan.md`, and `tasks.md` from the templates before implementation.

### Tech stack

Python ≥3.10, Hatch, Jinja2, pandas, geopandas, shapely, geobuf, h3, jenkspy. Frontend: MapLibre GL JS via CDN in `llmaps/templates/`; no Node in repo.

### References

- In-repo: `llmaps/LLM_CONTEXT.md` (canonical API stubs and scenarios), CONTRIBUTING.md (doc matrix), PHILOSOPHY.md (design principles), `CONSTITUTION.md`, and `specs/README.md`.
- Do not treat CLAUDE.md in llmaps as library API docs; it is workspace-specific (YouTrack, sheets).

### Maintaining this skill

When changing the llmaps repo in any of these ways: edits to CONTRIBUTING.md (doc matrix, checklist, or scope), repo or package structure (new top-level dirs, new modules under `llmaps/`, moved files), or how to install/run examples/tests — **also update this skill**: adjust the sections "Repo structure", "Documentation update rules", and "Running and developing" so they match the new state. Update `cursor-skill/SKILL.md` in the repo (or your copy at `~/.cursor/skills/llmaps/SKILL.md` if you use a personal copy). Do this in the same edit session as the repo changes.

Do not update the skill when only API surface or doc content changes (e.g. new Map parameter or new recipe) if structure and process are unchanged; the repo remains the source of truth for API details via LLM_CONTEXT and docs/api.
