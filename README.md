# LLMaps

![Python](https://img.shields.io/badge/python-%3E%3D3.9-blue)
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
- [Contributing](#contributing)

</details>

## Features

- **Declarative API** — composable `Map` + layers + sources + components. Describe *what* the map should show; the library handles *how*.
- **Single HTML output** — standalone file with MapLibre GL JS; works via `file://` when data is embedded.
- **Embedded mode** — inline GeoJSON (optionally Geobuf + Gzip) so you can share one file.
- **Comparison mode** — before/after slider using the MapLibre compare plugin.
- **Feature-state expressions** — GPU-efficient dynamic styling (`fill_color`, `opacity`) via `setFeatureState`.
- **Extensible** — custom JS/CSS/HTML injection, `embed_data()` for arbitrary JSON.
- **LLM-friendly** — predictable names, stable contracts, and a keyword-indexed [API Guide](API_GUIDE.md).

**Available building blocks:**

| Category | Classes |
|----------|---------|
| **Layers** | `CircleLayer`, `FillLayer`, `H3Layer`, `VectorTileLayer` |
| **Sources** | `FileSource`, `ApiSource`, `VectorTileSource` |
| **Components** | `Legend`, `Popup`, `Sidebar`, `Search`, `FeatureSearch`, `Controls`, `BasemapSwitcher` |

## Installation

```bash
pip install llmaps
```

Optional extras:

```bash
pip install llmaps[h3]           # H3 aggregation (h3, geopandas)
pip install llmaps[compression]  # Geobuf + Gzip for embedded data
pip install llmaps[all]          # h3 + compression
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

| Example | Description |
|---------|-------------|
| [01_quick_start.py](examples/01_quick_start.py) | Circle layer, legend, popup, controls; synthetic points. |
| [02_fill_layer.py](examples/02_fill_layer.py) | Fill layer (polygons). |
| [03_h3_heatmap.py](examples/03_h3_heatmap.py) | H3 hexagon heatmap, embedded mode, auto_extent. |
| [04_comparison.py](examples/04_comparison.py) | Before/after comparison with slider; embedded. |

Run an example:

```bash
cd examples
python 01_quick_start.py
# Opens or writes 01_quick_start.html
```

## Built With

- [MapLibre GL JS](https://maplibre.org/) — frontend map rendering
- [Jinja2](https://jinja.palletsprojects.com/) — HTML template engine
- Optional: [H3](https://h3geo.org/), [GeoPandas](https://geopandas.org/), [Geobuf](https://github.com/pygeobuf/pygeobuf)

## Comparison with Alternatives

| Criterion | Kepler.gl | Folium / ipyleaflet | Custom MapLibre/Leaflet | **LLMaps** |
|-----------|-----------|---------------------|--------------------------|------------|
| **Ready-made components** | Limited by UI | Few map primitives | None | Full set: layers, legend, popup, sidebar, search, controls |
| **LLM-friendly** | No | Partial (verbose) | Depends on custom code | Yes: keyword index, clear API, stable contracts |
| **H3 / aggregation** | Yes | No (manual) | Manual | Yes (H3Layer) |
| **Embedded (file://)** | No | Often needs server | Manual | Yes (`embedded=True`) |
| **Comparison (before/after)** | No | No | Manual | Yes (`enable_comparison`) |
| **Single HTML output** | No | Possible | Manual | Yes (`save` / `to_html`) |
| **Customization** | Limited by UI | Good | Full | Full (config + templates + custom JS/CSS) |
| **No backend** | No | Often | Possible | Yes (embedded mode) |

**When to use LLMaps:** You want a single Python API to produce a standalone interactive map (especially with embedded data), with minimal boilerplate and good support for LLM-generated code.

**When to choose something else:** You need a full GIS UI (Kepler.gl), tight Jupyter-only integration (Folium/ipyleaflet), or a fully custom frontend stack (raw MapLibre/Leaflet with your own backend).

## Architecture

```
Python API  →  Config (to_dict())  →  HTML (Jinja2)  →  Frontend (MapLibre GL JS + plugins)
```

Everything reduces to a serializable dict — no framework magic. The generator turns that config into one HTML file with inline or linked JS/CSS. See [PHILOSOPHY.md](PHILOSOPHY.md) for design principles and rationale.

## Documentation

- **[API_GUIDE.md](API_GUIDE.md)** — LLM-friendly index of all components (keywords, when to use, alternatives).
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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
