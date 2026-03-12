# Tasks: Feature-state fade utilities

**Input**: `spec.md` and `plan.md` from `specs/003-feature-state-fade/`

## Phase 1: Intent And Validation Setup

- [x] T001 Confirm affected API surface in `specs/003-feature-state-fade/spec.md`
- [x] T002 Confirm affected documentation targets in `specs/003-feature-state-fade/plan.md`
- [x] T003 Define verification path for tests, examples, and browser checks

## Phase 2: Tests And Examples First

- [ ] T004 Add or update pytest coverage for expression helpers in `tests/`
- [ ] T005 [P] Update recipe snippets in `docs/recipes/feature-state-highlighting.md`
- [ ] T006 [P] Define browser validation steps for animated transitions

## Phase 3: Implementation

- [ ] T007 Implement Python helper functions in `llmaps/expressions.py`
- [ ] T008 Implement frontend utility in `llmaps/templates/js/sources.js.j2`
- [ ] T009 Keep naming/serialization aligned with existing public API patterns

## Phase 4: Documentation Sync

- [ ] T010 Update `llmaps/LLM_CONTEXT.md`
- [ ] T011 [P] Update `docs/api/layers.md`
- [ ] T012 [P] Update `docs/recipes/feature-state-highlighting.md`

## Phase 5: Validation

- [ ] T013 Run targeted tests for `llmaps/expressions.py`
- [ ] T014 Inspect updated docs snippets for consistency
- [ ] T015 Validate generated HTML/browser behavior for fade-in/fade-out and restart semantics
- [ ] T016 Confirm implemented behavior matches `specs/003-feature-state-fade/spec.md`
