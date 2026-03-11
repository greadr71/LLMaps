# Recipe: points-sized

Use this recipe for point datasets with fewer than 10,000 features when a numeric field should drive marker size and/or color.

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

    radius_expr = [
        "interpolate",
        ["linear"],
        ["get", "{VALUE_FIELD}"],
        {RADIUS_MIN_VALUE},
        {RADIUS_MIN_SIZE},
        {RADIUS_MAX_VALUE},
        {RADIUS_MAX_SIZE},
    ]

    color_expr = [
        "interpolate",
        ["linear"],
        ["get", "{VALUE_FIELD}"],
        {COLOR_STOPS}
    ]

    layer = CircleLayer(
        id="{LAYER_ID}",
        source=source,
        radius=radius_expr,
        color=color_expr,
        opacity={POINT_OPACITY},
    )

    legend = Legend(
        position="{LEGEND_POSITION}",
        layer_labels={"{LAYER_ID}": "{LAYER_LABEL}"},
        layer_descriptions={"{LAYER_ID}": "Size and color by {VALUE_FIELD}"},
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
- `{VALUE_FIELD}`
- `{COLOR_STOPS}`
- `{DISPLAY_FIELDS}`
- `{FIELD_LABELS}`

## Notes

- `{COLOR_STOPS}` should be flattened stop pairs, for example:
  `0, "#f7fbff", 50, "#6baed6", 100, "#08306b"`
- If user wants fixed size but dynamic color, replace `radius_expr` with a constant.
- `{COLOR_PALETTE}` can be used upstream to produce `{COLOR_STOPS}`.
