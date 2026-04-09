# Recipe: hexagons

Use this recipe for high-volume point datasets (`>= 10,000` features) where aggregation improves clarity and performance.

## build_map.py template

```python
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.layers import H3Layer
from llmaps.palettes import get_palette_colors
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir / "{SOURCE_PATH}"
    output_path = script_dir / "map.html"

    source = FileSource(id="{SOURCE_ID}", path=str(data_path))

    layer = H3Layer(
        id="{LAYER_ID}",
        source=source,
        resolution={RESOLUTION},
        aggregation="{AGGREGATION}",
        property_field="{VALUE_FIELD}",
        colors=get_palette_colors("{PALETTE_ID}"),
        opacity={LAYER_OPACITY},
        stroke_width={STROKE_WIDTH},
    )

    legend = Legend(
        position="{LEGEND_POSITION}",
        layer_labels={"{LAYER_ID}": "{LAYER_LABEL}"},
        layer_descriptions={
            "{LAYER_ID}": "H3 resolution {RESOLUTION}, aggregation: {AGGREGATION}"
        },
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
- `{RESOLUTION}`
- `{AGGREGATION}`
- `{PALETTE_ID}`

## Optional placeholders

- `{VALUE_FIELD}`: use actual field for `sum`/`mean`/`median`; for `count` use a valid numeric field or map-level decision to skip field-dependent popup rows
- `{LAYER_OPACITY}`: `0.75`
- `{STROKE_WIDTH}`: `0.0`
- `{POPUP_TRIGGER}`: `hover`
