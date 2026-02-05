"""Comparison example: before/after maps with slider."""

import json
import random
from pathlib import Path

from llmaps import Map
from llmaps.components import Legend
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def _make_geojson_polygon(path: Path, features: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}),
        encoding="utf-8",
    )


def main():
    examples_dir = Path(__file__).resolve().parent
    data_dir = examples_dir / "data"
    before_path = data_dir / "comparison_before.geojson"
    after_path = data_dir / "comparison_after.geojson"

    def box(lon: float, lat: float, size: float):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [lon, lat],
                    [lon + size, lat],
                    [lon + size, lat + size],
                    [lon, lat + size],
                    [lon, lat],
                ]],
            },
            "properties": {},
        }

    if not before_path.exists():
        random.seed(1)
        before = [box(10 + random.uniform(0, 2), 50 + random.uniform(0, 2), 0.3) for _ in range(5)]
        _make_geojson_polygon(before_path, before)
    if not after_path.exists():
        random.seed(2)
        after = [box(10.5 + random.uniform(0, 2), 50.5 + random.uniform(0, 2), 0.25) for _ in range(6)]
        _make_geojson_polygon(after_path, after)

    src_before = FileSource(id="before", path=str(before_path))
    src_after = FileSource(id="after", path=str(after_path))
    layer_before = FillLayer(id="before-layer", source=src_before, fill_color="#3182bd", fill_opacity=0.6)
    layer_after = FillLayer(id="after-layer", source=src_after, fill_color="#de2d26", fill_opacity=0.6)

    m = Map(center=[11.0, 51.0], zoom=8, title="Before / After", tiles="osm")
    m.add_layer(layer_before).add_layer(layer_after)
    m.add_component(Legend(layer_labels={"before-layer": "Before", "after-layer": "After"}))
    m.enable_comparison(left_layers=["before-layer"], right_layers=["after-layer"])
    m.embedded = True
    m.save(examples_dir / "04_comparison.html")
    print("Saved 04_comparison.html (comparison mode, embedded)")


if __name__ == "__main__":
    main()
