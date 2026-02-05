"""H3 heatmap example: aggregate points into hexagons, auto_extent, embedded."""

import json
import random
from pathlib import Path

from llmaps import Map
from llmaps.components import Legend
from llmaps.layers import H3Layer
from llmaps.sources import FileSource


def _write_synthetic_geojson(path: Path, count: int = 200) -> None:
    random.seed(42)
    features = []
    base_lon, base_lat = 10.0, 50.0
    for i in range(count):
        lon = base_lon + random.uniform(-5, 5)
        lat = base_lat + random.uniform(-3, 3)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"name": f"Location {i + 1}", "value": random.randint(10, 100)},
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8")


def main():
    examples_dir = Path(__file__).resolve().parent
    data_path = examples_dir / "data" / "synthetic_points.geojson"
    if not data_path.exists():
        _write_synthetic_geojson(data_path, 200)

    source = FileSource(id="points", path=str(data_path))
    layer = H3Layer(
        id="h3-heat",
        source=source,
        resolution=5,
        aggregation="count",
        property_field="value",
        colors=["#ffffcc", "#800026"],
        opacity=0.7,
    )

    m = Map(center=[10.0, 50.0], zoom=4, title="H3 heatmap", tiles="osm")
    m.add_layer(layer).add_component(
        Legend(position="top-right", layer_labels={"h3-heat": "Point count"})
    )
    m.auto_extent()
    m.embedded = True
    m.save(examples_dir / "03_h3_heatmap.html")
    print("Saved 03_h3_heatmap.html (embedded, open via file://)")


if __name__ == "__main__":
    main()
