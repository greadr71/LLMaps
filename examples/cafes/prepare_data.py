"""Download cafe and restaurant data from OpenStreetMap via Overpass API.

This script fetches cafes and restaurants in Paris from OpenStreetMap
and converts the data into a GeoJSON FeatureCollection format suitable
for use with llmaps.

Data source: OpenStreetMap via Overpass API
License: ODbL (Open Database License)
"""

import json
from pathlib import Path

import requests


def fetch_paris_cafes():
    """Fetch cafes and restaurants in Paris from Overpass API."""
    # Overpass QL query
    # Search for cafes and restaurants in Paris administrative area
    query = """
    [out:json][timeout:60];
    area["name"="Paris"]["admin_level"="8"]->.paris;
    (
      node(area.paris)["amenity"="cafe"];
      node(area.paris)["amenity"="restaurant"];
    );
    out body;
    """

    print("Fetching data from Overpass API...")
    response = requests.get(
        "https://overpass-api.de/api/interpreter",
        params={"data": query},
        timeout=90,
    )
    response.raise_for_status()

    data = response.json()
    print(f"✓ Received {len(data['elements'])} POIs from Overpass API")

    return data


def convert_to_geojson(osm_data):
    """Convert OSM JSON to GeoJSON FeatureCollection."""
    features = []

    for element in osm_data["elements"]:
        if element["type"] != "node":
            continue

        lon = element["lon"]
        lat = element["lat"]
        tags = element.get("tags", {})

        # Extract relevant properties
        properties = {
            "name": tags.get("name", "Unnamed"),
            "amenity": tags.get("amenity", "unknown"),
            "cuisine": tags.get("cuisine"),
            "opening_hours": tags.get("opening_hours"),
            "website": tags.get("website"),
            "phone": tags.get("phone"),
            "addr_street": tags.get("addr:street"),
            "addr_housenumber": tags.get("addr:housenumber"),
            "outdoor_seating": tags.get("outdoor_seating"),
        }

        # Remove None values to keep GeoJSON clean
        properties = {k: v for k, v in properties.items() if v is not None}

        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": properties,
        }

        features.append(feature)

    geojson = {"type": "FeatureCollection", "features": features}

    print(f"✓ Converted to GeoJSON with {len(features)} features")
    return geojson


def main():
    """Main execution function."""
    # Define paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    output_path = data_dir / "paris_cafes.geojson"

    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)

    # Fetch and convert data
    osm_data = fetch_paris_cafes()
    geojson = convert_to_geojson(osm_data)

    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    file_size_kb = output_path.stat().st_size / 1024
    print(f"✓ Saved to {output_path.relative_to(script_dir)}")
    print(f"  File size: {file_size_kb:.1f} KB")
    print(f"  Total features: {len(geojson['features'])}")

    # Print sample feature
    if geojson["features"]:
        sample = geojson["features"][0]
        print(f"\nSample feature:")
        print(f"  Name: {sample['properties'].get('name')}")
        print(f"  Type: {sample['properties'].get('amenity')}")
        print(f"  Cuisine: {sample['properties'].get('cuisine', 'N/A')}")


if __name__ == "__main__":
    main()
