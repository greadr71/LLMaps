# Feature Specification: [FEATURE NAME]

**Feature Folder**: `specs/[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft

## Why This Change Exists

[Explain the user or developer problem in plain language. Focus on the behavior and value, not the implementation details.]

## User Scenarios And Testing

### User Story 1 - [Primary Outcome] (Priority: P1)

[Describe the most important usage outcome for this change. For llmaps, this is often a developer story such as adding a new layer, source, component, or map capability.] 

**Why this priority**: [Why this is the MVP slice]

**Independent Test**: [How this outcome can be validated with a runnable example, test, or generated HTML behavior]

**Acceptance Scenarios**:

1. **Given** [starting context], **When** [action], **Then** [expected outcome]
2. **Given** [starting context], **When** [action], **Then** [expected outcome]

### User Story 2 - [Secondary Outcome] (Priority: P2)

[Optional follow-up outcome]

**Why this priority**: [Why it comes after P1]

**Independent Test**: [How to validate independently]

**Acceptance Scenarios**:

1. **Given** [starting context], **When** [action], **Then** [expected outcome]

## Edge Cases

- What happens when required inputs are missing or invalid?
- What happens in embedded mode?
- What happens if the feature interacts with `feature_state` or `promote_id`?
- How should existing examples or generated HTML behave if the feature is absent?

## Public API Impact

- **Affected API surface**: [Map / layer / source / component / expression / frontend JS utility]
- **New or changed symbols**: [List classes, methods, parameters, helper functions]
- **Backward compatibility**: [Compatible / breaking / additive with caveats]
- **Migration note needed**: [Yes/No and why]

## Documentation Impact

List every documentation artifact that must change if this feature is implemented.

- [ ] [llmaps/LLM_CONTEXT.md](../../llmaps/LLM_CONTEXT.md)
- [ ] [docs/api/map.md](../../docs/api/map.md)
- [ ] [docs/api/layers.md](../../docs/api/layers.md)
- [ ] [docs/api/sources.md](../../docs/api/sources.md)
- [ ] [docs/api/components.md](../../docs/api/components.md)
- [ ] [docs/recipes/](../../docs/recipes/)
- [ ] [README.md](../../README.md)
- [ ] [examples/README.md](../../examples/README.md)

Keep only the items that apply.

## Verification Impact

- **Pytest coverage**: [What new or updated tests are needed in `tests/`]
- **Example validation**: [Which example(s) should be updated or rerun]
- **Consumer/browser validation**: [Optional external checks, such as llmaps_instances or manual browser verification]

## Requirements

### Functional Requirements

- **FR-001**: System MUST [public behavior]
- **FR-002**: System MUST [public behavior]
- **FR-003**: Users MUST be able to [developer-facing usage outcome]

### Non-Functional Requirements

- **NFR-001**: The API MUST remain explicit and serializable.
- **NFR-002**: The change MUST be documented in all affected public docs.
- **NFR-003**: The feature MUST have a reproducible validation path.

## Success Criteria

- **SC-001**: [Measurable or observable outcome]
- **SC-002**: [Documentation and example parity outcome]
- **SC-003**: [Verification outcome]