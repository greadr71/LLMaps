# Recipe: Embedded Map (Single HTML, file://)

Generate a single HTML file that contains all data inline so the map works when opened via `file://` (e.g. from disk or after download), without a web server.

## When to use

- Share a standalone map (e.g. email, USB, internal docs).
- Open the map in a browser without running a server.
- Embed the map in another page or notebook by using the HTML string from `to_html()`.

## Steps

1. **Set `Map(embedded=True)`** so that data from file-based sources (e.g. `FileSource`) is inlined in the HTML.
2. **Optional:** Set `use_compression=True` to compress GeoJSON with Geobuf + Gzip and reduce file size (requires optional dependency: `pip install llmaps[compression]` or `llmaps[all]`).
3. **Use `FileSource`** for layers that should be embedded; `ApiSource` and `VectorTileSource` are not inlined (they are loaded by the frontend from URL/tiles).
4. **Save** with `save(path)` or get the string with `to_html()`.

## Example (no compression)

```python
from llmaps import Map
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource
from llmaps.components import Legend

source = FileSource(id="points", path="data/points.geojson")
layer = CircleLayer(id="points-layer", source=source, radius=6, color="#3182bd", opacity=0.8)

m = Map(center=[10.0, 50.0], zoom=4, title="Embedded map", tiles="osm")
m.add_layer(layer)
m.add_component(Legend(layer_labels={"points-layer": "Points"}))

m.embedded = True
m.save("embedded_map.html")
# Open embedded_map.html in a browser via file://
```

## Example (with compression)

```python
m.embedded = True
m.use_compression = True
m.save("embedded_compressed.html")
```

Requires: `pip install llmaps[compression]` (geobuf). The frontend will decompress the data before rendering.

## Notes

- **Size:** Embedded mode inlines all GeoJSON (or compressed payloads) for file-based sources. For very large data, consider `ApiSource` (data loaded from URL) or vector tiles.
- **H3Layer:** With embedded mode, H3 aggregation is computed when building the map; the inlined data is the aggregated GeoJSON, not the raw points.
- **Compression:** Geobuf + Gzip typically reduces size significantly; use `use_compression=True` when the HTML would otherwise be too large.

## See also

- [Map: embedded, use_compression](../api/map.md#constructor)
- [API_GUIDE: Map and Core](../../API_GUIDE.md#map-and-core)
- [Heatmap recipe](heatmap.md) — often used with embedded + compression
