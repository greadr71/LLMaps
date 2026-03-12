# Implementation Plan: Feature-state fade utilities

**Feature Folder**: `specs/003-feature-state-fade`  
**Date**: 2026-03-12  
**Spec**: [spec.md](./spec.md)

## Summary

Add a built-in frontend utility for animated `setFeatureState` transitions and add Python expression helpers that make fade-ready `fill-color` / `fill-opacity` expressions easy to compose. Keep the change additive and backward compatible.

## Technical Context

- **Language/Version**: Python 3.10+
- **Project Type**: Library
- **Core Stack**: `jinja2`, `pandas`, `geopandas`, `shapely`, `MapLibre GL JS`
- **Testing**: `pytest`, docs recipe validation, manual browser checks
- **Constraints**: serializable API output, public API clarity, docs parity

## Constitution Check

Use [CONSTITUTION.md](../../CONSTITUTION.md) as the source of truth.

- [x] Article I (Public API First): public API scope is explicitly identified.
- [x] Article I (Public API First): backward compatibility impact is described.
- [x] Article III (Documentation Parity): documentation impact is named before implementation starts.
- [x] Article IV (Verification Before Merge): verification path exists before coding starts.
- [x] Article VI (Simplicity Over Process): the design uses the simplest change that fits the current repo structure.

## Affected Code Paths

- [x] [llmaps/expressions.py](../../llmaps/expressions.py)
- [x] [llmaps/templates/js/sources.js.j2](../../llmaps/templates/js/sources.js.j2)

## Affected Documentation

- [x] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md)
- [x] [docs/api/layers.md](../../docs/api/layers.md)
- [x] [docs/recipes/feature-state-highlighting.md](../../docs/recipes/feature-state-highlighting.md)

## Verification Plan

### Automated Checks

- Add/extend tests in `tests/` for new expression helpers:
  - default output shape
  - custom keys/colors/stops
  - backward-compatible fallback behavior

### Example Validation

- Verify that recipe snippets produce valid config with new helpers.
- Ensure no existing expression helper examples are broken.

### Browser Or Consumer Validation

- Manual check of generated map:
  - smooth fade-in and fade-out
  - no abrupt final color snap
  - repeated animation calls supersede previous transition cleanly

## Implementation Notes

- JS utility lives near existing frontend utility functions in `sources.js.j2`.
- Use one animation scheduler for active animations to avoid RAF fan-out.
- New Python helpers are additive and return pure list expressions.

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|--------------------------------------|
| Shared animation loop for active states | Keeps runtime stable under many simultaneous feature updates | One RAF per feature caused visible jitter and unnecessary scheduling overhead |
