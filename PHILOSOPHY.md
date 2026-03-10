# LLMaps Philosophy

LLMaps is a **Python library** for creating interactive web maps, designed for LLM-assisted development and vibe coding. This document describes the concept, design principles, and how it compares to alternatives.

---

## Concept

**LLMaps** — A Python library for creating interactive maps, optimized for LLM-assisted development.

- **Library, not framework:** It does not dictate application architecture. You use it inside your code; it does not wrap your app.
- **Single responsibility:** Build a map configuration, render it to standalone HTML. No server, no backend required for the default embedded mode.
- **Declarative API:** You describe *what* the map should show (center, zoom, layers, components); the library handles *how* (MapLibre GL JS, Jinja2, templates).

---

## Vibe Coding and LLM-First Design

**Vibe coding** here means: writing code with the help of an LLM (e.g. in an IDE or chat). The API is built so that:

1. **Predictable names** — `Map`, `CircleLayer`, `FillLayer`, `FileSource`, `Legend`, `Popup`, `Controls`, `Search`. No magic or overloaded meanings.
2. **Stable contracts** — Constructors and methods have clear signatures; `to_dict()` produces a serialisable config. This makes it easy for an LLM to suggest correct code.
3. **Composable pieces** — One map, many layers, many components. Add what you need: `map.add_layer(...).add_component(...).save(...)`.
4. **Documentation as product** — `get_llm_context()` yields a compact reference (signatures, scenarios, JS utilities) for LLM-assisted code; humans use `docs/api/`.

The goal is: *fewer edits, fewer bugs* when generating map code with an LLM.

---

## Design Principles

1. **LLM-first** — Structure and naming are chosen so that both humans and LLMs can find and use the right abstraction quickly (see `get_llm_context()` / LLM_CONTEXT and `docs/api/`).
2. **Component-based** — Clear abstractions: `Map`, `Layer`, `Source`, `Component`, `Optimizer`. Each does one job and combines with others.
3. **KISS** — Configuration via parameters, dataclasses, or dicts. Complex logic (H3 aggregation, compression, comparison mode) lives inside the library, not in user code.
4. **Don’t reinvent the wheel** — Build on proven tools: MapLibre GL JS for the map, Jinja2 for HTML, optional geopandas/h3/geobuf for data and optimizations. Use official plugins (e.g. maplibre-gl-compare) where they fit.
5. **Extensibility** — Well-defined extension points: new layer types, new sources, new components, without rewriting the core.
6. **English only** — Code, comments, docs, and UI strings are in English for a global, open-source audience.

---

## Comparison with Alternatives

| Criterion | Kepler.gl | Folium / ipyleaflet | Custom MapLibre/Leaflet | **LLMaps** |
|-----------|-----------|---------------------|--------------------------|------------|
| **Ready-made components** | Limited by UI | Few map primitives | None | Full set: layers, legend, popup, search, controls |
| **LLM-friendly** | No | Partial (verbose) | Depends on custom code | Yes: index, tags, clear API |
| **H3 / aggregation** | Yes | No (manual) | Manual | Yes (H3Layer) |
| **Embedded (file://)** | No | Often needs server | Manual | Yes (embedded=True) |
| **Comparison (before/after)** | No | No | Manual | Yes (enable_comparison) |
| **Single HTML output** | No | Possible | Manual | Yes (save/to_html) |
| **Customization** | Limited by UI | Good | Full | Full (config + templates) |
| **No backend** | No | Often | Possible | Yes (embedded mode) |

**When to use LLMaps:** You want a single Python API to produce a standalone interactive map (especially with embedded data), with minimal boilerplate and good support for LLM-generated code. You are fine with MapLibre GL JS on the frontend and optional dependencies (geopandas, h3, geobuf) for advanced features.

**When to choose something else:** You need a full GIS UI (Kepler.gl), tight Jupyter integration only (Folium/ipyleaflet), or a fully custom stack (raw MapLibre/Leaflet and your own backend).

---

## Architecture in Brief

- **Python API** — `Map`, layers (`CircleLayer`, `FillLayer`, `H3Layer`, `VectorTileLayer`), sources (`FileSource`, `ApiSource`, `VectorTileSource`), components (`Legend`, `Popup`, `Search`, `Controls`).
- **Config** — Everything reduces to a serialisable dict (`to_dict()`); no framework magic.
- **Output** — The generator (`llmaps.core.generator`) turns that config into one HTML file (with inline or linked JS/CSS). Embedded mode inlines GeoJSON (optionally Geobuf+Gzip).
- **Frontend** — MapLibre GL JS + plugins (e.g. comparison). Templates live under `llmaps/templates/`.

---

## Summary

LLMaps combines a small, predictable Python API with a component-based design and an LLM-oriented doc set. It targets developers who want to generate or maintain map code quickly (including with LLMs) and ship a single HTML map without a backend. The philosophy is: **simple to call, explicit in structure, and built on solid open-source building blocks.**

For public API development governance and review rules, see [CONSTITUTION.md](CONSTITUTION.md).
