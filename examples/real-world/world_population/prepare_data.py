"""Download and prepare world population data from Natural Earth.

This script fetches the 110m Admin-0 Countries dataset from Natural Earth,
extracts population and economic indicators, and saves it as GeoJSON.

Data source: Natural Earth
License: Public Domain
"""

import json
import zipfile
import io
from pathlib import Path

import requests


def read_shapefile_to_geojson(shp_path):
    """Read a shapefile and convert to GeoJSON using fiona."""
    try:
        import fiona
        from shapely.geometry import mapping
    except ImportError:
        print("Error: fiona and shapely are required.")
        print("Install with: pip install fiona shapely")
        raise
    
    features = []
    with fiona.open(shp_path) as src:
        for feature in src:
            features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


def main():
    """Download and process Natural Earth data."""
    # Define paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    output_path = data_dir / "countries.geojson"
    
    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)

    # URL for Natural Earth 110m Cultural Vectors - Admin 0 - Countries
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    
    print("Downloading Natural Earth data...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # Extract Shapefile from ZIP in memory
    print("Extracting shapefile...")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Find the .shp file
        shp_file = next(f for f in z.namelist() if f.endswith(".shp"))
        
        # Extract all files to data_dir
        z.extractall(data_dir)
    
    # Read the shapefile using fiona
    print("Converting to GeoJSON...")
    shp_path = data_dir / shp_file
    geojson_data = read_shapefile_to_geojson(shp_path)
    
    # Columns to keep (attributes for map)
    keep_columns = {
        "NAME",          # Country name
        "POP_EST",       # Population estimate
        "GDP_MD",        # GDP (Million Dollars)
        "CONTINENT",     # Continent
        "INCOME_GRP",    # Income group
        "ECONOMY",       # Economy type
        "ISO_A3",        # ISO 3-letter code (for promote_id)
    }
    
    # Filter attributes
    for feature in geojson_data["features"]:
        props = feature.get("properties", {})
        # Keep only selected columns
        filtered_props = {k: props.get(k) for k in keep_columns if k in props}
        feature["properties"] = filtered_props
    
    # Save to GeoJSON
    print(f"Saving to {output_path.relative_to(script_dir)}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f)
    
    # Clean up extracted shapefiles (shp, shx, dbf, prj, etc.)
    for f in data_dir.glob("ne_110m_admin_0_countries.*"):
        if f.name != "countries.geojson":
            f.unlink()
            
    print("✓ Done!")
    print(f"  Total countries: {len(geojson_data['features'])}")
    
    # Print sample
    if geojson_data['features']:
        row = geojson_data['features'][0]['properties']
        print(f"\nSample country:")
        print(f"  Name: {row.get('NAME', 'N/A')}")
        pop = row.get('POP_EST')
        gdp = row.get('GDP_MD')
        if pop:
            print(f"  Population: {pop:,.0f}")
        if gdp:
            print(f"  GDP: ${gdp:,.0f}M")
