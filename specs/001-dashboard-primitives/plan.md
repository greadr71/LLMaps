# Implementation Plan: Dashboard Primitives

**Feature Folder**: `specs/001-dashboard-primitives`  
**Date**: 2026-03-08  
**Spec**: [spec.md](./spec.md)

## Summary

Add a first-class `Dashboard` component to LLMaps as a persistent, serializable overlay panel for map dashboards. The first implementation includes a dashboard container, optional collapsible behavior, declarative filter controls, a content HTML slot, minimal frontend helper functions, an example, and documentation updates.

## Technical Context

- **Language/Version**: Python 3.10+
- **Project Type**: Library
- **Core Stack**: `jinja2`, `pandas`, `geopandas`, `shapely`, `MapLibre GL JS`
- **Testing**: `pytest`, example validation, manual browser checks
- **Constraints**: preserve public API clarity, docs parity, serializable config output, avoid interfering with existing component behavior

## Constitution Check

Source: [CONSTITUTION.md](../../CONSTITUTION.md)

- [x] Article I (Public API First): public API scope is explicitly identified.
- [x] Article I (Public API First): backward compatibility impact is described.
- [x] Article III (Documentation Parity): documentation impact is named before implementation starts.
- [x] Article IV (Verification Before Merge): verification path exists before coding starts.
- [x] Article VI (Simplicity Over Process): the design uses the simplest change that fits the current repo structure.

## Affected Code Paths

- [x] [llmaps/components/](../../llmaps/components)
- [x] [llmaps/templates/](../../llmaps/templates)

## Affected Documentation

- [x] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md)
- [x] [docs/api/components.md](../../docs/api/components.md)
- [x] [examples/README.md](../../examples/README.md)

## Verification Plan

### Automated Checks

- Add `tests/test_dashboard_component.py` for `Dashboard.to_dict()` and default serialization behavior.

### Example Validation

- Add `examples/dashboard/build_map.py` and generate example HTML to confirm rendering and JS bridge behavior.

### Browser Or Consumer Validation

- Open the generated dashboard example and verify panel rendering, collapse toggle, filter event emission, and content updates from custom JS.

## Implementation Notes

- The Python side should mirror existing component patterns with a dataclass plus `to_dict()`.
- The frontend should extend `components.js.j2` with a dedicated dashboard branch and expose only minimal helpers on `window`.
- The initial version should not introduce a generic chart framework, async data layer, or domain-specific state machine.
- Styles should be added to the existing base stylesheet with `.llmaps-dashboard-*` prefixes.

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|--------------------------------------|
| Keep filters nested inside `Dashboard` config | Smaller public surface for v1 | Separate `FilterBar` component would add another top-level public contract too early |
| Use minimal global JS helpers | Makes custom JS integration practical | Direct DOM manipulation would create unstable consumer contracts |