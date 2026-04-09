"""Build an interactive map of global earthquakes with depth and magnitude visualization.

This example demonstrates:
- CircleLayer with MapLibre interpolate expressions for radius and color
- compute_color_stops with Jenks natural breaks classification
- Legend with color ramp for depth visualization
- Popup with hover trigger
- Sidebar with comprehensive earthquake information
- Embedded mode with compression
- Dark theme basemap
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup, Sidebar
from llmaps.expressions import compute_color_stops
from llmaps.layers.circle import CircleLayer
from llmaps.sources.file import FileSource


def main() -> None:
    """Build the earthquake map."""
    # Define paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    input_path = data_dir / "earthquakes_2021_2026.geojson"
    processed_path = data_dir / "earthquakes_with_depth.geojson"
    output_path = script_dir / "map.html"
    
    # Verify input exists
    if not input_path.exists():
        print(f"Error: {input_path} not found. Run prepare_data.py first.")
        return

    # Load GeoJSON and enrich with depth and formatted time
    print("Processing earthquake data...")
    with open(input_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    for feature in geojson_data["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        # Extract depth from coordinates (third dimension)
        if len(coords) > 2:
            props["depth"] = coords[2]
        else:
            props["depth"] = 0

        # Format timestamp for display
        ts = props.get("time")
        if ts is not None:
            dt = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
            props["time_readable"] = dt.strftime("%Y-%m-%d %H:%M UTC")
        else:
            props["time_readable"] = ""

    # Save processed GeoJSON
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f)
        
    print(f"✓ Processed {len(geojson_data['features'])} earthquakes")

    # Create data source
    source = FileSource(
        id="earthquakes", 
        path=str(processed_path)
    )

    # Create MapLibre expression for radius interpolation
    # Magnitude 5→3px, 6→8px, 7→20px, 8→40px
    radius_expr = [
        "interpolate",
        ["linear"],
        ["get", "mag"],
        5, 3,
        6, 8,
        7, 20,
        8, 40,
    ]

    # Compute color stops for depth using Jenks natural breaks
    depths = [f["properties"]["depth"] for f in geojson_data["features"]]
    color_stops = compute_color_stops(
        depths,
        method="jenks",
        palette="arctic-chill",
        n_stops=5,
    )
    
    print(f"\nColor stops (depth in km):")
    for value, color in color_stops:
        print(f"  {value:6.1f} km → {color}")

    # Create MapLibre expression for color interpolation
    color_expr = ["interpolate", ["linear"], ["get", "depth"]]
    for value, color in color_stops:
        color_expr.extend([value, color])

    # Create circle layer
    layer = CircleLayer(
        id="earthquakes-layer",
        source=source,
        radius=radius_expr,
        color=color_expr,
        opacity=0.8,
    )

    # Create legend with color ramp
    legend = Legend(
        position="top-right",
        show_toggle=True,
        layer_labels={"earthquakes-layer": "Earthquake epicenters"},
        layer_descriptions={
            "earthquakes-layer": "Size = magnitude; Color = depth",
        },
        layer_color_ramps={
            "earthquakes-layer": {
                "stops": [[v, c] for v, c in color_stops],
                "label_min": f"{color_stops[0][0]:.0f} km (shallow)",
                "label_max": f"{color_stops[-1][0]:.0f}+ km (deep)",
            }
        },
    )

    # Create popup (hover trigger)
    popup = Popup(
        trigger="hover",
        fields=["place", "mag", "depth", "time_readable", "alert", "tsunami"],
        field_labels={
            "place": "Location",
            "mag": "Magnitude",
            "depth": "Depth (km)",
            "time_readable": "Date",
            "alert": "Alert",
            "tsunami": "Tsunami",
        },
    )

    # Create sidebar (click trigger with full details)
    sidebar = Sidebar(
        position="right",
        width=400,
        title_field="title",
        fields_by_layer={
            "earthquakes-layer": [
                "title",
                "place",
                "mag",
                "depth",
                "time_readable",
                "alert",
                "tsunami",
                "felt",
                "mmi",
                "sig",
                "status",
                "magType",
                "url",
            ]
        },
        field_labels={
            "title": "Title",
            "place": "Location",
            "mag": "Magnitude",
            "depth": "Depth (km)",
            "time_readable": "Time (UTC)",
            "alert": "Alert",
            "tsunami": "Tsunami",
            "felt": "Felt reports",
            "mmi": "MMI",
            "sig": "Significance",
            "status": "Status",
            "magType": "Mag type",
            "url": "USGS link",
        },
    )

    # Create controls
    controls = Controls(
        zoom=True,
        scale=True,
        fullscreen=True
    )

    # Create map
    m = Map(
        center=[0, 0],
        zoom=2,
        title="Global Earthquakes 2021-2026 (M5.0+)",
        tiles="carto-dark",
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
    print(f"\n✓ Map saved to {output_path.relative_to(script_dir)}")
    print(f"  File size: {file_size_kb:.1f} KB")


if __name__ == "__main__":
    main()
