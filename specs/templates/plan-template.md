# Implementation Plan: [FEATURE NAME]

**Feature Folder**: `specs/[###-feature-name]`  
**Date**: [DATE]  
**Spec**: [link to spec.md]

## Summary

[Summarize the change, the API surface involved, and the intended verification strategy.]

## Technical Context

- **Language/Version**: Python 3.10+
- **Project Type**: Library
- **Core Stack**: `jinja2`, `pandas`, `geopandas`, `shapely`, `MapLibre GL JS`
- **Testing**: `pytest`, example validation, optional browser checks
- **Constraints**: preserve public API clarity, docs parity, serializable config output

## Constitution Check

- [ ] Public API scope is explicitly identified.
- [ ] Backward compatibility impact is described.
- [ ] Documentation impact is named before implementation starts.
- [ ] Verification path exists before coding starts.
- [ ] The design uses the simplest change that fits the current repo structure.

## Affected Code Paths

Keep only the paths that apply.

- [ ] [llmaps/map.py](../../llmaps/map.py)
- [ ] [llmaps/layers/](../../llmaps/layers)
- [ ] [llmaps/sources/](../../llmaps/sources)
- [ ] [llmaps/components/](../../llmaps/components)
- [ ] [llmaps/expressions.py](../../llmaps/expressions.py)
- [ ] [llmaps/core/generator.py](../../llmaps/core/generator.py)
- [ ] [llmaps/templates/](../../llmaps/templates)

## Affected Documentation

Keep only the paths that apply.

- [ ] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md)
- [ ] [docs/api/map.md](../../docs/api/map.md)
- [ ] [docs/api/layers.md](../../docs/api/layers.md)
- [ ] [docs/api/sources.md](../../docs/api/sources.md)
- [ ] [docs/api/components.md](../../docs/api/components.md)
- [ ] [docs/recipes/](../../docs/recipes)
- [ ] [README.md](../../README.md)
- [ ] [examples/README.md](../../examples/README.md)

## Verification Plan

### Automated Checks

- [Describe pytest coverage to add or update]

### Example Validation

- [Describe example directories or scripts to rerun]

### Browser Or Consumer Validation

- [Optional: describe llmaps_instances, manual map verification, or generated HTML checks]

## Implementation Notes

- [Describe data flow and serialization changes]
- [Describe frontend template or JS implications if any]
- [Describe migration or deprecation handling if any]

## Complexity Tracking

Fill this section only if the change introduces unusual complexity.

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|--------------------------------------|
| [example] | [reason] | [reason] |