# Feature Specification: Dashboard Primitives

**Feature Folder**: `specs/001-dashboard-primitives`  
**Created**: 2026-03-08  
**Status**: Complete

## Why This Change Exists

LLMaps already supports transient UI such as popups, sidebars, legends, and storytelling panels, but it lacks a reusable way to attach persistent dashboard UI to a map. Consumers currently need ad hoc `add_custom_html()` and `add_custom_js()` glue for filters, status panels, and persistent metric blocks.

This change introduces a first-class dashboard component so developers can declare a persistent map overlay with a stable Python API, serializable config, and minimal frontend hooks for custom logic.

## User Scenarios And Testing

### User Story 1 - Add A Persistent Dashboard Panel (Priority: P1)

A developer can attach a dashboard panel to a map using `Map.add_component()` and control its position, size, title, and initial HTML content.

**Why this priority**: This is the smallest reusable public slice. Without a stable container component, filter controls and richer widgets have no consistent host.

**Independent Test**: Generate a runnable example map and verify that the dashboard panel is rendered without custom HTML injection.

**Acceptance Scenarios**:

1. **Given** a `Dashboard` component attached to a map, **When** the map HTML is generated, **Then** the config contains a `dashboard` component entry and the panel is rendered in the configured position.
2. **Given** a `Dashboard` configured as collapsible, **When** the user toggles the panel, **Then** it switches between expanded and collapsed states without affecting the map layers.

### User Story 2 - Add Declarative Filter Controls (Priority: P1)

A developer can declare a lightweight filter bar inside the dashboard using serializable filter definitions such as select, date, and text inputs.

**Why this priority**: Persistent filters are a core dashboard use case and were the main requirement for the first implementation wave.

**Independent Test**: Generate a runnable example and verify that changing a filter emits a stable frontend event with dashboard and filter identifiers.

**Acceptance Scenarios**:

1. **Given** a dashboard with declared filters, **When** the page loads, **Then** each filter is rendered with its configured label, default value, and input type.
2. **Given** a rendered dashboard filter, **When** the user changes its value, **Then** a frontend event is emitted with the dashboard id, filter id, and current state snapshot.

### User Story 3 - Update Dashboard Content From Custom JS (Priority: P2)

A developer can use a small JS bridge to update dashboard content and read filter state from custom JS without directly manipulating DOM selectors.

**Why this priority**: This keeps the first release useful for consumer code without overcommitting to a broader widget framework.

**Independent Test**: Use custom JS in an example to update the dashboard HTML when a filter changes.

**Acceptance Scenarios**:

1. **Given** a rendered dashboard, **When** consumer JS calls a documented update helper, **Then** the dashboard content updates without rebuilding the map.

## Edge Cases

- If `dashboard_id` is omitted, the system should use a predictable default id.
- If filters are empty, the dashboard should still render its content area.
- If `content_html` is empty, the dashboard should render an empty content region without failing.
- In embedded mode, the dashboard should behave the same because it relies only on generated HTML/JS.
- If the dashboard component is absent, existing generated HTML and examples must remain unchanged.
- The component must not interfere with existing `Sidebar`, `Popup`, `Legend`, or `Storytelling` behavior.

## Public API Impact

- **Affected API surface**: component, frontend JS utility
- **New or changed symbols**: `llmaps.components.Dashboard`, frontend helpers `window.llmapsDashboardSetContent`, `window.llmapsDashboardSetTitle`, `window.llmapsDashboardGetState`
- **Backward compatibility**: additive
- **Migration note needed**: No, because there is no breaking change

## Documentation Impact

- [x] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md)
- [x] [docs/api/components.md](../../docs/api/components.md)
- [x] [examples/README.md](../../examples/README.md)

## Verification Impact

- **Pytest coverage**: add unit tests for `Dashboard.to_dict()`
- **Example validation**: add and run a new dashboard example
- **Consumer/browser validation**: inspect generated example HTML in a browser and verify filter events update dashboard content

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a `Dashboard` component that can be attached via `Map.add_component()`.
- **FR-002**: `Dashboard` MUST remain explicit and serializable via `to_dict()`.
- **FR-003**: `Dashboard` MUST support a persistent content region populated from `content_html`.
- **FR-004**: `Dashboard` MUST support declarative filter definitions for at least `select`, `date`, and `text` inputs.
- **FR-005**: The generated frontend MUST emit a stable event when dashboard filters change.
- **FR-006**: The generated frontend MUST expose a minimal JS bridge for reading filter state and updating dashboard title/content.

### Non-Functional Requirements

- **NFR-001**: The API MUST remain explicit and serializable.
- **NFR-002**: The change MUST be documented in all affected public docs.
- **NFR-003**: The feature MUST have a reproducible validation path.
- **NFR-004**: Dashboard styles MUST be namespaced to avoid collisions with existing components.

## Success Criteria

- **SC-001**: A developer can generate a map with a dashboard using only LLMaps public Python API.
- **SC-002**: Documentation and LLM context mention the new component and JS bridge.
- **SC-003**: Targeted unit tests pass and the dashboard example renders and responds to filter changes.