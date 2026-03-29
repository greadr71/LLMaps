# Implementation Plan: SymbolLayer

**Feature Folder**: `specs/004-symbol-layer`  
**Date**: 2026-03-26  
**Spec**: [spec.md](spec.md)

## Summary

Add `SymbolLayer` to `llmaps.layers` as a new dataclass (MapLibre `"symbol"` type). It accepts icon image reference (string or expression), optional text, and all standard symbol layout/paint properties. `source_layer` is optional for cross-source compatibility (GeoJSON + VectorTile). Update docs matrix and write tests. Wire into `atlas/source/firma-rr-zrr-map` as the immediate consumer.

## Technical Context

- **Language/Version**: Python 3.10+
- **Project Type**: Library
- **Core Stack**: dataclasses, MapLibre GL JS
- **Testing**: pytest
- **Constraints**: `to_dict()` must produce valid MapLibre layer spec; None-fields must be omitted from layout/paint output.

## Constitution Check

- [x] Article I (Public API First): `SymbolLayer` is fully described in spec.md before coding.
- [x] Article I (Public API First): additive, no breaking changes.
- [x] Article III (Documentation Parity): all three doc files are identified.
- [x] Article IV (Verification Before Merge): pytest + generate_map.py run path defined.
- [x] Article VI (Simplicity Over Process): single dataclass file, mirrors CircleLayer pattern exactly.

## Affected Code Paths

- [x] `llmaps/layers/symbol.py` — **new file**
- [x] `llmaps/layers/__init__.py` — add import + `__all__`
- [ ] `llmaps/map.py` — no change
- [ ] `llmaps/sources/` — no change
- [ ] `llmaps/components/` — no change
- [ ] `llmaps/expressions.py` — no change
- [ ] `llmaps/core/generator.py` — no change (symbol type serialized like any other)
- [ ] `llmaps/templates/` — no change

Consumer files (outside llmaps):
- `Work/WB/atlas/source/firma-rr-zrr-map/generate_map.py` — replace `VectorTileLayer` with `SymbolLayer`
- `Work/WB/atlas/source/firma-rr-zrr-map/map.js` — add `loadIcons()`, remove `applyColors()`

## Affected Documentation

- [x] `llmaps/LLM_CONTEXT.md` — add SymbolLayer constructor stub to Constructors section
- [ ] `docs/api/map.md` — no change
- [x] `docs/api/layers.md` — add SymbolLayer section after VectorTileLayer
- [ ] `docs/api/sources.md` — no change
- [ ] `docs/api/components.md` — no change
- [ ] `docs/recipes/` — no change
- [x] `README.md` — add SymbolLayer to layers table (line ~45)

## Verification Plan

### Automated Checks

```bash
pytest tests/test_symbol_layer.py -v
```

Tests:
1. `to_dict()` contains `"type": "symbol"`
2. `"source-layer"` present when `source_layer` is non-empty, absent otherwise
3. `icon_image` as string → verbatim in layout
4. `icon_image` as list (expression) → verbatim in layout
5. `text_field="name"` → `["get", "name"]` in layout; `text_field=None` → key absent
6. `icon_image=None` → `"icon-image"` key absent from layout

### Example Validation

```bash
cd Work/WB/atlas/source/firma-rr-zrr-map
python generate_map.py
```
Inspect generated HTML: three layers with `"type": "symbol"`.

### Browser Or Consumer Validation

Open generated HTML, zoom to Russia — Ф/Р/З icon markers should render with correct colors from PALETTE.

## Implementation Notes

- `SymbolLayer` inherits `BaseLayer`; `layer_type = "symbol"`.
- `to_dict()`: calls `super().to_dict()`, sets `base["type"] = "symbol"`, builds `layout` dict by filtering None values, builds `paint` dict similarly, adds `"source-layer"` only if non-empty.
- `text_field`: if plain string `"prop"` → auto-wrap to `["get", "prop"]`; if already a list → pass through; if None → omit.
- icon_color (SDF paint property) included but defaults to None (omitted) — non-SDF icons ignore it.
- `source_layer` defaults to `None` to allow use with GeoJSON sources.

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|--------------------------------------|
| `source_layer: Optional[str]` instead of required | Supports both VectorTile and GeoJSON sources | Making it required would break GeoJSON icon use-cases |
| `text_field` auto-wrap | MapLibre expects `["get", "prop"]` not a bare string for feature props | Requiring callers to write the expression is error-prone |
