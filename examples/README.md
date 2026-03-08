# LLMaps Examples

Real-world examples demonstrating the full capabilities of the llmaps library.

## Overview

Each example is a self-contained project with:
- `prepare_data.py` — downloads/prepares real-world GIS data
- `build_map.py` — builds an interactive map with llmaps
- `map.html` — ready-to-open output (embedded data)
- `data/` — downloaded/processed data (gitignored)

All examples use real data from open sources and demonstrate different layers, components, and visualization techniques.

## Examples

### 1. [Paris Cafes & Restaurants](cafes/)

**Features**: CircleLayer, Search, FeatureSearch, BasemapSwitcher, Popup, Sidebar

An interactive map of cafes and restaurants in Paris from OpenStreetMap. Demonstrates:
- Conditional styling with MapLibre `match` expressions
- Geocoding search and feature attribute search
- Basemap switcher for different tile providers
- Hover popup and detailed sidebar

**Data**: OpenStreetMap via Overpass API (~2000 POIs, 300KB)

**Run**:
```bash
cd cafes
python prepare_data.py
python build_map.py
open map.html
```

**Live demo**: [View map](https://greadr71.github.io/llmaps/examples/cafes/map.html)

---

### 2. [World Population](world_population/)

**Features**: FillLayer, feature-state expressions, Jenks classification, color ramps

A choropleth map of world countries colored by population. Demonstrates:
- GPU-efficient feature-state styling for polygons
- Jenks natural breaks classification
- `compute_color_stops` with matplotlib colormaps
- Legend with color ramp visualization

**Data**: Natural Earth 110m Countries (210KB, public domain)

**Run**:
```bash
cd world_population
python prepare_data.py
python build_map.py
open map.html
```

**Live demo**: [View map](https://greadr71.github.io/llmaps/examples/world_population/map.html)

---

### 3. [NYC Taxi Heatmap](taxi_heatmap/)

**Features**: H3Layer, hexagonal aggregation, embedded mode

A hexagonal heatmap of NYC taxi pickups. Demonstrates:
- H3 hexagonal binning and aggregation
- CSV data source support
- Dark theme basemap
- Embedded mode with compression

**Data**: NYC TLC Yellow Taxi (January 2015 sample, 10K trips, 500KB)

**Run**:
```bash
cd taxi_heatmap
python prepare_data.py  # Downloads ~40MB, creates 500KB sample
python build_map.py
open map.html
```

**Live demo**: [View map](https://greadr71.github.io/llmaps/examples/taxi_heatmap/map.html)

---

### 4. [Global Earthquakes](earthquakes/)

**Features**: CircleLayer with interpolate expressions, Jenks classification, Sidebar

A map of magnitude 5.0+ earthquakes from 2021-2026 with depth visualization. Demonstrates:
- MapLibre `interpolate` expressions for radius and color
- Jenks natural breaks for depth classification
- `plasma_r` colormap for depth gradient
- Comprehensive sidebar with 12+ fields
- Hover popup for quick info

**Data**: USGS Earthquake Hazards Program (real-time API, ~500KB)

**Run**:
```bash
cd earthquakes
python prepare_data.py
python build_map.py
open map.html
```

**Live demo**: [View map](https://greadr71.github.io/llmaps/examples/earthquakes/map.html)

---

### 5. [Pennsylvania Gerrymandering Story](gerrymandering/)

**Features**: FillLayer, Storytelling, SceneComparison, Popup, custom overlays

A scrollytelling map explaining how district boundaries in Pennsylvania affected
Congressional representation before and after the 2018 court-ordered redistricting.
Demonstrates:
- Storytelling scenes with camera transitions and layer visibility control
- Before/after swipe comparison for district maps (2016 vs 2018)
- Highlighted districts for packing/cracking explanations
- Custom HTML/CSS/JS overlays integrated into the map output
- Locale-specific builds for English and Russian

**Data**: Pennsylvania congressional districts and election results (2016/2018), open sources

**Run**:
```bash
cd gerrymandering
python build_map.py                # builds EN + RU
python build_map.py --locale en    # English only
python build_map.py --locale ru    # Russian only
open gerrymandering_en.html
```

**Live demos**:
- EN: [View map](https://greadr71.github.io/llmaps/examples/gerrymandering/gerrymandering_en.html)
- RU: [View map](https://greadr71.github.io/llmaps/examples/gerrymandering/gerrymandering_ru.html)

---

### 6. [Dashboard Primitives](dashboard/)

**Features**: Dashboard, filter bar, custom JS bridge, CircleLayer

A minimal example of a persistent dashboard panel attached to the map viewport. Demonstrates:
- First-class `Dashboard` component added through `Map.add_component()`
- Declarative select, date, and text filters
- Frontend event bridge via `llmaps:dashboard-filter-change`
- Dynamic content updates with `window.llmapsDashboardSetContent()`

**Data**: Small embedded GeoJSON with a few sample cities

**Run**:
```bash
cd dashboard
python build_map.py
open map.html
```

---

## API Coverage

Every public feature of llmaps is demonstrated across these examples:

| Feature | Examples |
|---------|----------|
| **Layers** |
| `CircleLayer` | cafes, earthquakes |
| `FillLayer` | world_population |
| `H3Layer` | taxi_heatmap |
| **Components** |
| `Legend` | all examples |
| `Popup` | all examples |
| `Storytelling` | gerrymandering |
| `Sidebar` | cafes, world_population, earthquakes |
| `Dashboard` | dashboard |
| `Controls` | all examples |
| `Search` (geocoding) | cafes |
| `FeatureSearch` | cafes |
| `BasemapSwitcher` | cafes |
| **Expressions** |
| `match` expressions | cafes |
| `interpolate` expressions | earthquakes |
| `feature_state_color` | world_population |
| `compute_color_stops` | world_population, earthquakes |
| **Sources** |
| `FileSource` (GeoJSON) | cafes, world_population, earthquakes |
| `FileSource` (CSV) | taxi_heatmap |
| **Themes** |
| Light themes (`osm`, `carto-light`) | cafes, world_population |
| Dark theme (`carto-dark`) | taxi_heatmap, earthquakes |
| **Modes** |
| Embedded + compression | all examples |
| `auto_extent()` | cafes, taxi_heatmap |

---

## GitHub Pages

All examples are published at: [https://greadr71.github.io/llmaps/examples/](https://greadr71.github.io/llmaps/examples/)

See [index.html](index.html) for an interactive gallery.

---

## Data Licenses

All examples use open data:
- **OpenStreetMap**: ODbL (Open Database License)
- **Natural Earth**: Public Domain
- **NYC TLC**: Public Domain
- **USGS**: Public Domain

---

## Requirements

```bash
pip install llmaps
```

---

## Contributing

Want to add a new example? Follow the pattern:
1. Create a new directory in `examples/`
2. Add `prepare_data.py` and `build_map.py`
3. Update this README with description
4. Submit a PR!
