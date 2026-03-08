import urllib.request, json
from pathlib import Path

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2021-01-01&endtime=2026-02-15&minmagnitude=5.0&orderby=magnitude"
project_dir = Path(__file__).resolve().parent
(project_dir / "data").mkdir(parents=True, exist_ok=True)
output_file = project_dir / "data" / "earthquakes_2021_2026.geojson"
print("Downloading...")
with urllib.request.urlopen(url) as r:
    data = r.read()
    output_file.write_bytes(data)
print(f"Saved: {output_file}")
