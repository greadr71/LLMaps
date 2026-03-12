# Feature Specification: Feature-state fade utilities

**Feature Folder**: `specs/003-feature-state-fade`  
**Created**: 2026-03-12  
**Status**: Draft

## Why This Change Exists

Users often build dynamic polygon highlighting with `setFeatureState`, but smooth fade-in/fade-out currently requires custom animation loops in consumer JS. This leads to duplicated code and inconsistent behavior across projects.

LLMaps already exposes frontend state utilities and Python expression helpers. Adding first-class fade utilities keeps the API ergonomic and reduces repeated low-level animation logic in downstream maps.

## User Scenarios And Testing

### User Story 1 - Animate feature-state transitions with built-in JS utility (Priority: P1)

A developer can call one public LLMaps JS function to animate feature-state values over time for a single feature, including cancellation/restart on repeated calls.

**Why this priority**: This is the core behavior that removes custom RAF boilerplate from user maps.

**Independent Test**: Generated map with `add_custom_js` invokes the utility for many polygons; visual check confirms smooth fade and no final abrupt color jump.

**Acceptance Scenarios**:

1. **Given** a source with `promote_id`, **When** the user calls `window.llmapsAnimateFeatureState("regions", fid, {active: true, fade_mix: 1}, {duration: 280})`, **Then** feature-state values interpolate smoothly and end at the target state.
2. **Given** an ongoing animation for the same feature, **When** a new animation call is made, **Then** the previous run is superseded and the new transition continues from the current interpolated value.

### User Story 2 - Build fade-ready expressions from Python helpers (Priority: P2)

A developer can build fill color/opacity expressions for fade behavior using documented helper functions instead of writing raw MapLibre arrays.

**Why this priority**: JS utility solves transition timing, but Python helpers make adoption straightforward and consistent.

**Independent Test**: Small script creates a `FillLayer` using new helpers and renders expected expression arrays in map config.

**Acceptance Scenarios**:

1. **Given** color stops and inactive color, **When** the user calls new fade expression helpers, **Then** helpers return serializable MapLibre expressions that use `coalesce(feature-state.fade_mix, active-fallback)`.

## Edge Cases

- Animation called for missing source or missing map instance should no-op safely.
- Invalid duration/easing should fall back to defaults.
- If `fade_mix` is missing, expressions should gracefully fall back to boolean `active`.
- Repeated calls during animation should not leak RAF handlers or keep stale state.

## Public API Impact

- **Affected API surface**: Frontend JS utilities + expression helpers.
- **New or changed symbols**:
  - `window.llmapsAnimateFeatureState(sourceId, featureId, targetState, options)`
  - `llmaps.expressions.feature_state_fade_mix(...)`
  - `llmaps.expressions.feature_state_fade_value(...)`
  - `llmaps.expressions.feature_state_fade_color(...)`
- **Backward compatibility**: Additive, backward compatible.
- **Migration note needed**: No.

## Documentation Impact

- [ ] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md)
- [ ] [docs/api/layers.md](../../docs/api/layers.md)
- [ ] [docs/recipes/feature-state-highlighting.md](../../docs/recipes/feature-state-highlighting.md)

## Verification Impact

- **Pytest coverage**: Add expression helper tests under `tests/` for output shapes and defaults.
- **Example validation**: Validate a feature-state highlighting example using new helpers and utility call pattern.
- **Consumer/browser validation**: Manual visual check of fade-in/fade-out and cancellation behavior.

## Requirements

### Functional Requirements

- **FR-001**: System MUST expose a public JS utility to animate feature-state on a feature by source/id.
- **FR-002**: System MUST support configurable duration/easing and predictable restart behavior on repeated calls.
- **FR-003**: System MUST expose Python expression helpers for fade mix/value/color patterns.
- **FR-004**: Helpers MUST produce serializable MapLibre expressions compatible with existing `FillLayer` usage.

### Non-Functional Requirements

- **NFR-001**: Frontend animation runtime MUST avoid per-feature RAF fan-out when many features animate simultaneously.
- **NFR-002**: API additions MUST be documented in `LLM_CONTEXT` and relevant docs pages.
- **NFR-003**: Existing public APIs and existing expression helpers MUST remain unchanged.

## Success Criteria

- **SC-001**: Developers can implement smooth region fade without writing custom animation loop logic.
- **SC-002**: Fade-out no longer exhibits abrupt final color jump when using provided fade expressions.
- **SC-003**: New API is fully documented and validated via tests/examples/manual check.
