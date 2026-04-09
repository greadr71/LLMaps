# Tasks: Geoscience Color Palettes

**Input**: [spec.md](spec.md) and [plan.md](plan.md)

## Phase 1: Data + Palettes Module

- [x] T001 Download `palettes.json` from color-for-geoscience repo
- [x] T002 Create `scripts/prepare_palettes.py` — strip unnecessary fields, output to `llmaps/palettes/data/palettes.json`
- [x] T003 Run `scripts/prepare_palettes.py` → generate `llmaps/palettes/data/palettes.json`
- [x] T004 Create `llmaps/palettes/__init__.py` with `get_palette()`, `get_palette_colors()`, `list_palettes()`
- [x] T005 Update `pyproject.toml`: remove `"matplotlib>=3.7"` from dependencies, add `llmaps/palettes/data/palettes.json` to `force-include`
- [x] T006 Update `llmaps/__init__.py`: add `from . import palettes` and `"palettes"` to `__all__`
- [x] T007 Choose default palette (sequential, blindsafe, perceptually uniform) and document the choice
- [x] T008 Determine cmap→palette mapping (viridis→?, plasma→?, YlOrRd→?) for Phase 5

## Phase 2: expressions.py Integration

- [x] T009 Delete `_colors_from_cmap()` function (lines 176–189)
- [x] T010 Delete `_DEFAULT_COLORS` constant (line 17), replace with `get_palette_colors(<default_id>, n)`
- [x] T011 Remove `cmap` parameter from `compute_color_stops()` signature and all internal logic
- [x] T012 Add `palette: Optional[str] = None` parameter to `compute_color_stops()`
- [x] T013 Add conflict check: `ValueError` if both `palette` and `colors` are set
- [x] T014 Update `compute_color_stops()` docstring — remove cmap refs, document palette=
- [x] T015 Remove `import matplotlib` and related `ImportError` handling
- [x] T016 [P] Write `tests/test_palettes.py` — palette module tests (loading, filtering, resampling, errors)
- [x] T017 Write integration tests in `tests/test_palettes.py` — `compute_color_stops` with `palette=`
- [x] T018 Verify `compute_color_stops(values, cmap=...)` raises `TypeError` (parameter no longer exists)

## Phase 3: Compass Update (parallel with Phase 2)

- [x] T019 [P] Update `compass/question-bank.md` Q-LYR-06 — replace viridis/plasma/YlOrRd with geoscience palette categories and palette= parameter; explicitly add https://dominicroye.github.io/color-for-geoscience/ as manual fallback when suggested palettes do not fit user preference
- [x] T020 [P] Update `compass/decision-tree.md` — add "Color Palette Selection" section (sequential/diverging/qualitative/default logic)
- [x] T021 [P] Update `compass/recipes/choropleth.md` — `cmap="{COLOR_PALETTE}"` → `palette="{PALETTE_ID}"`
- [x] T022 [P] Update `compass/recipes/hexagons.md` — use `get_palette_colors("{PALETTE_ID}")`
- [x] T023 [P] Update `compass/recipes/points-sized.md` — palette-based color stops if applicable
- [x] T024 [P] Update `compass/recipes/categorical.md` — qualitative palettes for `{COLOR_MAP}`
- [x] T025 [P] Review remaining recipes (points-basic, comparison, search-sidebar, storytelling) for color references

## Phase 4: Documentation

- [x] T026 Update `llmaps/LLM_CONTEXT.md` — add Palettes section, remove `cmap` from `compute_color_stops` signature
- [x] T027 Update `docs/recipes/feature-state-highlighting.md` — `cmap="YlOrRd"` → `palette="<id>"`
- [x] T028 [P] Update `CLAUDE.md` — remove matplotlib references (lines 66, 76, 99)
- [x] T029 [P] Update `cursor-skill/SKILL.md` — remove matplotlib from tech stack (line 121)
- [x] T030 Create `docs/recipes/palette-selection.md` — guide for choosing palettes

## Phase 5: Examples Migration

- [x] T031 Update `examples/real-world/earthquakes/build_map.py` — `cmap="plasma_r"` → `palette="<id>"`
- [x] T032 Update `examples/real-world/world_population/build_map.py` — `cmap="YlOrRd"` → `palette="<id>"`
- [x] T033 Update `specs/002-compass/validation/build_choropleth.py` — `cmap="viridis"` → `palette="<id>"`
- [x] T034 Update `examples/index.html` — update "plasma colormap" description text
- [x] T035 Re-run updated examples and verify HTML output

## Phase 6: Validation

- [x] T036 Run `pytest tests/test_palettes.py` — all pass
- [x] T037 Run `pytest tests/` — no regressions
- [x] T038 Run 2-3 updated examples → verify `map.html` is generated
- [x] T039 Open generated HTML in browser — verify colors render correctly
- [x] T040 Verify `pip install .` works without matplotlib
- [x] T041 Verify compass recipes contain `palette=` / `get_palette_colors()` in templates
- [x] T042 Verify LLM_CONTEXT.md has Palettes section and no cmap references
- [x] T043 Verify no remaining matplotlib/cmap references in repo: `grep -r "matplotlib\|cmap" llmaps/ compass/ docs/ examples/`

## Delivery Notes

- Stop after Phase 2 and re-check if public API semantics changed unexpectedly.
- The cmap→palette mapping (T008) should be reviewed before Phase 5 starts.
- Breaking change: add migration notes to CHANGELOG.md before release.
- Docs drift = incomplete feature — all T026–T030 must be done before merge.
