# Recipe: Dynamic polygon highlighting with feature-state

GPU-efficient dynamic recoloring of polygons via MapLibre `setFeatureState`. Thousands of polygons update in ~5ms (vs ~200ms with `setData`).

## How it works

1. **`promote_id`** on the source → each feature gets a stable ID from a property
2. **`feature-state` expressions** in paint → `fill-color` interpolates by a numeric state key
3. **Setting state** — either declarative (`feature_state` on the layer, no JS) or via **`setFeatureState`** in custom JS (e.g. on click)

---

## Static data (automatic, no custom JS)

When colors come from a GeoJSON property and do not change at runtime, use the layer's **`feature_state`** parameter. The library auto-generates the JS that sets feature state for every feature after the source loads.

```python
from llmaps import Map
from llmaps.sources import FileSource
from llmaps.layers import FillLayer
from llmaps.expressions import feature_state_color, compute_color_stops

src = FileSource(id="countries", path="data/countries.geojson", promote_id="ISO_A3")
populations = [f["properties"]["POP_EST"] for f in geojson["features"] if f["properties"].get("POP_EST", 0) > 0]
color_stops = compute_color_stops(populations, method="jenks", palette="seismic-intensity", n_stops=7)

layer = FillLayer(
    id="population-layer",
    source=src,
    fill_color=feature_state_color(
        state_key="active",
        color_ramp_key="color",
        color_stops=color_stops,
        inactive="#f0f0f0",
        default="#e0e0e0",
    ),
    fill_opacity=0.8,
    feature_state={"active": True, "color": "POP_EST"},  # no add_custom_js
)
m = Map(center=[0, 20], zoom=2, embedded=True, use_compression=True)
m.add_layer(layer)
m.save("map.html")
```

---

## Dynamic highlighting (custom JS)

For interactive recoloring (e.g. click a polygon to highlight it), use **`add_custom_js`** and the JS utilities.

## Python setup

```python
from llmaps import Map
from llmaps.sources import FileSource
from llmaps.layers import FillLayer
from llmaps.expressions import (
    feature_state_color,
    feature_state_value,
    feature_state_fade_color,
    feature_state_fade_value,
)

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
    fill_color=feature_state_fade_color(
        color_ramp_key="delivery_hours",
        color_stops=[
            (0, "#004d33"),
            (12, "#00AA44"),
            (24, "#FFCC00"),
            (48, "#FF6600"),
            (72, "#CC0000"),
        ],
        inactive="#F0F0F0",
        state_key="active",
        fade_mix_key="fade_mix",
    ),
    fill_opacity=feature_state_fade_value(
        active=0.7,
        inactive=0.2,
        state_key="active",
        fade_mix_key="fade_mix",
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

        // Set base values first
        window.llmapsSetFeatureState('regions', feat.id, {
            active: true,
            fade_mix: 0,
            delivery_hours: feat.properties.delivery_hours || 0,
        });

        // Animate fade-in to avoid abrupt appearance
        window.llmapsAnimateFeatureState('regions', feat.id, {
            active: true,
            fade_mix: 1,
            delivery_hours: feat.properties.delivery_hours || 0,
        }, { duration: 280, easing: 'easeInOutSine' });
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
| `window.llmapsAnimateFeatureState(sourceId, featureId, targetState, options)` | Animate state with shared RAF loop (`duration`, `easing`) |
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
- Expressions: `feature_state_color`, `feature_state_value`, `feature_state_fade_mix`, `feature_state_fade_value`, `feature_state_fade_color`, `compute_color_stops` — in `llmaps.expressions`; compact ref in `get_llm_context()` output
