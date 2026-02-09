"""Fill layer example: polygon rendering with Legend and Popup."""

import json
from pathlib import Path

from llmaps import Map
from llmaps.components import Legend, Popup
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def _write_sample_geojson(path: Path) -> None:
    """Create a small GeoJSON with polygon features (e.g. regions/zones)."""
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [10.0, 50.0],
                    [10.5, 50.0],
                    [10.5, 50.5],
                    [10.0, 50.5],
                    [10.0, 50.0],
                ]],
            },
            "properties": {"name": "Region A", "value": 100},
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [10.5, 50.0],
                    [11.0, 50.0],
                    [11.0, 50.5],
                    [10.5, 50.5],
                    [10.5, 50.0],
                ]],
            },
            "properties": {"name": "Region B", "value": 200},
        },
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}),
        encoding="utf-8",
    )


def main() -> None:
    examples_dir = Path(__file__).resolve().parent
    data_path = examples_dir / "data" / "regions.geojson"
    if not data_path.exists():
        _write_sample_geojson(data_path)

    source = FileSource(id="regions", path=str(data_path))
    layer = FillLayer(
        id="regions-layer",
        source=source,
        fill_color="#3182bd",
        fill_opacity=0.6,
        stroke_color="#08519c",
        stroke_width=1.0,
    )

    m = Map(center=[10.5, 50.25], zoom=8, title="Fill layer example", tiles="osm")
    m.add_layer(layer)
    m.add_component(Legend(layer_labels={"regions-layer": "Regions"}))
    m.add_component(
        Popup(
            fields=["name", "value"],
            field_labels={"name": "Name", "value": "Value"},
        )
    )
    m.save(examples_dir / "02_fill_layer.html")
    print("Saved 02_fill_layer.html")


if __name__ == "__main__":
    main()
