"""Example: circle radius and color from one numeric field (DataDrivenSize + server legend)."""

from __future__ import annotations

from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, DataDrivenSize, Legend
from llmaps.layers import CircleLayer
from llmaps.sources.file import FileSource


def main() -> None:
    root = Path(__file__).parent
    data = root / "data" / "sample.geojson"
    out = root / "map.html"

    src = FileSource(id="pts", path=str(data))
    dds = DataDrivenSize(
        field="weight",
        size_range=(6.0, 24.0),
        legend_title="Size and color ∝ weight",
        value_format="thousands",
        locale="en-US",
        color_stops=[
            (0, "#dbeafe"),
            (80, "#38bdf8"),
            (200, "#0369a1"),
        ],
        color_mode="interpolate",
    )
    layer = CircleLayer(
        id="points",
        source=src,
        color="#64748b",
        opacity=0.9,
        data_driven_size=dds,
    )

    m = Map(
        center=[2.35, 48.86],
        zoom=11.0,
        title="DataDrivenSize sample",
        tiles="carto-light",
        embedded=True,
        use_compression=False,
        locale="en-US",
    )
    m.add_layer(layer)
    m.add_component(
        Legend(
            position="top-right",
            layer_labels={"points": "Weighted points"},
            instructions=["Radius and fill are driven by the `weight` property via DataDrivenSize."],
        )
    )
    m.add_component(Controls())
    m.save(str(out))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
