from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir.parent.parent.parent / "examples" / "real-world" / "cafes" / "data" / "paris_cafes.geojson"
    output_path = script_dir / "map_points_basic.html"

    source = FileSource(id="cafes", path=str(data_path))
    layer = CircleLayer(id="cafes-layer", source=source, radius=6, color="#3182bd", opacity=0.8)

    legend = Legend(position="top-right", layer_labels={"cafes-layer": "Cafes"})
    popup = Popup(trigger="hover", fields=["name", "amenity", "cuisine"], field_labels={"name": "Name", "amenity": "Type", "cuisine": "Cuisine"})
    controls = Controls(zoom=True, scale=True)

    m = Map(center=[0, 0], zoom=2, title="Compass Points Basic Validation", tiles="osm", locale="en-US", embedded=True, use_compression=True)
    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(controls)
    m.auto_extent()
    m.save(output_path)
    print(output_path)


if __name__ == "__main__":
    main()
