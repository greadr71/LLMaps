# Tasks: [FEATURE NAME]

**Input**: `spec.md` and `plan.md` from `specs/[###-feature-name]/`

## Task Format

- Use checkboxes.
- Include exact file paths.
- Mark parallel-safe tasks with `[P]`.
- Prefer tasks grouped by user story when the feature has multiple independent outcomes.

## Phase 1: Intent And Validation Setup

- [ ] T001 Confirm affected API surface in `spec.md`
- [ ] T002 Confirm affected documentation targets in `plan.md`
- [ ] T003 Define verification path for tests, examples, and browser checks

## Phase 2: Tests And Examples First

- [ ] T004 Add or update pytest coverage in `tests/`
- [ ] T005 [P] Prepare or update runnable example in `examples/`
- [ ] T006 [P] Define optional consumer/browser validation path

## Phase 3: Implementation

- [ ] T007 Implement Python API changes in the relevant `llmaps/` modules
- [ ] T008 Implement generator, template, or frontend changes if needed
- [ ] T009 Keep serialization and public naming consistent with existing patterns

## Phase 4: Documentation Sync

- [ ] T010 Update `llmaps/LLM_CONTEXT.md`
- [ ] T011 [P] Update affected files under `docs/api/`
- [ ] T012 [P] Update affected recipes, README sections, or examples overview

## Phase 5: Validation

- [ ] T013 Run targeted tests
- [ ] T014 Run or inspect affected examples
- [ ] T015 Validate generated HTML or browser behavior when relevant
- [ ] T016 Confirm the implemented behavior matches `spec.md`

## Delivery Notes

- Stop after Phase 2 and re-check the plan if the intended public behavior changed.
- Treat docs drift as an incomplete feature, not as follow-up work.
- If the change is breaking, add migration notes before considering the task list complete.