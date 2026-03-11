from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.layers import H3Layer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir.parent.parent.parent / "examples" / "real-world" / "earthquakes" / "data" / "earthquakes_with_depth.geojson"
    output_path = script_dir / "map_hexagons.html"

    source = FileSource(id="earthquakes", path=str(data_path))
    layer = H3Layer(
        id="earthquakes-h3",
        source=source,
        resolution=6,
        aggregation="mean",
        property_field="depth",
        colors=["#ffffcc", "#fd8d3c", "#800026"],
        opacity=0.75,
        stroke_width=0.0,
    )

    legend = Legend(position="top-right", layer_labels={"earthquakes-h3": "Earthquake Density"})
    popup = Popup(trigger="hover", fields=["depth", "sig"], field_labels={"depth": "Depth", "sig": "Significance"})
    controls = Controls(zoom=True, scale=True)

    m = Map(center=[0, 0], zoom=2, title="Compass Hexagons Validation", tiles="carto-dark", locale="en-US", embedded=True, use_compression=True)
    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(controls)
    m.auto_extent()
    m.save(output_path)
    print(output_path)


if __name__ == "__main__":
    main()
