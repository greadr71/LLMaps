"""Earthquakes map with depth and magnitude interpolation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Legend, Popup, Sidebar
from llmaps.layers.circle import CircleLayer
from llmaps.sources.file import FileSource


def main() -> None:
    examples_dir = Path(__file__).resolve().parent
    data_dir = examples_dir / "data"
    input_path = data_dir / "earthquakes_2021_2026.geojson"
    output_geojson_path = examples_dir / "earthquakes_with_depth.geojson"
    output_map_path = examples_dir / "earthquakes_map.html"

    # Load GeoJSON and add depth + formatted time to properties
    with open(input_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    for feature in geojson_data["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        if len(coords) > 2:
            props["depth"] = coords[2]
        else:
            props["depth"] = 0
        # Formatted date for popup and sidebar (time is Unix ms)
        ts = props.get("time")
        if ts is not None:
            dt = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
            props["time_readable"] = dt.strftime("%Y-%m-%d %H:%M UTC")
        else:
            props["time_readable"] = ""

    # Save updated GeoJSON with depth and time_readable
    with open(output_geojson_path, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f)

    # Create data source
    source = FileSource(id="earthquakes", path=str(output_geojson_path))

    # Create MapLibre expressions for interpolation
    # Radius interpolation: mag 5→3px, 6→8px, 7→20px, 8→40px
    radius_expr = ["interpolate", ["linear"], ["get", "mag"], 5, 3, 6, 8, 7, 20, 8, 40]

    # Color interpolation (plasma): depth 0→yellow (shallow), 700→dark blue (deep)
    color_expr = [
        "interpolate",
        ["linear"],
        ["get", "depth"],
        0,
        "#f0f921",  # shallow - bright yellow
        150,
        "#fca636",  # orange
        300,
        "#e16462",  # red
        500,
        "#b12a90",  # purple
        700,
        "#0d0887",  # deep - dark blue
    ]

    # Create circle layer with interpolated properties
    layer = CircleLayer(
        id="earthquakes-layer",
        source=source,
        radius=radius_expr,
        color=color_expr,
        opacity=0.8,
    )

    # Create legend
    legend = Legend(
        position="top-right",
        show_toggle=True,
        layer_labels={"earthquakes-layer": "Earthquake epicenters"},
        layer_descriptions={
            "earthquakes-layer": "Size — magnitude; color — epicenter depth",
        },
        layer_color_ramps={
            "earthquakes-layer": {
                "stops": [[0, "#f0f921"], [150, "#fca636"], [300, "#e16462"], [500, "#b12a90"], [700, "#0d0887"]],
                "label_min": "0 km (shallow)",
                "label_max": "700+ km (deep)",
            }
        },
    )

    # Popup on hover: formatted date required, plus place, mag, depth, alert, tsunami
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

    # Sidebar on click: full details
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
    controls = Controls(zoom=True, scale=True, fullscreen=True)

    # Create map and add components
    m = Map(center=[0, 0], zoom=2, title="Earthquakes 2021-2026", tiles="carto-dark")
    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(sidebar)
    m.add_component(controls)

    # Auto-fit map to data bounds
    # m.auto_extent()  # Временно отключено из-за PROJ database issue

    # Save with embedded data and compression
    m.embedded = True
    m.use_compression = True
    m.save(output_map_path)

    print(f"Map saved to {output_map_path}")
    print(f"GeoJSON with depth saved to {output_geojson_path}")


if __name__ == "__main__":
    main()
