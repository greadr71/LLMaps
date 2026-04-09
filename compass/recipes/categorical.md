# Recipe: categorical

Use this recipe for polygon datasets where a categorical field defines styling.

## build_map.py template

```python
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir / "{SOURCE_PATH}"
    output_path = script_dir / "map.html"

    source = FileSource(id="{SOURCE_ID}", path=str(data_path))

    fill_expr = [
        "match",
        ["get", "{CATEGORY_FIELD}"],
        {COLOR_MAP},
        "{DEFAULT_COLOR}",
    ]

    layer = FillLayer(
        id="{LAYER_ID}",
        source=source,
        fill_color=fill_expr,
        fill_opacity={FILL_OPACITY},
        stroke_color="{STROKE_COLOR}",
        stroke_width={STROKE_WIDTH},
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
- `{CATEGORY_FIELD}`
- `{COLOR_MAP}`

## Placeholder format note

- `{COLOR_MAP}` is a flattened list of category and color pairs, for example:
  `"A", "#1f78b4", "B", "#33a02c", "C", "#e31a1c"`
- For category-first generation, start with a qualitative palette (for example `crameri-viko`) and map categories to palette colors deterministically.
