# LLMaps

**A Python library for creating interactive web maps, optimized for LLM-assisted development.**

LLMaps lets you build a map in Python (layers, sources, legend, popup, controls), then output a single HTML file that works in any browser—no server required when using embedded mode.

## Features

- **Simple API:** `Map` + layers (`CircleLayer`, `FillLayer`, `H3Layer`, `VectorTileLayer`) + sources (`FileSource`, `ApiSource`, `VectorTileSource`) + components (`Legend`, `Popup`, `Search`, `Controls`).
- **Single HTML output:** Standalone file with MapLibre GL JS; works via `file://` when data is embedded.
- **Embedded mode:** Inline GeoJSON (optionally Geobuf + Gzip) so you can share one file.
- **Comparison mode:** Before/after slider using the MapLibre compare plugin.
- **LLM-friendly:** Clear names, stable contracts, and an [API index](API_GUIDE.md) with keywords for grep and context.

## Installation

```bash
pip install llmaps
```

Optional extras:

```bash
pip install llmaps[h3]        # H3 aggregation (h3, geopandas)
pip install llmaps[compression]  # Geobuf + Gzip for embedded data
pip install llmaps[all]       # h3 + compression
```

## Quick start

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

## Documentation

- **[API_GUIDE.md](API_GUIDE.md)** — LLM-friendly index of components (keywords, when to use, alternatives).
- **[PHILOSOPHY.md](PHILOSOPHY.md)** — Concept, design principles, comparison with alternatives.
- **[docs/api/](docs/api/)** — Map, layers, sources, components (parameters and examples).
- **[docs/recipes/](docs/recipes/)** — Heatmap, comparison, embedded map.

## Tile providers

Use the `tiles` argument when creating the map:

- `"osm"` — OpenStreetMap (default)
- `"carto-light"` — Carto Light
- `"carto-dark"` — Carto Dark
- `"yandex"`, `"2gis"` — Placeholder URLs; replace with your own if needed.

## License

MIT. See [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
