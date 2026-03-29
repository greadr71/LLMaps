# Tasks: SymbolLayer

**Input**: `spec.md` and `plan.md` from `specs/004-symbol-layer/`

## Phase 1: Intent And Validation Setup

- [x] T001 Confirm affected API surface in `spec.md`
- [x] T002 Confirm affected documentation targets in `plan.md`
- [x] T003 Define verification path for tests, examples, and browser checks

## Phase 2: Tests And Examples First

- [ ] T004 Add `tests/test_symbol_layer.py` with 6 test cases (see plan.md)
- [ ] T005 [P] Prepare consumer example: update `generate_map.py` + `map.js`

## Phase 3: Implementation

- [ ] T006 Create `llmaps/layers/symbol.py`
- [ ] T007 Update `llmaps/layers/__init__.py`

## Phase 4: Documentation Sync

- [ ] T008 Update `llmaps/LLM_CONTEXT.md` — add SymbolLayer constructor stub
- [ ] T009 [P] Update `docs/api/layers.md` — add SymbolLayer section
- [ ] T010 [P] Update `README.md` — add SymbolLayer to layers table

## Phase 5: Validation

- [ ] T011 Run `pytest tests/test_symbol_layer.py -v`
- [ ] T012 Run `python generate_map.py` in firma-rr-zrr-map
- [ ] T013 Confirm generated HTML has `"type": "symbol"` layers
