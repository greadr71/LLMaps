# Scrollytelling Map

A scrollytelling map pairs a scrollable narrative panel with a reactive map.  As the user reads through scenes, the map animates: camera flies to new locations, layers appear/disappear, and features get highlighted.

## Minimal Example

```python
from llmaps import Map
from llmaps.components import Storytelling, Scene, Controls
from llmaps.layers import FillLayer
from llmaps.sources import FileSource

source = FileSource("regions", "data/regions.geojson", promote_id="id")

layer = FillLayer(
    id="regions-fill",
    source=source,
    fill_color="#3182bd",
    fill_opacity=0.6,
    visible=False,  # hidden at start; scenes control visibility
)

scenes = [
    Scene(
        id="intro",
        title="Welcome",
        content="<p>This map tells a story about regions.</p>",
        center=[10.0, 50.0],
        zoom=5,
    ),
    Scene(
        id="show-data",
        title="The Data",
        content="<p>Here are the regions colored by category.</p>",
        visible_layers=["regions-fill"],  # show the layer
    ),
    Scene(
        id="highlight",
        title="Key Region",
        content="<p>Region #42 is special.</p>",
        center=[12.0, 48.0],
        zoom=8,
        visible_layers=["regions-fill"],
        highlight={"regions": [42]},  # highlight feature with id=42
    ),
]

m = Map(center=[10.0, 50.0], zoom=5, tiles="carto-light", embedded=True)
m.add_layer(layer)
m.add_component(Storytelling(scenes=scenes))
m.add_component(Controls(zoom=True, scale=True))
m.save("story_map.html")
```

## Key Concepts

### Scene Camera

Each scene can optionally set `center`, `zoom`, `bearing`, and `pitch`. If `None`, the camera stays where it is — useful for scenes that only change text or layer visibility.

### Layer Visibility

- Set `visible=False` on layers you want hidden initially.
- Use `visible_layers=["layer-id"]` in a scene to show specific layers.
- Use `visible_layers=[]` to hide all layers (e.g. for a text-only transition).
- Use `visible_layers=None` (default) to not change visibility.

Outline layers (`{id}-outline`) are toggled automatically.

### Feature Highlights

Use `highlight={"source_id": [feature_id, ...]}` to set `highlighted: true` on specific features via feature-state. Combine with expressions:

```python
fill_color = [
    "case",
    ["boolean", ["feature-state", "highlighted"], False],
    "#ff0000",  # highlighted color
    "#3182bd",  # normal color
]
```

Requires `promote_id` on the source.

### Navigation Dots

When `progress=True` (default), clickable dots appear on the edge of the map. Hover shows the scene title. Click scrolls to that scene.

### Responsive

On screens < 768px, the layout switches to vertical: map on top (60vh), narrative below (40vh). Navigation dots are hidden.

## See Also

- [Components API: Storytelling](../api/components.md#storytelling)
