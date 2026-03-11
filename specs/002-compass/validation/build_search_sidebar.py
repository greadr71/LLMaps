from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, FeatureSearch, Legend, Sidebar
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    data_path = script_dir.parent.parent.parent / "examples" / "real-world" / "cafes" / "data" / "paris_cafes.geojson"
    output_path = script_dir / "map_search_sidebar.html"

    source = FileSource(id="cafes", path=str(data_path))
    layer = CircleLayer(id="cafes-layer", source=source, radius=6, color="#10b981", opacity=0.8)

    legend = Legend(position="top-right", layer_labels={"cafes-layer": "Cafes"})
    feature_search = FeatureSearch(
        position="top-left",
        placeholder="Search by name...",
        search_fields={"cafes": ["name", "amenity"]},
        field_labels={"name": "Name", "amenity": "Type"},
        max_results=10,
        zoom_on_select=14,
    )
    sidebar = Sidebar(
        position="right",
        width=420,
        title_field="name",
        fields_by_layer={"cafes-layer": ["amenity", "cuisine", "opening_hours", "website"]},
        field_labels={"amenity": "Type", "cuisine": "Cuisine", "opening_hours": "Hours", "website": "Website"},
        hide_empty_fields=True,
    )
    controls = Controls(zoom=True, scale=True)

    m = Map(center=[2.3522, 48.8566], zoom=12, title="Compass Search Sidebar Validation", tiles="osm", locale="en-US", embedded=True, use_compression=True)
    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(feature_search)
    m.add_component(sidebar)
    m.add_component(controls)
    m.save(output_path)
    print(output_path)


if __name__ == "__main__":
    main()
