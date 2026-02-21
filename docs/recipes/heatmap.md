# Recipe: H3 Heatmap

Build a heatmap-style visualization by aggregating points into H3 hexagons. Best for large point datasets (&gt;100k points) or when you want a density view.

## Requirements

- Point data (GeoJSON, CSV, or Parquet with geometry).

## Steps

1. **Load point data** with `FileSource` (or `ApiSource` for remote GeoJSON).
2. **Create an H3Layer** with `resolution`, `aggregation` (count/sum/mean/median), and `property_field` for the value used in aggregation and color gradient.
3. **Add a Legend** with a label for the H3 layer.
4. **Optional:** Use `Map(embedded=True)` so data is inlined in HTML; use `use_compression=True` to reduce size.
5. **Optional:** Call `map.auto_extent()` to fit the map to the data.

## Example

```python
from llmaps import Map
from llmaps.layers import H3Layer
from llmaps.sources import FileSource
from llmaps.components import Legend

source = FileSource(id="points", path="data/points.geojson")

layer = H3Layer(
    id="h3-heat",
    source=source,
    resolution=5,           # coarser = larger hexagons (e.g. 5 ≈ 2.5 km)
    aggregation="count",   # or "sum", "mean", "median"
    property_field="value",
    colors=["#ffffcc", "#800026"],
    opacity=0.7,
)

m = Map(center=[10.0, 50.0], zoom=4, title="H3 heatmap", tiles="osm")
m.add_layer(layer)
m.add_component(Legend(position="top-right", layer_labels={"h3-heat": "Point count"}))

m.auto_extent()
m.embedded = True
m.save("heatmap.html")
```

## Parameters to tune

| Parameter | Effect |
|-----------|--------|
| `resolution` | H3 resolution 0–15; lower = larger hexagons (e.g. 5 ≈ 2.5 km, 8 ≈ 460 m). |
| `aggregation` | `"count"` for density; `"sum"`/`"mean"`/`"median"` for a numeric field. |
| `property_field` | Field used for sum/mean/median and for the color gradient. |
| `colors` | Two or more colors for the gradient (e.g. low→high). |

## See also

- [Layers: H3Layer](../api/layers.md#h3layer)
- [Embedded map recipe](embedded-map.md) — for `embedded=True` and `use_compression=True`
