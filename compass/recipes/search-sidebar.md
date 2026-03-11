# Recipe: search-sidebar

Use this recipe when users need search and richer feature details than popup-only interaction.

## build_map.py template

```python
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, FeatureSearch, Legend, Sidebar
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

    feature_search = FeatureSearch(
        position="{SEARCH_POSITION}",
        placeholder="{SEARCH_PLACEHOLDER}",
        search_fields={SEARCH_FIELDS},
        field_labels={FIELD_LABELS},
        max_results={MAX_RESULTS},
        zoom_on_select={ZOOM_ON_SELECT},
    )

    sidebar = Sidebar(
        position="{SIDEBAR_POSITION}",
        width={SIDEBAR_WIDTH},
        title_field="{TITLE_FIELD}",
        fields_by_layer={"{LAYER_ID}": {DISPLAY_FIELDS}},
        field_labels={FIELD_LABELS},
        hide_empty_fields=True,
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
    m.add_component(feature_search)
    m.add_component(sidebar)
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
- `{SEARCH_FIELDS}`
- `{DISPLAY_FIELDS}`
- `{FIELD_LABELS}`

## Placeholder format notes

- `{SEARCH_FIELDS}` example: `{"{SOURCE_ID}": ["name", "code"]}`
- `{DISPLAY_FIELDS}` example: `["name", "category", "address", "value"]`
