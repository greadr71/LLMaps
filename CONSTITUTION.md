# LLMaps Constitution

## Core Principles

### I. Public API First

LLMaps is a library with a public Python API. Any change to `Map`, layers, sources, components, expression helpers, embedded/comparison behavior, or frontend-facing JS utilities MUST be treated as a public contract change.

Backward compatibility is the default. Breaking changes require explicit justification, a migration note, and a coordinated update of documentation and examples.

### II. Serializable, Predictable Contracts

Public objects MUST remain explicit, composable, and serializable through `to_dict()` or equivalent config output. Naming should stay predictable for humans and LLMs: clear class names, stable parameter names, and minimal hidden behavior.

New abstractions are allowed only when they simplify the public API or reduce repeated implementation complexity without obscuring the contract.

### III. Documentation Parity Is Mandatory

For any public API change, code is not considered complete until documentation is updated. At minimum, contributors MUST update the affected files from the documentation matrix in [CONTRIBUTING.md](CONTRIBUTING.md), especially [llmaps/LLM_CONTEXT.md](llmaps/LLM_CONTEXT.md) and the relevant files under [docs/api/](docs/api/).

Documentation is part of the product, not post-work cleanup.

### IV. Verification Before Merge

Public behavior changes MUST define how they are verified before implementation is considered complete. Verification can include pytest coverage, example validation, or consumer-side browser checks when frontend behavior is involved.

Tests are preferred for stable behavior. Examples are required when a feature changes user-facing map capabilities or recommended usage patterns.

### V. Examples Are Regression Assets

Examples are not marketing-only artifacts. They are executable demonstrations of intended library usage and should be used to validate that important workflows remain functional.

When a change affects a documented usage pattern, at least one example or consumer scenario MUST be reviewed or updated.

### VI. Simplicity Over Process

LLMaps uses spec-driven development as a lightweight planning aid for meaningful public changes, not as ceremony for every commit. Small internal refactors, typo fixes, or isolated implementation cleanups do not require a feature spec unless they change behavior or public contracts.

The process should stay brownfield-friendly: fit the repository as it exists today, avoid new infrastructure unless it clearly reduces missed updates and review churn.

## Scope And Constraints

- Feature specs are REQUIRED for meaningful public API changes.
- Feature specs are OPTIONAL for internal refactors, bug fixes with no API change, and docs-only updates.
- The canonical implementation paths remain the existing repository structure: [llmaps/](llmaps/), [docs/api/](docs/api/), [docs/recipes/](docs/recipes/), [examples/](examples/), and [tests/](tests/).
- Consumer-side integration checks may live outside this repository when they exercise generated HTML in a browser.

## Development Workflow

For a meaningful public API change:

1. Create a feature folder under [specs/](specs/) using the next numeric prefix.
2. Write [spec.md](specs/README.md) using the llmaps template: describe user/developer value, API behavior, edge cases, and success criteria.
3. Write `plan.md`: map the feature to concrete code paths, docs impact, examples, and verification strategy.
4. Write `tasks.md`: break the work into docs intent, tests/examples, implementation, docs sync, and validation.
5. Implement the change.
6. Verify the resulting code, docs, examples, and tests are in sync.

## Governance

This constitution guides public API development and review. [CONTRIBUTING.md](CONTRIBUTING.md) contains the operational checklist, while this document defines the non-negotiable principles behind it.

Amendments require:

- an explicit rationale,
- alignment with [PHILOSOPHY.md](PHILOSOPHY.md),
- and updates to affected workflow documents.

**Version**: 1.0.0 | **Ratified**: 2026-03-08 | **Last Amended**: 2026-03-08