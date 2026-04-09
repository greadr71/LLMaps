import json
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.expressions import compute_color_stops, feature_state_color
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir.parent.parent.parent / "examples" / "real-world" / "world_population" / "data" / "countries.geojson"
    output_path = script_dir / "map_choropleth.html"

    with open(data_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    values = [f["properties"].get("POP_EST") for f in geojson["features"] if f["properties"].get("POP_EST") and f["properties"].get("POP_EST") > 0]
    color_stops = compute_color_stops(values, method="quantile", n_stops=5, palette="arctic-chill")

    source = FileSource(id="countries", path=str(data_path), promote_id="ISO_A3")
    layer = FillLayer(
        id="countries-layer",
        source=source,
        fill_color=feature_state_color("active", "value", color_stops, inactive="#f0f0f0", default="#e0e0e0"),
        fill_opacity=0.8,
        stroke_color="#ffffff",
        stroke_width=0.5,
        feature_state={"active": True, "value": "POP_EST"},
    )

    legend = Legend(
        position="bottom-left",
        layer_labels={"countries-layer": "Population"},
        layer_color_ramps={
            "countries-layer": {
                "stops": [[v, c] for v, c in color_stops],
                "label_min": f"{color_stops[0][0]:,.0f}",
                "label_max": f"{color_stops[-1][0]:,.0f}",
            }
        },
    )
    popup = Popup(trigger="hover", fields=["NAME", "POP_EST"], field_labels={"NAME": "Country", "POP_EST": "Population"})
    controls = Controls(zoom=True, scale=True)

    m = Map(center=[0, 20], zoom=2, title="Compass Choropleth Validation", tiles="carto-light", locale="en-US", embedded=True, use_compression=True)
    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(controls)
    m.save(output_path)
    print(output_path)


if __name__ == "__main__":
    main()
