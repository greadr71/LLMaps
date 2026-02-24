# Recipe: Before/After Comparison Within Storytelling Scenes

Show a draggable before/after slider during specific scenes in a scrollytelling narrative. The comparison overlay appears and disappears dynamically as the user scrolls through scenes.

## When to Use

- You have two map states (e.g. different years, before/after intervention) and want to tell a story that includes side-by-side comparison at specific moments.
- You want the comparison to be part of a narrative flow, not a standalone full-page slider.

## How It Works

1. Some scenes use `comparison=SceneComparison(...)` — these show a slider overlay.
2. Other scenes use `visible_layers` / `highlight` as usual — no slider, just the main map.
3. The comparison maps are created lazily on first use (no overhead for non-comparison scenes).
4. Camera sync is automatic: scrolling a comparison scene keeps all maps aligned.
5. Popups work on both comparison map panels.

## Example

```python
from llmaps import Map
from llmaps.components import Storytelling, Scene, SceneComparison, Controls, Popup
from llmaps.layers import FillLayer
from llmaps.sources import FileSource

# Two sources for two time periods
src_2016 = FileSource(id="data-2016", path="data/before.geojson", promote_id="id")
src_2018 = FileSource(id="data-2018", path="data/after.geojson", promote_id="id")

# Layers — hidden initially; scenes control visibility
layer_2016 = FillLayer(id="fill-2016", source=src_2016, fill_color="#b2182b", fill_opacity=0.6, visible=False)
layer_2018 = FillLayer(id="fill-2018", source=src_2018, fill_color="#2166ac", fill_opacity=0.6, visible=False)

scenes = [
    # Regular scene — text only, no layers
    Scene(
        id="intro",
        title="Introduction",
        content="<p>This map tells the story of change over time.</p>",
        center=[-77.5, 41.0],
        zoom=7,
    ),

    # Regular scene — show the "before" layer on the main map
    Scene(
        id="before",
        title="The Situation in 2016",
        content="<p>Here is how things looked in 2016.</p>",
        visible_layers=["fill-2016"],
    ),

    # Comparison scene — slider with before on left, after on right
    Scene(
        id="compare",
        title="2016 vs 2018",
        content="<p>Drag the slider to compare the two years.</p>",
        center=[-77.5, 41.0],
        zoom=7,
        comparison=SceneComparison(
            before_layers=["fill-2016"],
            after_layers=["fill-2018"],
            before_label="2016",
            after_label="2018",
        ),
    ),

    # Comparison scene with per-side highlights
    Scene(
        id="detail",
        title="Region #7: A Closer Look",
        content="<p>See how region 7 changed between the two periods.</p>",
        center=[-75.6, 40.1],
        zoom=9,
        comparison=SceneComparison(
            before_layers=["fill-2016"],
            after_layers=["fill-2018"],
            before_label="2016",
            after_label="2018",
            before_highlight={"data-2016": [7]},
            after_highlight={"data-2018": [7]},
        ),
    ),

    # Back to regular scene — slider disappears
    Scene(
        id="conclusion",
        title="Conclusion",
        content="<p>The same region, different outcomes.</p>",
        visible_layers=["fill-2018"],
    ),
]

m = Map(
    center=[-77.5, 41.0],
    zoom=7,
    title="Before / After Story",
    tiles="carto-light",
    locale="en-US",
    embedded=True,
    use_compression=True,
)
m.add_layer(layer_2016)
m.add_layer(layer_2018)
m.add_component(Popup(fields=["id", "name", "value"]))
m.add_component(Storytelling(scenes=scenes, position="left", width=420, progress=True))
m.add_component(Controls(zoom=True, scale=True))
m.save("story_comparison.html")
```

## Parameters

### `SceneComparison`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `before_layers` | list of str | [] | Layer ids on the left (before) side. |
| `after_layers` | list of str | [] | Layer ids on the right (after) side. |
| `before_label` | str or None | None | Label on the before panel (e.g. `"2016"`). |
| `after_label` | str or None | None | Label on the after panel (e.g. `"2018"`). |
| `before_highlight` | dict | {} | `{source_id: [feature_id, ...]}` on the before map. |
| `after_highlight` | dict | {} | `{source_id: [feature_id, ...]}` on the after map. |

### `Storytelling.comparison_slider_hint`

Custom tooltip text for the slider (e.g. `"Drag to compare"`). If `None`, an automatic locale-aware default is used ("Drag to compare" for English, "Потяните слайдер для сравнения" for Russian).

## Key Differences from `enable_comparison()`

| Feature | `enable_comparison()` | `SceneComparison` |
|---------|-----------------------|-------------------|
| Scope | Full-map, always visible | Per-scene, appears/disappears dynamically |
| Camera | Independent maps | Synced with main map + storytelling camera |
| Layers | Fixed left/right split | Different layers per scene |
| Highlights | Not supported | Per-side feature highlights |
| Popups | Separate setup | Automatic from main map config |

## Notes

- Outline layers (`{id}-outline`) are toggled automatically when their base layer is in `before_layers` or `after_layers`.
- Comparison maps are created lazily — no WebGL overhead until a comparison scene is reached.
- The comparison maps clone the main map's style, so all sources and layers are available without re-loading data.
- The slider tooltip appears only once per session on the first comparison scene.

## See Also

- [Components API: SceneComparison](../api/components.md#scenecomparison)
- [Storytelling recipe](storytelling.md) — without comparison
- [Comparison recipe](comparison.md) — static full-map comparison
