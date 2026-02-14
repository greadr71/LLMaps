# LLMaps API Guide

LLM-friendly index of all LLMaps components for quick search and selection. Use grep on **Keywords** to find components by functionality.

## How to Use This Index

- **Keywords** — semantic tags for grep search
- **When to use** — selection criteria
- **Related** — components often used together
- **Alternatives** — other options by scenario

---

## Map and Core

| Component | Description | Keywords | When to use |
|-----------|-------------|----------|-------------|
| `Map` | Main map class; center, zoom, title, tiles | map, main, center, zoom, title, tiles | Creating a map, adding layers and components |
| `Map.add_layer()` | Attach a visual layer | layer, add_layer | After creating the map |
| `Map.add_component()` | Attach a UI component (legend, popup, controls) | component, add_component | After adding layers |
| `Map.enable_comparison(left_layers, right_layers)` | Before/after slider (two maps) | compare, comparison, swipe, before, after, slider | Visual comparison of two states |
| `Map.auto_extent()` | Set center/zoom from data bounds | auto_extent, bounds, fit | Fit map to data |
| `Map.save(path)` | Render and write HTML file | save, export, html | Output standalone HTML |
| `Map.to_html()` | Return HTML string | to_html, embed | Embed in another page or notebook |
| `Map.add_custom_js(js)` | Inject custom JS (str or Path) | custom_js, inject, javascript | Custom interactivity, event handlers |
| `Map.add_custom_css(css)` | Inject custom CSS (str or Path) | custom_css, inject, style | Custom styling, sidebar, overlays |
| `Map.add_custom_html(html)` | Inject custom HTML into body | custom_html, inject, sidebar, overlay | Sidebar panels, custom UI elements |
| `Map.embed_data(key, data)` | Embed JSON data as `window.llmapsData.<key>` | embed_data, user_data, json | Pass Python data to custom JS |
| `Map.embedded` | Inline data in HTML (works via file://) | embedded, inline, file | Static maps without a server |
| `Map.use_compression` | Geobuf + Gzip for embedded data | compression, geobuf, gzip | Reduce HTML size for large data |

**Related:** All layers, all sources, Legend, Popup, Controls

**Alternatives:** Use `embedded=True` for file://; use `ApiSource` for live data from URL.

---

## Layers

| Component | Description | Keywords | When to use |
|-----------|-------------|----------|-------------|
| `CircleLayer` | Points rendered as circles | points, markers, circles | &lt;10k points, point data |
| `FillLayer` | Polygons with fill and optional stroke; fill_color/fill_opacity accept expressions | polygons, fill, regions, zones, boundaries, choropleth, expressions, feature_state | Polygon data, districts, zones, dynamic coloring |
| `H3Layer` | Hexagonal grid (H3 aggregation: count/sum/mean/median) | h3, hexagon, aggregation, heatmap | &gt;100k points, density, aggregated data |
| `VectorTileLayer` | Mapbox Vector Tiles (PBF) | vector tiles, pbf, tiles, large data | Large datasets, on-demand loading |
| `BaseLayer` | Base class (id, source, visible, minzoom, maxzoom) | base, abstract | Custom layer implementations |

**Related:** FileSource, ApiSource, VectorTileSource, Legend, Popup

**Alternatives:**
- Points (&lt;10k): `CircleLayer`
- Points (&gt;100k): `H3Layer` with aggregation or `VectorTileLayer`
- Polygons: `FillLayer` or `VectorTileLayer` (PBF)

---

## Data Sources

| Component | Description | Keywords | When to use |
|-----------|-------------|----------|-------------|
| `FileSource` | Load from file (GeoJSON, CSV, Parquet) | file, geojson, csv, parquet | Local files, static data |
| `ApiSource` | Load GeoJSON from HTTP URL (frontend fetches) | api, http, rest, url, endpoint | External APIs, live data |
| `VectorTileSource` | Vector tile URL template ({z},{x},{y}) | vector tiles, pbf, tiles | Used with VectorTileLayer |
| `BaseSource` | Base class (id, to_dict) | base, abstract | Custom sources |
| `promote_id` | Feature property for id (keyword-only on all sources) | promote_id, promoteId, feature_state, setFeatureState | Dynamic highlighting, feature-state expressions |

**Related:** Map.add_layer(), CircleLayer, H3Layer, FillLayer

**Alternatives:**
- Local data: `FileSource`
- Remote/live: `ApiSource`
- Tiled vector data: `VectorTileSource`

---

## UI Components

| Component | Description | Keywords | When to use |
|-----------|-------------|----------|-------------|
| `Legend` | Legend with layer labels and optional toggles | legend, colorbar, scale, toggle | Show layer names, toggle visibility, layer_counts |
| `Popup` | Popup on click or hover (fields, field_labels, trigger, fields_by_layer) | popup, tooltip, click, hover, info | Display feature attributes on click or hover |
| `Sidebar` | Sliding panel with feature details (fields_by_layer, title_field, position) | sidebar, panel, detail, click, fields | Complex feature detail views, replaces popup for rich content |
| `FeatureSearch` | Search within map data by attributes (search_fields by source) | feature_search, search, attributes, dropdown, data | Find features by name/id/address within loaded data |
| `Search` | Address search (geocoder_url, autocomplete, zoom_on_result) | search, geocoding, address, autocomplete | Navigate to address via external geocoder |
| `Controls` | Zoom, scale bar, fullscreen | controls, zoom, scale, fullscreen | Standard map controls |

**Related:** Map.add_component(), layers (for Legend/Popup/Sidebar layer_ids)

**Alternatives:** Simple info: Popup; rich detail: Sidebar; data navigation: FeatureSearch; address navigation: Search.

---

## Tile Providers

| Provider | Description | Keywords | When to use |
|----------|-------------|----------|-------------|
| `osm` | OpenStreetMap | osm, openstreetmap | Default, international |
| `carto-light` | Carto Light basemap | carto, light | Light theme |
| `carto-dark` | Carto Dark basemap | carto, dark | Dark theme |
| `yandex` | Yandex Maps (placeholder URL) | yandex, tiles | Customise URL for your key |
| `2gis` | 2GIS (placeholder URL) | 2gis, tiles | Customise URL for your key |

**Related:** `Map(tiles="osm")`, `llmaps.tiles.resolve_tile_provider`, `list_tile_providers`

**Alternatives:** Use `tiles="osm"` or `"carto-light"` for neutral examples; replace placeholder URLs for Yandex/2GIS if needed.

---

## Optimizers

| Component | Description | Keywords | When to use |
|-----------|-------------|----------|-------------|
| Geobuf + Gzip | Compress embedded GeoJSON | compression, geobuf, gzip | Large embedded data, reduce HTML size |
| Visibility optimization | Free RAM/GPU when tab hidden | visibility, memory, performance | Embedded maps in multi-tab UIs |
| MULTIPOINT explosion | Async split of MULTIPOINT geometries | multipoint, explode, async | MULTIPOINT features |

**Related:** `Map(embedded=True, use_compression=True)`, `llmaps.optimizers.compression`

---

## Expressions

| Component | Description | Keywords | When to use |
|-----------|-------------|----------|-------------|
| `feature_state_color(state_key, color_ramp_key, color_stops, ...)` | Build `case` + `interpolate` expression for dynamic fill color by feature-state | feature_state, color, interpolate, expression, choropleth | Dynamic polygon coloring (click → recolor) |
| `feature_state_value(state_key, active, inactive, default)` | Build `case` expression returning numeric value by feature-state | feature_state, opacity, value, expression | Dynamic opacity/radius by state |
| `compute_color_stops(values, n_stops, colors, percentiles)` | Auto-compute color stops from data distribution (percentile-based) | color_stops, percentile, quantile, palette, auto | Generate color ramps from data for expressions or legends |

```python
from llmaps.expressions import feature_state_color, feature_state_value, compute_color_stops
```

**Related:** `FillLayer(fill_color=...)`, `promote_id`, `window.llmapsSetFeatureState()`

**When to use:** GPU-efficient dynamic styling — instant recoloring of thousands of polygons without re-uploading data. Requires `promote_id` on the source. Use `compute_color_stops()` to auto-generate thresholds from data.

---

## Frontend JS Utilities

Global functions available in custom JS (via `add_custom_js()`):

| Function | Description | Keywords | When to use |
|----------|-------------|----------|-------------|
| `window.llmapsGetSourceData(sourceId)` | Async: get GeoJSON data for a source (embedded/compressed/remote) | source_data, geojson, embedded | Access feature data in custom JS |
| `window.llmapsClearFeatureStates(sourceId)` | Clear all feature states on a source | feature_state, clear, highlight | Reset dynamic highlighting |
| `window.llmapsSetFeatureState(sourceId, featureId, state)` | Set feature state for GPU-side styling | feature_state, set, highlight | Dynamic polygon coloring |
| `window.llmapsOnLayersReady(fn)` | Register callback for when layers are loaded | ready, callback, layers | Run code after map is initialized |
| `window.llmapsData` | User-embedded data (via `embed_data()`) | data, user_data, json | Access Python data in JS |
| `window.llmapsSidebarOpen(layerId, feature)` | Open sidebar with feature details | sidebar, open, feature | Programmatic sidebar control |
| `window.llmapsSidebarClose()` | Close sidebar | sidebar, close | Programmatic sidebar control |

**Related:** `Map.add_custom_js()`, `Map.embed_data()`, `expressions.feature_state_color()`

---

## Quick Reference by Scenario

| Scenario | Components |
|----------|------------|
| Small dataset (&lt;10k points) | CircleLayer + FileSource + Legend |
| Large dataset (&gt;100k points) | H3Layer + FileSource + Legend (+ use_compression) |
| Polygons / choropleth | FillLayer + FileSource + Legend + Popup |
| Dynamic polygon coloring | FillLayer + expressions + promote_id + custom JS |
| Rich feature details | Sidebar + FillLayer/CircleLayer (replaces Popup for complex views) |
| Search within data | FeatureSearch (+ Sidebar for detail on select) |
| Hover tooltips | Popup(trigger="hover") + FillLayer/CircleLayer |
| Embedded map (no server) | Map(embedded=True, use_compression=True) + FileSource |
| Before/after comparison | Two layers + Map.enable_comparison(left_layers, right_layers) |
| Data from API | CircleLayer/FillLayer + ApiSource + Legend |
| Vector tiles | VectorTileLayer + VectorTileSource |

---

## Detailed Documentation

- [docs/api/map.md](docs/api/map.md) — Map class and methods
- [docs/api/layers.md](docs/api/layers.md) — Layer types and parameters
- [docs/api/sources.md](docs/api/sources.md) — Data sources
- [docs/api/components.md](docs/api/components.md) — UI components
- [docs/recipes/](docs/recipes/) — Heatmap, comparison, embedded map, feature-state highlighting
