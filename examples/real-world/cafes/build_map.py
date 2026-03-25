"""Build an interactive map of cafes and restaurants in Paris.

This example demonstrates:
- CircleLayer with MapLibre expressions for conditional styling
- Popup with hover trigger
- Sidebar with detailed information
- FeatureSearch (filtering by attribute)
- BasemapSwitcher for different tile providers
- Legend with multiple categories
"""

from pathlib import Path

from llmaps import Map
from llmaps.components import (
    BasemapSwitcher,
    Controls,
    FeatureSearch,
    Legend,
    Popup,
    Sidebar,
)
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource


def main():
    """Build the map."""
    # Define paths
    script_dir = Path(__file__).parent
    data_path = script_dir / "data" / "paris_cafes.geojson"
    output_path = script_dir / "map.html"

    # Create data source
    source = FileSource(id="cafes", path=str(data_path))

    # Create layer with conditional styling using MapLibre expressions
    # Radius: cafe = 5px, restaurant = 7px, default = 6px
    # Color: cafe = orange, restaurant = red, default = gray
    layer = CircleLayer(
        id="cafes-layer",
        source=source,
        radius=["match", ["get", "amenity"], "cafe", 5, "restaurant", 7, 6],
        color=[
            "match",
            ["get", "amenity"],
            "cafe",
            "#10b981",
            "restaurant",
            "#3b82f6",
            "#999999",
        ],
        opacity=0.8,
        stroke_width=1,
        stroke_color="#ffffff",
    )

    # Create legend
    legend = Legend(
        title="Paris Cafes & Restaurants",
        description="Data from OpenStreetMap",
        entries=[
            {"label": "Cafe", "color": "#10b981"},
            {"label": "Restaurant", "color": "#3b82f6"},
        ],
        position="top-right",
        collapsible=True,
    )

    # Create popup (hover trigger)
    popup = Popup(
        trigger="hover",
        fields=["name", "cuisine", "opening_hours"],
        field_labels={
            "name": "Name",
            "cuisine": "Cuisine",
            "opening_hours": "Hours",
        },
    )

    # Create sidebar (click trigger with detailed info)
    sidebar = Sidebar(
        title_field="name",
        fields_by_layer={
            "cafes-layer": [
                "amenity",
                "cuisine",
                "opening_hours",
                "phone",
                "website",
                "addr_street",
                "addr_housenumber",
                "outdoor_seating"
            ]
        },
        field_labels={
            "amenity": "Type",
            "cuisine": "Cuisine",
            "opening_hours": "Opening Hours",
            "phone": "Phone",
            "website": "Website",
            "addr_street": "Street",
            "addr_housenumber": "House Number",
            "outdoor_seating": "Outdoor Seating",
        },
        hide_empty_fields=True,
    )

    # Create feature search
    feature_search = FeatureSearch(
        layer_id="cafes-layer",
        search_field="name",
        placeholder="Search cafe by name...",
        position="top-left",
    )

    # Create basemap switcher
    basemap_switcher = BasemapSwitcher(
        position="bottom-right",
        basemaps=["osm", "carto-light", "carto-dark"],
    )

    # Create controls
    controls = Controls(
        zoom=True,
        scale=True,
        fullscreen=True,
    )

    # Create map
    m = Map(
        center=[2.3522, 48.8566],  # Paris center
        zoom=13,
        title="Paris Cafes & Restaurants",
        tiles="carto-light",
    )

    # Add all components
    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(sidebar)
    m.add_component(feature_search)
    m.add_component(basemap_switcher)
    m.add_component(controls)

    # Enable embedding and compression
    m.embedded = True
    m.use_compression = True

    # Auto-fit to data extent
    # m.auto_extent()

    # Save map
    m.save(output_path)
    file_size_kb = output_path.stat().st_size / 1024
    print(f"✓ Map saved to {output_path.relative_to(script_dir)}")
    print(f"  File size: {file_size_kb:.1f} KB")


if __name__ == "__main__":
    main()
