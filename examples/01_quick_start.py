"""Quick start example for LLMaps.

This example uses synthetic point data to keep the repository small and
fully self-contained. It demonstrates the minimal Map API, a circle
layer and a few basic components.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.layers.circle import CircleLayer
from llmaps.sources.file import FileSource


def _write_synthetic_geojson(path: Path, count: int = 20) -> None:
    """Create a tiny GeoJSON file with random-ish points.

    The coordinates are hard-coded around central Europe to avoid any
    runtime dependencies and provide a deterministic demo.
    """

    import random

    random.seed(42)

    features = []
    base_lon, base_lat = 10.0, 50.0
    for i in range(count):
        lon = base_lon + random.uniform(-5, 5)
        lat = base_lat + random.uniform(-3, 3)
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {
                    "name": f"Location {i + 1}",
                    "value": random.randint(10, 100),
                },
            }
        )

    geojson = {"type": "FeatureCollection", "features": features}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(geojson), encoding="utf-8")


def build_map() -> Map:
    examples_dir = Path(__file__).resolve().parent
    data_path = examples_dir / "data" / "synthetic_points.geojson"

    if not data_path.exists():
        _write_synthetic_geojson(data_path)

    source = FileSource(id="points", path=str(data_path))

    layer = CircleLayer(
        id="points-layer",
        source=source,
        radius=6,
        color="#3182bd",
        opacity=0.8,
    )

    legend = Legend(
        position="top-right",
        show_toggle=False,
        layer_labels={"points-layer": "Synthetic points"},
    )

    popup = Popup(
        fields=["name", "value"],
        field_labels={"name": "Name", "value": "Value"},
    )

    controls = Controls(zoom=True, scale=True, fullscreen=False)

    m = Map(center=[10.0, 50.0], zoom=4, title="LLMaps quick start", tiles="osm")
    m.add_layer(layer).add_component(legend).add_component(popup).add_component(controls)
    return m


def main() -> None:
    examples_dir = Path(__file__).resolve().parent
    output_path = examples_dir / "01_quick_start.html"
    build_map().save(output_path)
    print(f"Map saved to {output_path}")


if __name__ == "__main__":
    main()

