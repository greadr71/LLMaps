"""Download earthquake data from USGS API.

This script fetches earthquake data (magnitude 5.0+) from 2021 to present
from the USGS Earthquake Hazards Program.

Data source: USGS Earthquake Hazards Program
License: Public Domain
"""

import json
import urllib.request
from pathlib import Path


def main():
    """Download earthquake data from USGS."""
    # USGS FDSN Event Web Service
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query?"
        "format=geojson&"
        "starttime=2021-01-01&"
        "endtime=2026-02-15&"
        "minmagnitude=5.0&"
        "orderby=magnitude"
    )

    # Define paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    output_file = data_dir / "earthquakes_2021_2026.geojson"

    print("Downloading earthquake data from USGS...")
    with urllib.request.urlopen(url) as response:
        data = response.read()

    output_file.write_bytes(data)

    # Load and print summary
    geojson = json.loads(data)
    num_features = len(geojson.get("features", []))
    file_size_kb = len(data) / 1024

    print(f"✓ Saved to {output_file.relative_to(script_dir)}")
    print(f"  File size: {file_size_kb:.1f} KB")
    print(f"  Total earthquakes: {num_features}")

    if num_features > 0:
        # Print sample
        sample = geojson["features"][0]
        print(f"\nMost recent earthquake:")
        print(f"  Location: {sample['properties'].get('place')}")
        print(f"  Magnitude: {sample['properties'].get('mag')}")


if __name__ == "__main__":
    main()
