# Recipe: Before/After Comparison Map

Build a map with a slider that compares two states (e.g. before/after). Two maps are shown side by side; the user drags the slider to reveal one or the other.

## Requirements

- Two (or more) layers: one set for “before” (left) and one for “after” (right).
- Implementation uses the MapLibre GL JS compare plugin (maplibre-gl-compare).

## Steps

1. **Create two layers** (or two groups of layers), e.g. `FillLayer` or `CircleLayer`, each with its own source or shared source with different styling.
2. **Add both layers** to the map with `add_layer()`.
3. **Call `enable_comparison(left_layers, right_layers)`** with lists of layer ids: left map shows `left_layers`, right map shows `right_layers`.
4. **Optional:** Use `Map(embedded=True)` so data is inlined and the map works via `file://`.
5. **Save** with `save(path)`.

## Example

```python
from llmaps import Map
from llmaps.layers import FillLayer
from llmaps.sources import FileSource
from llmaps.components import Legend

src_before = FileSource(id="before", path="data/before.geojson")
src_after = FileSource(id="after", path="data/after.geojson")

layer_before = FillLayer(
    id="before-layer",
    source=src_before,
    fill_color="#3182bd",
    fill_opacity=0.6,
)
layer_after = FillLayer(
    id="after-layer",
    source=src_after,
    fill_color="#de2d26",
    fill_opacity=0.6,
)

m = Map(center=[11.0, 51.0], zoom=8, title="Before / After", tiles="osm")
m.add_layer(layer_before)
m.add_layer(layer_after)
m.add_component(Legend(layer_labels={
    "before-layer": "Before",
    "after-layer": "After",
}))
m.enable_comparison(
    left_layers=["before-layer"],
    right_layers=["after-layer"],
)
m.embedded = True
m.save("comparison.html")
```

## Notes

- Layer ids in `left_layers` and `right_layers` must exist on the map.
- The same layer id must not appear in both lists.
- You can pass multiple layer ids in each list to show several layers on the left or right side.

## See also

- [Map: enable_comparison](../api/map.md#enable_comparisonleft_layers-right_layers)
- [API_GUIDE: Map](../../API_GUIDE.md#map-and-core)
- [Embedded map recipe](embedded-map.md)
