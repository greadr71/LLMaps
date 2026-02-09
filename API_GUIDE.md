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
| `Map.embedded` | Inline data in HTML (works via file://) | embedded, inline, file | Static maps without a server |
| `Map.use_compression` | Geobuf + Gzip for embedded data | compression, geobuf, gzip | Reduce HTML size for large data |

**Related:** All layers, all sources, Legend, Popup, Controls

**Alternatives:** Use `embedded=True` for file://; use `ApiSource` for live data from URL.

---

## Layers

| Component | Description | Keywords | When to use |
|-----------|-------------|----------|-------------|
| `CircleLayer` | Points rendered as circles | points, markers, circles | &lt;10k points, point data |
| `FillLayer` | Polygons with fill and optional stroke | polygons, fill, regions, zones, boundaries, choropleth | Polygon data, districts, zones |
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
| `Popup` | Popup on click (fields, field_labels, template, fields_by_layer) | popup, tooltip, click, info | Display feature attributes on click |
| `Search` | Address search (geocoder_url, autocomplete, zoom_on_result) | search, geocoding, address, autocomplete | Navigate to address |
| `Controls` | Zoom, scale bar, fullscreen | controls, zoom, scale, fullscreen | Standard map controls |

**Related:** Map.add_component(), layers (for Legend/Popup layer_ids)

**Alternatives:** Minimal map: Legend only; interactive: Legend + Popup + Controls; full: add Search.

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

## Quick Reference by Scenario

| Scenario | Components |
|----------|------------|
| Small dataset (&lt;10k points) | CircleLayer + FileSource + Legend |
| Large dataset (&gt;100k points) | H3Layer + FileSource + Legend (+ use_compression) |
| Polygons / choropleth | FillLayer + FileSource + Legend + Popup |
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
- [docs/recipes/](docs/recipes/) — Heatmap, comparison, embedded map
