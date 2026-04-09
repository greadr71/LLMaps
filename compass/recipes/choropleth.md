# Recipe: choropleth

Use this recipe for polygon datasets with a numeric field.

## build_map.py template

```python
import json
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.expressions import compute_color_stops, feature_state_color
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir / "{SOURCE_PATH}"
    output_path = script_dir / "map.html"

    with open(data_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    values = [
        feature["properties"].get("{VALUE_FIELD}")
        for feature in geojson["features"]
        if feature["properties"].get("{VALUE_FIELD}") is not None
    ]

    color_stops = compute_color_stops(
        values,
        method="{CLASSIFICATION_METHOD}",
        n_stops={N_STOPS},
        palette="{PALETTE_ID}",
    )

    source = FileSource(
        id="{SOURCE_ID}",
        path=str(data_path),
        promote_id="{PROMOTE_ID}",
    )

    layer = FillLayer(
        id="{LAYER_ID}",
        source=source,
        fill_color=feature_state_color(
            state_key="active",
            color_ramp_key="value",
            color_stops=color_stops,
            inactive="{INACTIVE_COLOR}",
            default="{DEFAULT_COLOR}",
        ),
        fill_opacity={FILL_OPACITY},
        stroke_color="{STROKE_COLOR}",
        stroke_width={STROKE_WIDTH},
        feature_state={"active": True, "value": "{VALUE_FIELD}"},
    )

    legend = Legend(
        position="{LEGEND_POSITION}",
        layer_labels={"{LAYER_ID}": "{LAYER_LABEL}"},
        layer_color_ramps={
            "{LAYER_ID}": {
                "stops": [[v, c] for v, c in color_stops],
                "label_min": f"{color_stops[0][0]:,.0f}",
                "label_max": f"{color_stops[-1][0]:,.0f}",
            }
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
- `{VALUE_FIELD}`
- `{PROMOTE_ID}`
- `{CLASSIFICATION_METHOD}`
- `{N_STOPS}`
- `{PALETTE_ID}`
