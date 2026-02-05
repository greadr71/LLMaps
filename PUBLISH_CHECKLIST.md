# Pre-publication checklist (GitHub + PyPI)

Use this list before publishing LLMaps to GitHub and PyPI.

## Content and branding

- [ ] **No internal/proprietary brands** — No company-specific or internal project names in code, docs, or examples.
- [ ] **No internal URLs** — No pgtile-storage or other internal endpoints; tile URLs for Yandex/2GIS are placeholders.
- [ ] **Neutral examples** — Examples use synthetic data, museums, parks, regions (no company-specific or NDA data).
- [ ] **Public data only** — Example data is either generated in-script or from public sources (OSM, Natural Earth, etc.).

## Repository

- [ ] **English only** — Code, comments, documentation, examples, and UI strings are in English.
- [ ] **README in English** — README.md describes the library, installation, quick start, and links to docs.
- [ ] **Git history** — Repository history started from scratch for the LLMaps project (no copied history).

## Legal and metadata

- [ ] **LICENSE (MIT)** — LICENSE file present with MIT text and your name (e.g. "Copyright (c) 2026 Sergey Abramov").
- [ ] **pyproject.toml** — Correct `name`, `version`, `description`, `authors`, `license`, `keywords`, `classifiers`, `[project.urls]` (Homepage, Documentation, Source, Issues).

## Documentation

- [ ] **API_GUIDE.md** — LLM-friendly index with Keywords, Related, Alternatives; aligned with public API.
- [ ] **PHILOSOPHY.md** — Concept, design principles, comparison with alternatives, vibe coding.
- [ ] **docs/api/** — map.md, layers.md, sources.md, components.md up to date.
- [ ] **docs/recipes/** — heatmap.md, comparison.md, embedded-map.md with working examples.
- [ ] **CONTRIBUTING.md** — Contribution guidelines and scope.

## Publishing

- [ ] **GitHub** — Create repo, push, set description and topics.
- [ ] **PyPI** — `pip install build twine`, `python -m build`, `twine upload dist/*` (or use GitHub Actions).
- [ ] **Optional:** Update `Documentation` URL in pyproject.toml to point to GitHub Pages or docs site when available.
