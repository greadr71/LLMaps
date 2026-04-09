# Implementation Plan: Geoscience Color Palettes

**Feature Folder**: `specs/005-geoscience-palettes`  
**Date**: 2025-07-15  
**Spec**: [spec.md](spec.md)

## Summary

Replace matplotlib-based color system with embedded geoscience palettes from [color-for-geoscience](https://github.com/dominicroye/color-for-geoscience). Add new `llmaps.palettes` module, `palette=` parameter in `compute_color_stops()`, and update compass for LLM-guided palette selection. **Fully remove matplotlib** — no deprecation, no optional dependency.

## Technical Context

- **Language/Version**: Python 3.10+
- **Project Type**: Library
- **Core Stack**: `jinja2`, `pandas`, `geopandas`, `shapely`, `MapLibre GL JS`
- **Testing**: `pytest`, example validation, optional browser checks
- **Constraints**: breaking change for `cmap=` users; must provide clear migration path

## Constitution Check

- [x] Article I (Public API First): removing `cmap=`, adding `palette=`, new `palettes` module — all public API changes explicitly identified.
- [x] Article I (Public API First): breaking change documented; migration note in spec.
- [x] Article III (Documentation Parity): 9 documentation artifacts listed in spec.
- [x] Article IV (Verification Before Merge): test plan + example validation defined.
- [x] Article VI (Simplicity Over Process): single module `palettes/__init__.py`, embedded JSON, no plugin system.

## Affected Code Paths

- [x] [llmaps/expressions.py](../../llmaps/expressions.py) — remove `cmap=`, `_colors_from_cmap()`, `_DEFAULT_COLORS`; add `palette=`
- [x] [llmaps/palettes/__init__.py](../../llmaps/palettes/__init__.py) — **NEW** module
- [x] [llmaps/palettes/data/palettes.json](../../llmaps/palettes/data/palettes.json) — **NEW** embedded data
- [x] [llmaps/__init__.py](../../llmaps/__init__.py) — export `palettes`
- [x] [pyproject.toml](../../pyproject.toml) — remove `matplotlib>=3.7`, add `force-include` for palettes.json
- [x] [scripts/prepare_palettes.py](../../scripts/prepare_palettes.py) — **NEW** data preparation script

## Affected Documentation

- [x] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md) — add Palettes section, remove cmap from compute_color_stops
- [x] [CLAUDE.md](../../CLAUDE.md) — remove 3 matplotlib references (lines 66, 76, 99)
- [x] [cursor-skill/SKILL.md](../../cursor-skill/SKILL.md) — remove matplotlib from tech stack (line 121)
- [x] [docs/recipes/feature-state-highlighting.md](../../docs/recipes/feature-state-highlighting.md) — `cmap="YlOrRd"` → `palette=`
- [x] [compass/question-bank.md](../../compass/question-bank.md) — replace viridis/plasma/YlOrRd in Q-LYR-06
- [x] [compass/decision-tree.md](../../compass/decision-tree.md) — add Palette Selection section
- [x] [compass/recipes/choropleth.md](../../compass/recipes/choropleth.md) — `cmap="{COLOR_PALETTE}"` → `palette="{PALETTE_ID}"`
- [x] [compass/recipes/hexagons.md](../../compass/recipes/hexagons.md) — `colors={COLOR_PALETTE}` → `get_palette_colors()`
- [x] [examples/index.html](../../examples/index.html) — update "plasma colormap" description

## Complete Inventory of Files Requiring matplotlib/cmap Removal

Every file in the repo that references matplotlib, cmap, viridis, plasma, or YlOrRd:

| File | Line(s) | What to change |
|------|---------|----------------|
| `pyproject.toml` | 37 | **Remove** `"matplotlib>=3.7"` from dependencies |
| `llmaps/expressions.py` | 176–189 | **Delete** `_colors_from_cmap()` function |
| `llmaps/expressions.py` | 214,232,242–245,259,275–276 | **Remove** `cmap` parameter, docstring refs, logic branch |
| `llmaps/expressions.py` | 17 | **Replace** `_DEFAULT_COLORS` with geoscience palette lookup |
| `llmaps/LLM_CONTEXT.md` | 179, 182 | **Remove** cmap from `compute_color_stops` signature and comment |
| `CLAUDE.md` | 66, 76, 99 | **Remove** matplotlib from coding guidelines |
| `cursor-skill/SKILL.md` | 121 | **Remove** matplotlib from tech stack list |
| `compass/question-bank.md` | 115–116 | **Replace** viridis/plasma/YlOrRd with geoscience palette IDs |
| `compass/recipes/choropleth.md` | 36 | **Replace** `cmap="{COLOR_PALETTE}"` with `palette="{PALETTE_ID}"` |
| `docs/recipes/feature-state-highlighting.md` | 25 | **Replace** `cmap="YlOrRd"` with `palette="<id>"` |
| `specs/002-compass/validation/build_choropleth.py` | 20 | **Replace** `cmap="viridis"` with `palette="<id>"` |
| `examples/real-world/earthquakes/build_map.py` | 92 | **Replace** `cmap="plasma_r"` with `palette="<id>"` |
| `examples/real-world/world_population/build_map.py` | 46, 51 | **Replace** `cmap="YlOrRd"` with `palette="<id>"` |
| `examples/index.html` | 398 | **Update** "plasma colormap" description text |

## Verification Plan

### Automated Checks

