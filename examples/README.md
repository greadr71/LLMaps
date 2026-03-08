# LLMaps Examples

Examples are split into two groups:
- Real-world examples with external/open datasets
- Technical examples focused on specific API patterns

## Structure

Each example is a self-contained project with:
- `prepare_data.py` - optional data download/prepare step for real-world datasets
- `build_map.py` - builds an interactive map with llmaps
- `map.html` or custom output HTML files
- `data/` - downloaded/processed data (mostly gitignored)

## Technical Examples

### 1. [Dashboard Primitives](technical/dashboard/)

**Features**: Dashboard, filter bar, custom JS bridge, CircleLayer

A minimal example of a persistent dashboard panel attached to the map viewport. Demonstrates:
- First-class `Dashboard` component added via `Map.add_component()`
- Declarative select, date, and text filters
- Frontend event bridge via `llmaps:dashboard-filter-change`
- Dynamic content updates with `window.llmapsDashboardSetContent()`

**Data**: Small embedded GeoJSON with sample cities

**Run**:
```bash
cd technical/dashboard
python build_map.py
open map.html
```

## Real-World Examples

### 1. [Paris Cafes & Restaurants](real-world/cafes/)

**Features**: CircleLayer, Search, FeatureSearch, BasemapSwitcher, Popup, Sidebar

An interactive map of cafes and restaurants in Paris from OpenStreetMap.

**Data**: OpenStreetMap via Overpass API (~2000 POIs, 300KB)

**Run**:
```bash
cd real-world/cafes
python prepare_data.py
python build_map.py
open map.html
```

**Live demo**: [View map](https://greadr71.github.io/llmaps/examples/real-world/cafes/map.html)

---

### 2. [World Population](real-world/world_population/)

**Features**: FillLayer, feature-state expressions, Jenks classification, color ramps

A choropleth map of world countries colored by population.

**Data**: Natural Earth 110m Countries (210KB, public domain)

**Run**:
```bash
cd real-world/world_population
python prepare_data.py
python build_map.py
open map.html
```

**Live demo**: [View map](https://greadr71.github.io/llmaps/examples/real-world/world_population/map.html)

---

### 3. [Global Earthquakes](real-world/earthquakes/)

**Features**: CircleLayer with interpolate expressions, Jenks classification, Sidebar

A map of magnitude 5.0+ earthquakes from 2021-2026 with depth visualization.

**Data**: USGS Earthquake Hazards Program (real-time API, ~500KB)

**Run**:
```bash
cd real-world/earthquakes
python prepare_data.py
python build_map.py
open map.html
```

**Live demo**: [View map](https://greadr71.github.io/llmaps/examples/real-world/earthquakes/map.html)

---

### 4. [Pennsylvania Gerrymandering Story](real-world/gerrymandering/)

**Features**: FillLayer, Storytelling, SceneComparison, Popup, custom overlays

A scrollytelling map explaining how district boundaries in Pennsylvania affected
Congressional representation before and after the 2018 court-ordered redistricting.

**Data**: Pennsylvania congressional districts and election results (2016/2018), open sources

**Run**:
```bash
cd real-world/gerrymandering
python build_map.py                # builds EN + RU
python build_map.py --locale en    # English only
python build_map.py --locale ru    # Russian only
open gerrymandering_en.html
```

**Live demos**:
- EN: [View map](https://greadr71.github.io/llmaps/examples/real-world/gerrymandering/gerrymandering_en.html)
- RU: [View map](https://greadr71.github.io/llmaps/examples/real-world/gerrymandering/gerrymandering_ru.html)

## API Coverage

| Feature | Examples |
|---------|----------|
| `CircleLayer` | technical/dashboard, real-world/cafes, real-world/earthquakes |
| `FillLayer` | real-world/world_population, real-world/gerrymandering |
| `Legend` | all examples |
| `Popup` | all examples |
| `Storytelling` | real-world/gerrymandering |
| `Sidebar` | real-world/cafes, real-world/world_population, real-world/earthquakes |
| `Dashboard` | technical/dashboard |
| `Controls` | all examples |
| `Search` (geocoding) | real-world/cafes |
| `FeatureSearch` | real-world/cafes |
| `BasemapSwitcher` | real-world/cafes |
| `match` expressions | real-world/cafes |
| `interpolate` expressions | real-world/earthquakes |
| `feature_state_color` | real-world/world_population |
| `compute_color_stops` | real-world/world_population, real-world/earthquakes |
| `FileSource` (GeoJSON) | technical/dashboard, real-world/cafes, real-world/world_population, real-world/earthquakes, real-world/gerrymandering |
| Light themes (`osm`, `carto-light`) | real-world/cafes, real-world/world_population |
| Dark theme (`carto-dark`) | real-world/earthquakes |
| Embedded mode | all examples |
| `auto_extent()` | real-world/cafes |

## GitHub Pages

All examples are published at: [https://greadr71.github.io/llmaps/examples/](https://greadr71.github.io/llmaps/examples/)

See [index.html](index.html) for an interactive gallery.

## Data Licenses

All examples use open data:
- OpenStreetMap: ODbL
- Natural Earth: Public Domain
- USGS: Public Domain

## Requirements

```bash
pip install llmaps
```

## Contributing

Want to add a new example?
1. Choose a category: `examples/technical/` or `examples/real-world/`
2. Create a new directory under that category
3. Add `prepare_data.py` (optional for technical examples) and `build_map.py`
4. Update this README and `examples/index.html`
5. Submit a PR
