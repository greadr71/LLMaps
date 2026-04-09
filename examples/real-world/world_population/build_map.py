"""Build an interactive world population map.

This example demonstrates:
- FillLayer with feature-state for GPU-efficient styling
- Jenks natural breaks classification for choropleth mapping
- Color ramps in Legend
- Detailed Sidebar with country statistics
"""

import json
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup, Sidebar
from llmaps.expressions import compute_color_stops, feature_state_color
from llmaps.layers import FillLayer
from llmaps.sources import FileSource


def main():
    """Build the map."""
    # Define paths
    script_dir = Path(__file__).parent
    data_path = script_dir / "data" / "countries.geojson"
    output_path = script_dir / "map.html"

    # Verify data exists
    if not data_path.exists():
        print(f"Error: {data_path} not found. Run prepare_data.py first.")
        return

    # Load data to compute statistics
    with open(data_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    
    # Extract population values for classification
    # Filter out -99 or null values often found in NE data
    populations = [
        f["properties"]["POP_EST"] 
        for f in geojson["features"] 
        if f["properties"].get("POP_EST", 0) > 0
    ]
    
    # Compute color stops using Jenks natural breaks.
    # Uses a warm-to-cool palette suitable for density mapping.
    n_stops = 7
    color_stops = compute_color_stops(
        populations, 
        method="jenks", 
        palette="crameri-lajolla",
        n_stops=n_stops
    )
    
    print("Population classification breaks:")
    for val, color in color_stops:
        print(f"  {val:15,.0f} -> {color}")
    
    # Format values for legend labels
    min_val_formatted = f"{color_stops[0][0]:,.0f}"
    max_val_formatted = f"{color_stops[-1][0]:,.0f}"

    # Create data source
    # Important: promote_id="ISO_A3" tells MapLibre to use the ISO_A3 property
    # as the feature ID. This is required for feature-state to work.
    source = FileSource(
        id="countries", 
        path=str(data_path),
        promote_id="ISO_A3"
    )

    # Create FillLayer using feature-state for color.
    # feature_state dict tells the library to automatically call
    # map.setFeatureState for each feature after source loading:
    #   "active": True        -> constant, every feature gets active=true
    #   "color": "POP_EST"    -> reads POP_EST property from each GeoJSON feature
    layer = FillLayer(
        id="population-layer",
        source=source,
        fill_color=feature_state_color(
            state_key="active",
            color_ramp_key="color",
            color_stops=color_stops,
            inactive="#f0f0f0",
            default="#e0e0e0"
        ),
        fill_opacity=0.8,
        stroke_color="#ffffff",
        stroke_width=0.5,
        feature_state={
            "active": True,
            "color": "POP_EST",
        },
    )

    # Create Legend
    legend = Legend(
        title="World Population",
        description="Estimated population by country",
        position="bottom-left",
        layer_labels={
            "population-layer": "Population",
        },
        layer_color_ramps={
            "population-layer": {
                "stops": [[v, c] for v, c in color_stops],
                "label_min": min_val_formatted,
                "label_max": max_val_formatted,
            }
        }
    )

    # Create Popup (hover)
    popup = Popup(
        trigger="hover",
        fields=["NAME", "POP_EST", "CONTINENT"],
        field_labels={
            "NAME": "Country",
            "POP_EST": "Population",
            "CONTINENT": "Continent"
        }
    )

    # Create Sidebar (click)
    sidebar = Sidebar(
        title_field="NAME",
        fields_by_layer={
            "population-layer": [
                "POP_EST",
                "GDP_MD",
                "CONTINENT",
                "INCOME_GRP",
                "ECONOMY",
                "ISO_A3"
            ]
        },
        field_labels={
            "POP_EST": "Population",
            "GDP_MD": "GDP (Million $)",
            "CONTINENT": "Continent",
            "INCOME_GRP": "Income Group",
            "ECONOMY": "Economy",
            "ISO_A3": "ISO Code"
        }
    )

    # Create Controls
    controls = Controls(
        zoom=True,
        scale=True,
        fullscreen=True,
    )

    # Create Map
    m = Map(
        center=[0, 20],
        zoom=2,
        title="World Population Map",
        tiles="carto-light"  # Light theme works well with choropleth
    )

    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(sidebar)
    m.add_component(controls)
    
    m.embedded = True
    m.use_compression = True

    # Save
    m.save(output_path)
    file_size_kb = output_path.stat().st_size / 1024
    print(f"✓ Map saved to {output_path.relative_to(script_dir)}")
    print(f"  File size: {file_size_kb:.1f} KB")


if __name__ == "__main__":
    main()