- New `tests/test_palettes.py`:
  - `list_palettes()` returns 50+ entries
  - `list_palettes(type="sequential", blindsafe=True)` filters correctly
  - `get_palette_colors("rain_blues", n=5)` returns 5 hex strings
  - `get_palette_colors("nonexistent")` raises ValueError
  - `compute_color_stops(values, palette="rain_blues")` returns valid stops
  - `compute_color_stops(values, palette="x", colors=["#fff"])` raises ValueError
  - `compute_color_stops(values)` uses new default palette (no matplotlib)
  - `compute_color_stops(values, cmap="viridis")` — **must fail** (parameter removed)

### Example Validation

- Re-run `examples/real-world/earthquakes/build_map.py` — verify map renders
- Re-run `examples/real-world/world_population/build_map.py` — verify map renders
- Re-run `specs/002-compass/validation/build_choropleth.py` — verify output

### Browser Validation

- Open generated HTML files in browser — verify color rendering matches expectation
- Compare visually: old viridis/plasma vs new geoscience palette output

## Implementation Notes

### Phase 1: Data + Palettes Module

1. **Download** `palettes.json` from color-for-geoscience repo (CC BY 4.0)
2. **Create** `scripts/prepare_palettes.py` — strips unnecessary fields, keeps: `id`, `name`, `type`, `variable`, `blindsafe`, `perceptually_uniform`, `uniformity_cv`, `range`, `center`, `context`, `also_useful`, `colors`
3. **Create** `llmaps/palettes/__init__.py` (~80 lines, KISS):
   ```python
   get_palette(palette_id: str) -> dict
   get_palette_colors(palette_id: str, n: Optional[int] = None) -> List[str]
   list_palettes(type=, variable=, blindsafe=, perceptually_uniform=) -> List[dict]
   ```
4. **Update** `pyproject.toml`: remove `"matplotlib>=3.7"`, add palettes.json to `force-include`
5. **Update** `llmaps/__init__.py`: export `palettes`

### Phase 2: expressions.py Integration

1. **Delete** `_colors_from_cmap()` function entirely
2. **Delete** `_DEFAULT_COLORS` constant
3. **Remove** `cmap` parameter from `compute_color_stops()` signature
4. **Add** `palette: Optional[str] = None` parameter
5. **Resolution priority**:
   - If both `palette` and `colors` → `ValueError`
   - `colors` → explicit hex list (highest priority)
   - `palette` → `get_palette_colors(palette, n_stops)`
   - Neither → default geoscience palette (sequential, blindsafe, perceptually uniform)
6. **Remove** `import matplotlib` and all related code

### Phase 3: Compass Update (parallel with Phase 2)

1. **Update** `compass/question-bank.md` Q-LYR-06:
   - Replace viridis/plasma/YlOrRd with geoscience palette categories
   - Reference https://dominicroye.github.io/color-for-geoscience/ for visual picker
   - `palette=` as the parameter (not `cmap=`)
2. **Update** `compass/decision-tree.md` — add palette selection logic:
   - Sequential → absolute numeric data
   - Diverging → data with center/zero
   - Qualitative → categorical data
   - Default → blindsafe + perceptually uniform sequential
3. **Update** recipes: choropleth, hexagons, points-sized, categorical

### Phase 4: Documentation

1. **Update** `llmaps/LLM_CONTEXT.md` — add Palettes section, remove cmap=
2. **Update** `docs/recipes/feature-state-highlighting.md` — palette= examples
3. **Update** `CLAUDE.md` — remove 3 matplotlib mentions
4. **Update** `cursor-skill/SKILL.md` — remove matplotlib from tech stack
5. **Create** `docs/recipes/palette-selection.md` — palette choice guide

### Phase 5: Examples Migration

1. **Update** `examples/real-world/earthquakes/build_map.py` — `cmap="plasma_r"` → `palette="<id>"`
2. **Update** `examples/real-world/world_population/build_map.py` — `cmap="YlOrRd"` → `palette="<id>"`
3. **Update** `specs/002-compass/validation/build_choropleth.py` — `cmap="viridis"` → `palette="<id>"`
4. **Update** `examples/index.html` — text description

### Phase Dependencies

```
Phase 1 (data + module)
    ↓           ↓
Phase 2      Phase 3       ← parallel
    ↓           ↓
Phase 4 (documentation)    ← depends on 2+3
    ↓
Phase 5 (examples)
```

## Mapping: matplotlib colormaps → geoscience palettes

To be determined during implementation. Approximate mapping:

| Old (matplotlib) | Usage context | Candidate geoscience palette | Type |
|------------------|---------------|------------------------------|------|
| `viridis` | Generic sequential | TBD (blindsafe, perceptually uniform) | sequential |
| `plasma` / `plasma_r` | Earthquake depth | TBD (variable=depth or also_useful) | sequential |
| `YlOrRd` | Population density, highlighting | TBD (variable=temperature or population) | sequential |
| `_DEFAULT_COLORS` (green→red) | Default fallback | TBD (blindsafe + perceptually uniform) | sequential |

> **Note**: Exact palette IDs will be chosen during Phase 1 by matching `variable` and `also_useful` metadata from color-for-geoscience against the data contexts used in llmaps examples.

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|-----------|--------------------------------------|
| Full matplotlib removal (not deprecation) | matplotlib is ~60 MB, used for ONE function. Deprecation means maintaining dead code indefinitely. | Deprecation → keeps unnecessary weight, confusing dual API |
| Embedded palettes.json (not runtime download) | Offline stability, no network dependency, reproducible builds | Runtime API → fragile, blocks air-gapped usage |
| Single `palettes/__init__.py` | ~80 lines, no need for loader.py + filters.py split | Multi-file → over-engineering for <100 lines |
| Color resampling in `get_palette_colors(n=)` | Palettes have varying color counts (5–256); `n_stops` in compute_color_stops needs exact count | Requiring exact-count palette → too restrictive |
