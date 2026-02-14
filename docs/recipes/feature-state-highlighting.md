# Recipe: Dynamic polygon highlighting with feature-state

GPU-efficient dynamic recoloring of polygons via MapLibre `setFeatureState`. Thousands of polygons update in ~5ms (vs ~200ms with `setData`).

## How it works

1. **`promote_id`** on the source → each feature gets a stable ID from a property
2. **`feature-state` expressions** in paint → `fill-color` interpolates by a numeric state key
3. **`setFeatureState`** on click → polygons instantly recolor (GPU-side, no re-upload)

## Python setup

```python
from llmaps import Map
from llmaps.sources import FileSource
from llmaps.layers import FillLayer
from llmaps.expressions import feature_state_color, feature_state_value

# Source with promote_id — each feature needs a unique "_fid" property
src = FileSource(
    id="regions",
    path="data/regions.geojson",
    promote_id="_fid",   # keyword-only
)

# FillLayer with feature-state expressions
layer = FillLayer(
    id="regions-layer",
    source=src,
    fill_color=feature_state_color(
        state_key="active",
        color_ramp_key="delivery_hours",
        color_stops=[
            (0, "#004d33"),
            (12, "#00AA44"),
            (24, "#FFCC00"),
            (48, "#FF6600"),
            (72, "#CC0000"),
        ],
        inactive="#F0F0F0",
        default="#E0E0E0",
    ),
    fill_opacity=feature_state_value(
        state_key="active",
        active=0.7,
        inactive=0.2,
        default=0.6,
    ),
)

m = Map(center=[40, 55], zoom=4, embedded=True, use_compression=True)
m.add_layer(layer)

# Custom JS to handle clicks and set feature state
m.add_custom_js("""
window.llmapsOnLayersReady(function(map) {
    map.on('click', 'regions-layer', function(e) {
        const feat = e.features && e.features[0];
        if (!feat) return;

        // Clear previous states
        window.llmapsClearFeatureStates('regions');

        // Set new state — fill-color expression will react instantly
        window.llmapsSetFeatureState('regions', feat.id, {
            active: true,
            delivery_hours: feat.properties.delivery_hours || 0,
        });
    });
});
""")

m.save("map.html")
```

## What `feature_state_color` generates

```python
feature_state_color(
    state_key="active",
    color_ramp_key="delivery_hours",
    color_stops=[(0, "#004d33"), (12, "#00AA44"), (24, "#FFCC00")],
    inactive="#F0F0F0",
    default="#E0E0E0",
)
```

Produces this MapLibre expression:

```json
[
  "case",
  ["==", ["feature-state", "active"], true],
  ["interpolate", ["linear"], ["feature-state", "delivery_hours"],
    0, "#004d33", 12, "#00AA44", 24, "#FFCC00"],
  ["==", ["feature-state", "active"], false],
  "#F0F0F0",
  "#E0E0E0"
]
```

## JS utilities reference

| Function | Description |
|----------|-------------|
| `window.llmapsSetFeatureState(sourceId, featureId, state)` | Set state on a single feature |
| `window.llmapsClearFeatureStates(sourceId)` | Clear all feature states on a source |
| `window.llmapsGetSourceData(sourceId)` | Get GeoJSON data (async, works with compression) |
| `window.llmapsOnLayersReady(fn)` | Register callback for when layers are loaded |

## Requirements

- Source must have `promote_id` pointing to a unique property in the GeoJSON
- Each feature in the GeoJSON must have that property (e.g. `_fid`)
- FillLayer `fill_color` / `fill_opacity` must use expressions (not plain strings)

## See also

- [Layers API — FillLayer](../api/layers.md#filllayer) — expression support
- [Sources API — promote_id](../api/sources.md#basesource)
- [API Guide — Expressions](../../API_GUIDE.md#expressions)
