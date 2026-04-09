# Feature Specification: Geoscience Color Palettes

**Feature Folder**: `specs/005-geoscience-palettes`  
**Created**: 2025-07-15  
**Status**: Draft

## Why This Change Exists

llmaps currently depends on matplotlib (~60 MB) solely for a single function `_colors_from_cmap()` that samples hex colors from matplotlib colormaps. The built-in `_DEFAULT_COLORS` is a hardcoded 5-color green→red ramp with no metadata (blindsafe, perceptual uniformity, variable context).

[color-for-geoscience](https://github.com/dominicroye/color-for-geoscience) provides 50+ professionally curated palettes specifically designed for geoscientific map visualisation — with rich metadata that enables LLM-based palette selection via compass. Integrating these palettes and **removing matplotlib entirely** replaces a heavy, metadata-less dependency with a lightweight, purpose-built palette system.

## User Scenarios And Testing

### User Story 1 — palette= in compute_color_stops() (Priority: P1)

Developer passes `palette="rain_blues"` to `compute_color_stops()` and gets properly interpolated color stops from the embedded geoscience palette.

**Why this priority**: Core palette integration; all other features depend on this.

**Independent Test**: `pytest tests/test_palettes.py`

**Acceptance Scenarios**:

1. **Given** values `[1, 5, 10, 20, 50]`, **When** `compute_color_stops(values, palette="rain_blues")`, **Then** returns 5 `ColorStop` tuples with hex colors from the rain_blues palette.
2. **Given** `palette="nonexistent"`, **When** `compute_color_stops(values, palette="nonexistent")`, **Then** raises `ValueError` with a helpful message listing available palettes.
3. **Given** both `palette` and `colors` are set, **When** called, **Then** raises `ValueError` (conflicting params).
4. **Given** no `palette`, no `colors`, **When** `compute_color_stops(values)`, **Then** uses a default geoscience palette (sequential, blindsafe, perceptually uniform).

### User Story 2 — Palette Discovery API (Priority: P1)

Developer (or LLM agent via compass) can list available palettes, filter by type/variable/blindsafe, and retrieve hex colors for any palette.

**Why this priority**: Without discovery, neither humans nor LLM agents can choose palettes.

**Independent Test**: `pytest tests/test_palettes.py`

**Acceptance Scenarios**:

1. **Given** llmaps is installed, **When** `list_palettes()`, **Then** returns 50+ palette metadata dicts.
2. **Given** filter `type="sequential", blindsafe=True`, **When** `list_palettes(...)`, **Then** returns a subset matching criteria.
3. **Given** `palette_id="rain_blues"`, **When** `get_palette_colors("rain_blues", n=7)`, **Then** returns 7 hex strings resampled from the palette.

### User Story 3 — LLM Agent Palette Selection via Compass (Priority: P2)

Compass question-bank and decision-tree guide the LLM agent to pick the optimal palette based on data semantics (variable type, sequential vs diverging, etc.).

**Why this priority**: Builds on Stories 1–2, improves map quality but not a blocker.

**Independent Test**: Manual review of compass output for a choropleth recipe.

**Acceptance Scenarios**:

1. **Given** a choropleth recipe, **When** LLM reads decision-tree.md, **Then** it selects an appropriate palette by type and variable context.
2. **Given** the user has categorical data, **When** LLM reads question-bank.md Q-LYR-06, **Then** it recommends a qualitative palette.
3. **Given** the user is not satisfied with suggested palettes, **When** LLM presents palette options, **Then** it also offers https://dominicroye.github.io/color-for-geoscience/ for manual visual selection.

## Edge Cases

- `get_palette_colors(id, n=1)` — returns a single color (first or middle).
- `get_palette_colors(id, n=N)` where N > len(palette.colors) — resamples via linear interpolation.
- `compute_color_stops(values)` with no palette/colors — uses new default palette (replaces `_DEFAULT_COLORS`).
- Unknown palette id — `ValueError` with available palette names.
- Empty values list — existing behavior preserved (handled by `compute_color_stops`).

## Public API Impact

- **Affected API surface**: expressions (`compute_color_stops`), new module `palettes`
- **New symbols**:
  - `llmaps.palettes.get_palette(id) -> dict`
  - `llmaps.palettes.get_palette_colors(id, n=None) -> List[str]`
  - `llmaps.palettes.list_palettes(type=, variable=, blindsafe=, perceptually_uniform=) -> List[dict]`
  - `compute_color_stops(..., palette=)` — new parameter
- **Removed symbols**:
  - `_colors_from_cmap()` — deleted
  - `cmap=` parameter of `compute_color_stops()` — removed
  - `_DEFAULT_COLORS` — replaced with geoscience palette
- **Removed dependency**: `matplotlib>=3.7` — removed from `pyproject.toml`
- **Backward compatibility**: **Breaking** for users relying on `cmap=` parameter. Migration: replace `cmap="viridis"` with `palette="<equivalent_geoscience_id>"` or `colors=[<hex list>]`.
- **Migration note needed**: Yes — document cmap= removal and matplotlib dependency removal in CHANGELOG.

## Documentation Impact

- [x] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md) — add Palettes section, update compute_color_stops signature (remove cmap=)
- [x] [docs/recipes/feature-state-highlighting.md](../../docs/recipes/feature-state-highlighting.md) — replace `cmap="YlOrRd"` with `palette=`
- [x] [CLAUDE.md](../../CLAUDE.md) — remove matplotlib references
- [x] [cursor-skill/SKILL.md](../../cursor-skill/SKILL.md) — remove matplotlib from tech stack
- [x] [compass/question-bank.md](../../compass/question-bank.md) — replace viridis/plasma/YlOrRd with geoscience palettes
- [x] [compass/decision-tree.md](../../compass/decision-tree.md) — add Palette Selection section
- [x] [compass/recipes/choropleth.md](../../compass/recipes/choropleth.md) — `cmap=` → `palette=`
- [x] [compass/recipes/hexagons.md](../../compass/recipes/hexagons.md) — use get_palette_colors()
- [x] [examples/index.html](../../examples/index.html) — update "plasma colormap" description

## Verification Impact

- **Pytest coverage**: New `tests/test_palettes.py` covering palette loading, filtering, resampling, compute_color_stops integration, error cases.
- **Example validation**: Re-run `examples/real-world/earthquakes/build_map.py` and `examples/real-world/world_population/build_map.py` after migration from cmap= to palette=.
- **Consumer/browser validation**: Verify generated map HTML renders correct colors in browser.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide `get_palette_colors(id, n)` returning n hex colors from an embedded geoscience palette.
- **FR-002**: System MUST provide `list_palettes()` with filtering by `type`, `variable`, `blindsafe`, `perceptually_uniform`.
- **FR-003**: `compute_color_stops()` MUST accept `palette=` parameter to select an embedded palette.
- **FR-004**: System MUST NOT depend on matplotlib at runtime or in dependencies.
- **FR-005**: If both `palette` and `colors` are provided, system MUST raise `ValueError`.
- **FR-006**: Default palette (no `palette=`, no `colors=`) MUST be a blindsafe, perceptually uniform sequential geoscience palette.
- **FR-007**: Compass decision-tree and question-bank MUST guide LLM agents to select appropriate palette by data context.
- **FR-008**: Compass guidance MUST include https://dominicroye.github.io/color-for-geoscience/ as a manual fallback so users can choose a palette themselves if suggested options are not suitable.
