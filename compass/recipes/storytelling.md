# Recipe: storytelling

Use this recipe when the user wants a narrative map with ordered scenes.

## build_map.py template

```python
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Scene, Storytelling
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir / "{SOURCE_PATH}"
    output_path = script_dir / "map.html"

    source = FileSource(id="{SOURCE_ID}", path=str(data_path), promote_id="{PROMOTE_ID}")

    layer = FillLayer(
        id="{LAYER_ID}",
        source=source,
        fill_color="{FILL_COLOR}",
        fill_opacity={FILL_OPACITY},
        stroke_color="{STROKE_COLOR}",
        stroke_width={STROKE_WIDTH},
        visible=False,
    )

    scenes = {SCENES}

    storytelling = Storytelling(
        scenes=scenes,
        position="{STORY_POSITION}",
        width={STORY_WIDTH},
        progress=True,
        snap_mode="{SNAP_MODE}",
        touch_swipe={TOUCH_SWIPE},
    )

    controls = Controls(zoom=True, scale=True, fullscreen={FULLSCREEN})

    m = Map(
        center={MAP_CENTER},
        zoom={MAP_ZOOM},
        title="{MAP_TITLE}",
        tiles="{TILES}",
        locale="{LOCALE}",
        embedded=True,
        use_compression=True,
    )

    m.add_layer(layer)
    m.add_component(storytelling)
    m.add_component(controls)

    m.save(output_path)
    print(f"Saved storytelling map to {output_path}")


if __name__ == "__main__":
    main()
```

## Required placeholders

- `{SOURCE_PATH}`
- `{SOURCE_ID}`
- `{LAYER_ID}`
- `{PROMOTE_ID}`
- `{SCENES}`

## `{SCENES}` placeholder example

```python
[
    Scene(
        id="intro",
        title="Overview",
        content="<p>Story starts here.</p>",
        center=[-77.5, 40.5],
        zoom=6,
        visible_layers=["districts"],
        fly_duration=1800,
    ),
    Scene(
        id="focus",
        title="Detail",
        content="<p>Focus on region.</p>",
        center=[-75.5, 40.0],
        zoom=8,
        visible_layers=["districts"],
        fly_duration=1800,
    ),
]
```
