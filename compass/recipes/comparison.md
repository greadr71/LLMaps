# Recipe: comparison

Use this recipe for before/after analysis using two sources and a comparison slider.

## build_map.py template

```python
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Popup
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    before_path = script_dir / "{SOURCE_PATH_BEFORE}"
    after_path = script_dir / "{SOURCE_PATH_AFTER}"
    output_path = script_dir / "map.html"

    source_before = FileSource(id="{SOURCE_ID_BEFORE}", path=str(before_path), promote_id="{PROMOTE_ID}")
    source_after = FileSource(id="{SOURCE_ID_AFTER}", path=str(after_path), promote_id="{PROMOTE_ID}")

    layer_before = FillLayer(
        id="{LAYER_ID_BEFORE}",
        source=source_before,
        fill_color="{BEFORE_COLOR}",
        fill_opacity={FILL_OPACITY},
        stroke_color="{STROKE_COLOR}",
        stroke_width={STROKE_WIDTH},
        visible=True,
    )

    layer_after = FillLayer(
        id="{LAYER_ID_AFTER}",
        source=source_after,
        fill_color="{AFTER_COLOR}",
        fill_opacity={FILL_OPACITY},
        stroke_color="{STROKE_COLOR}",
        stroke_width={STROKE_WIDTH},
        visible=False,
    )

    popup = Popup(
        trigger="{POPUP_TRIGGER}",
        fields={DISPLAY_FIELDS},
        field_labels={FIELD_LABELS},
        fields_by_layer={
            "{LAYER_ID_BEFORE}": {DISPLAY_FIELDS},
            "{LAYER_ID_AFTER}": {DISPLAY_FIELDS},
        },
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

    m.add_layer(layer_before)
    m.add_layer(layer_after)
    m.add_component(popup)
    m.add_component(controls)

    m.enable_comparison(
        left_layers=["{LAYER_ID_BEFORE}"],
        right_layers=["{LAYER_ID_AFTER}"],
    )

    {AUTO_EXTENT_CALL}
    m.save(output_path)
    print(f"Saved comparison map to {output_path}")


if __name__ == "__main__":
    main()
```

## Required placeholders

- `{SOURCE_PATH_BEFORE}`
- `{SOURCE_PATH_AFTER}`
- `{SOURCE_ID_BEFORE}`
- `{SOURCE_ID_AFTER}`
- `{LAYER_ID_BEFORE}`
- `{LAYER_ID_AFTER}`
- `{PROMOTE_ID}`
