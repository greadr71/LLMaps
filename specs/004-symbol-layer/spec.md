# Feature Specification: SymbolLayer

**Feature Folder**: `specs/004-symbol-layer`  
**Created**: 2026-03-26  
**Status**: Approved

## Why This Change Exists

LLMaps can render points as circles (`CircleLayer`) but has no `"symbol"` layer type. MapLibre GL JS `"symbol"` layers allow icon images (sprites) and optional text labels to be drawn at point locations, which is the standard approach for icon-based markers — e.g. category badges, custom pin icons, or lettered markers.

The immediate consumer is `atlas/source/firma-rr-zrr-map`, which needs icon markers with letters Ф / Р / З for its three hierarchy layers. Currently the approach uses `VectorTileLayer(geometry_type="circle")` with JS post-processing; a proper `SymbolLayer` eliminates that workaround.

## User Scenarios And Testing

### User Story 1 — Icon markers from a pre-registered image (Priority: P1)

A developer registers SVG-based images with `map.addImage(...)` in custom JS, then assigns them to point features via `SymbolLayer(icon_image=...)` with a static name or a MapLibre expression.

**Why this priority**: Core use-case. Without it, custom icon markers require writing raw MapLibre spec by hand in `add_custom_js`.

**Independent Test**: Run `python generate_map.py` in `firma-rr-zrr-map`; inspect generated HTML — must contain `"type": "symbol"` for all three layers, and `"icon-image"` with valid MapLibre expression.

**Acceptance Scenarios**:

1. **Given** a `VectorTileSource`, **When** `SymbolLayer(id, source, source_layer, icon_image="my-icon")` is constructed, **Then** `to_dict()` returns `{"type": "symbol", "layout": {"icon-image": "my-icon", ...}, "source-layer": "my-layer", ...}`.
2. **Given** an `icon_image` that is a MapLibre expression list (e.g. `["concat", "fr-icon-", ...]`), **When** serialized, **Then** the expression is preserved verbatim in `"layout"["icon-image"]`.
3. **Given** `source_layer=None`, **When** serialized, **Then** `"source-layer"` key is absent (GeoJSON source compatibility).

### User Story 2 — Optional text label alongside icon (Priority: P2)

A developer passes `text_field` to render a text label near the icon (e.g. feature property name).

**Why this priority**: Useful but not needed by the immediate consumer.

**Acceptance Scenarios**:

1. **Given** `text_field="name"`, **When** serialized, **Then** `"layout"["text-field"]` equals `["get", "name"]`.
2. **Given** `text_field=None` (default), **When** serialized, **Then** `"text-field"` key is absent from layout.

## Edge Cases

- `icon_image=None` — omit `"icon-image"` from layout (pure text symbol or placeholder).
- `source_layer=""` (empty string) — treat same as `None`; omit `"source-layer"`.
- `icon_allow_overlap=True` by default — icons should not disappear on dense data.
- Works with both `FileSource`/`ApiSource` (GeoJSON) and `VectorTileSource` (PBF).

## Public API Impact

- **Affected API surface**: `llmaps.layers`
- **New symbols**: `SymbolLayer` dataclass
- **Backward compatibility**: Fully additive, no existing code changes.
- **Migration note needed**: No.

## Documentation Impact

- [x] `llmaps/LLM_CONTEXT.md` — add `SymbolLayer` constructor stub
- [ ] `docs/api/map.md` — no change
- [x] `docs/api/layers.md` — add SymbolLayer section
- [ ] `docs/api/sources.md` — no change
- [ ] `docs/api/components.md` — no change
- [ ] `docs/recipes/` — no change
- [x] `README.md` — add SymbolLayer to layers table

## Verification Impact

- **Pytest coverage**: Add `tests/test_symbol_layer.py` — serialize, source-layer omission, expression icon_image, text_field.
- **Example validation**: `generate_map.py` in `atlas/source/firma-rr-zrr-map` — must produce valid HTML.
- **Consumer/browser validation**: Open generated HTML; icons Ф/Р/З should render.

## Requirements

### Functional Requirements

- **FR-001**: `SymbolLayer` MUST emit `"type": "symbol"` in `to_dict()`.
- **FR-002**: `SymbolLayer` MUST emit `"layout"` with icon and text properties (omitting None values).
- **FR-003**: `SymbolLayer` MUST emit `"source-layer"` only when `source_layer` is a non-empty string.
- **FR-004**: `icon_image` MUST accept both a string and a MapLibre expression (list), both passed through verbatim.
- **FR-005**: `text_field` MUST be auto-wrapped as `["get", field_name]` when a plain string is given.
- **FR-006**: `SymbolLayer` MUST be importable from `llmaps.layers`.
