# LLMaps Specs

This directory contains lightweight feature specifications for meaningful public changes to LLMaps.

The goal is simple: before changing the public API, first write down what is changing, why it matters, what files are affected, and how the change will be verified.

## When To Use A Feature Spec

Create a spec when a change affects one or more of these areas:

- `Map` parameters or methods
- layers, sources, or components
- expression helpers
- embedded, comparison, or storytelling behavior
- frontend-facing JS utilities documented in `LLM_CONTEXT.md`
- examples or docs that define recommended public usage

You usually do not need a spec for:

- typo fixes
- internal refactors with no behavior change
- docs-only wording updates
- narrow bug fixes with no public API impact

## Directory Layout

Each feature gets its own folder:

```text
specs/
  001-feature-name/
    spec.md
    plan.md
    tasks.md
    quickstart.md      # optional
    research.md        # optional
```

Use numeric prefixes so features are easy to reference in PRs and discussions.

## Recommended Workflow

1. Copy the templates from [specs/templates/](templates/).
2. Write `spec.md` first. Focus on behavior, requirements, edge cases, docs impact, and success criteria.
3. Write `plan.md`. Name the code paths, docs files, examples, and tests that will change.
4. Write `tasks.md`. Break work into a concrete execution sequence.
5. Implement only after the intent and verification plan are clear.

## Done Criteria For A Public API Change

A feature is not done until all applicable items below are true:

- code matches the behavior described in the spec
- [llmaps/LLM_CONTEXT.md](../llmaps/LLM_CONTEXT.md) is updated
- affected files in [docs/api/](../docs/api/) or [docs/recipes/](../docs/recipes/) are updated
- examples or consumer scenarios were validated when the usage pattern changed
- tests were added or updated for stable behavior where practical

## Templates

- [specs/templates/spec-template.md](templates/spec-template.md)
- [specs/templates/plan-template.md](templates/plan-template.md)
- [specs/templates/tasks-template.md](templates/tasks-template.md)