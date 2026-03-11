# Recipe: points-basic

Use this recipe for point datasets with fewer than 10,000 features when fixed-size styling is enough.

## build_map.py template

```python
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir / "{SOURCE_PATH}"
    output_path = script_dir / "map.html"

    source = FileSource(id="{SOURCE_ID}", path=str(data_path))

    layer = CircleLayer(
        id="{LAYER_ID}",
        source=source,
        radius={POINT_RADIUS},
        color="{POINT_COLOR}",
        opacity={POINT_OPACITY},
    )

    legend = Legend(
        position="{LEGEND_POSITION}",
        layer_labels={"{LAYER_ID}": "{LAYER_LABEL}"},
    )

    popup = Popup(
        trigger="{POPUP_TRIGGER}",
        fields={DISPLAY_FIELDS},
        field_labels={FIELD_LABELS},
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
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(controls)
    {AUTO_EXTENT_CALL}

    m.save(output_path)
    print(f"Saved map to {output_path}")


if __name__ == "__main__":
    main()
```

## Required placeholders

- `{SOURCE_PATH}`
- `{SOURCE_ID}`
- `{LAYER_ID}`
- `{MAP_TITLE}`
- `{DISPLAY_FIELDS}`
- `{FIELD_LABELS}`

## Optional placeholders with defaults

- `{POINT_RADIUS}`: `6`
- `{POINT_COLOR}`: `#3182bd`
- `{POINT_OPACITY}`: `0.8`
- `{LEGEND_POSITION}`: `top-right`
- `{POPUP_TRIGGER}`: `hover`
- `{FULLSCREEN}`: `False`
- `{MAP_CENTER}`: `[0, 0]`
- `{MAP_ZOOM}`: `2`
- `{TILES}`: `osm`
- `{LOCALE}`: `en-US`
- `{AUTO_EXTENT_CALL}`: `m.auto_extent()` when center/zoom are not provided
