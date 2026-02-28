# LLMaps

![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MapLibre](https://img.shields.io/badge/frontend-MapLibre%20GL%20JS-orange)

**A Python library for creating interactive web maps, optimized for LLM-assisted development.**

Encapsulates best practices for interactive web map development behind a predictable, composable API — so both you and your LLM produce correct code on the first try. Outputs a single HTML file powered by MapLibre GL JS.

<details>
<summary>Table of Contents</summary>

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Built With](#built-with)
- [Comparison with Alternatives](#comparison-with-alternatives)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Tile Providers](#tile-providers)
- [License](#license)
- [Contact](#contact)
- [Contributing](#contributing)

</details>

## Features

- **Declarative API** — composable `Map` + layers + sources + components. Describe *what* the map should show; the library handles *how*.
- **Single HTML output** — standalone file with MapLibre GL JS; works via `file://` when data is embedded.
- **Embedded mode** — inline GeoJSON (optionally Geobuf + Gzip) so you can share one file.
- **Comparison mode** — before/after slider using the MapLibre compare plugin.
- **Feature-state expressions** — GPU-efficient dynamic styling (`fill_color`, `opacity`) via `setFeatureState`.
- **Extensible** — custom JS/CSS/HTML injection, `embed_data()` for arbitrary JSON.
- **Built-in attribution** — automatic LLMaps branding with GitHub link (customizable or removable).
- **LLM-friendly** — predictable names, stable contracts; use `get_llm_context()` for a compact reference in chat.

**Available building blocks:**

| Category | Classes |
|----------|---------|
| **Layers** | `CircleLayer`, `FillLayer`, `H3Layer`, `VectorTileLayer` |
| **Sources** | `FileSource`, `ApiSource`, `VectorTileSource` |
| **Components** | `Legend`, `Popup`, `Sidebar`, `Search`, `FeatureSearch`, `Controls`, `BasemapSwitcher`, `Storytelling` |

## Installation

```bash
pip install llmaps
```

**Cursor / Claude Code** — both support the [Agent Skills](https://agentskills.io) standard. Copy the repo's `cursor-skill` folder so the AI has full context when generating map code:

| Tool | Skills path |
|------|-------------|
| Cursor | `~/.cursor/skills/llmaps/SKILL.md` |
| Claude Code | `~/.claude/skills/llmaps/SKILL.md` |

On Windows use `%USERPROFILE%\` instead of `~/`. Create the folders if needed. The skill is picked up automatically on next launch. If you use either tool with this skill, you can skip the step below.

**Context for other LLM chats:** Run once in your project directory, then attach `llmaps_context.md` to the chat (e.g. `@llmaps_context.md` in Cursor):

```bash
python -c "import llmaps; open('llmaps_context.md','w').write(llmaps.get_llm_context())"
```

## Quick Start

```python
from llmaps import Map
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource
from llmaps.components import Legend, Popup, Controls

source = FileSource(id="points", path="data/points.geojson")
layer = CircleLayer(
    id="points-layer",
    source=source,
    radius=6,
    color="#3182bd",
    opacity=0.8,
)

m = Map(center=[10.0, 50.0], zoom=4, title="My Map", tiles="osm")
m.add_layer(layer)
m.add_component(Legend(layer_labels={"points-layer": "Points"}))
m.add_component(Popup(fields=["name", "value"], field_labels={"name": "Name", "value": "Value"}))
m.add_component(Controls(zoom=True, scale=True))

m.auto_extent()
m.save("my_map.html")
```

## Examples

Explore interactive maps showcasing key features and capabilities: [**LLMaps Examples Gallery**](https://greadr71.github.io/LLMaps/examples/)

Real-world examples with source code:

| Example | Features | Data |
|---------|----------|------|
| [Paris Cafes & Restaurants](examples/cafes/) | CircleLayer, Search, FeatureSearch, BasemapSwitcher, Popup, Sidebar | OpenStreetMap Overpass |
| [World Population](examples/world_population/) | FillLayer, feature-state styling, Jenks classification, color ramps | Natural Earth |
| [Earthquakes](examples/earthquakes/) | H3Layer, animated H3 heatmap, temporal filtering | USGS Earthquake API |

## Built With

- [MapLibre GL JS](https://maplibre.org/) — frontend map rendering
- [Jinja2](https://jinja.palletsprojects.com/) — HTML template engine
- Optional: [H3](https://h3geo.org/), [GeoPandas](https://geopandas.org/), [Geobuf](https://github.com/pygeobuf/pygeobuf)

## Comparison with Alternatives

| **Criterion** | **Kepler.gl** | **Folium / ipyleaflet** | **Custom MapLibre/Leaflet** | **LLMaps** |
|---------------|---------------|-------------------------|-----------------------------|------------|
| **Ready-made components** | ⚠️ Limited by UI | ⚠️ Few primitives | ❌ | ✅ Full set: layers, legend, popup, sidebar, search, controls |
| **LLM-friendly** | ❌ | ⚠️ Partial | ⚠️ Depends on code | ✅ Clear API, stable contracts |
| **H3 / aggregation** | ✅ | ❌ | ⚠️ Manual | ✅ H3Layer |
| **Embedded (file://)** | ❌ | ⚠️ Often needs server | ⚠️ Manual | ✅ `embedded=True` |
| **Comparison (before/after)** | ❌ | ❌ | ⚠️ Manual | ✅ `enable_comparison` |
| **Single HTML output** | ❌ | ✅ Possible | ⚠️ Manual | ✅ `save` / `to_html` |
| **Customization** | ⚠️ Limited | ✅ Good | ✅ Full | ✅ Full (config + templates + custom JS/CSS) |
| **Extensibility** | ⚠️ Limited by UI | ✅ Good (plugins, custom HTML/JS) | ✅ Full | ✅ Full (custom JS/CSS/HTML, `embed_data()`, templates) |
| **No backend** | ❌ | ✅ Often | ⚠️ Possible | ✅ Embedded mode |

**When to use LLMaps:** You want a single Python API to produce a standalone interactive map (especially with embedded data), with minimal boilerplate and good support for LLM-generated code.

**When to choose something else:** You need a full GIS UI (Kepler.gl), tight Jupyter-only integration (Folium/ipyleaflet), or a fully custom frontend stack (raw MapLibre/Leaflet with your own backend).

## Architecture

```
Python API  →  Config (to_dict())  →  HTML (Jinja2)  →  Frontend (MapLibre GL JS + plugins)
```

Everything reduces to a serializable dict — no framework magic. The generator turns that config into one HTML file with inline or linked JS/CSS. See [PHILOSOPHY.md](PHILOSOPHY.md) for design principles and rationale.

## Documentation

- **LLM context** — run `python -c "import llmaps; open('llmaps_context.md','w').write(llmaps.get_llm_context())"` and use @llmaps_context.md in chat for a compact API reference.
- **[PHILOSOPHY.md](PHILOSOPHY.md)** — Concept, design principles, comparison with alternatives.
- **[docs/api/](docs/api/)** — Map, layers, sources, components (parameters and examples).
- **[docs/recipes/](docs/recipes/)** — Heatmap, comparison, embedded map, feature-state highlighting.

## Tile Providers

Use the `tiles` argument when creating the map:

| Key | Provider | Attribution |
|-----|----------|-------------|
| `"osm"` | OpenStreetMap (default) | © OpenStreetMap contributors |
| `"carto-light"` | Carto Light | © OpenStreetMap contributors, © CARTO |
| `"carto-dark"` | Carto Dark | © OpenStreetMap contributors, © CARTO |
| `"yandex"` | Yandex Maps | © Yandex Maps |
| `"2gis"` | 2GIS | © 2GIS |

## License

MIT. See [LICENSE](LICENSE).

## Contact

**Sergey Abramov**

[![Telegram](https://img.shields.io/badge/Telegram-@sergey__abr-2CA5E0?logo=telegram&logoColor=white)](https://t.me/sergey_abr)
[![Email](https://img.shields.io/badge/Email-sergey.abr71@gmail.com-D14836?logo=gmail&logoColor=white)](mailto:sergey.abr71@gmail.com)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
