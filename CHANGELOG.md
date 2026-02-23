# Changelog

All notable changes to this project will be documented in this file.

## 0.5.0 - Storytelling

- **Added:** `Storytelling` component — scrollytelling narrative panel with scroll-driven map reactions (camera, layers, highlights). Uses Scrollama.
- **Added:** `Scene` dataclass — defines a single step in a storytelling narrative (title, content, center, zoom, visible layers, feature highlights).
- **Added:** Clickable navigation dots with tooltips for quick scene access.
- **Added:** Responsive layout — narrative panel collapses below map on mobile.
- **Fixed:** `BaseLayer(visible=False)` now correctly hides layers at initialization (previously `visible` was only used by legend toggles).

## 0.4.0 - New components (A1, A2, A4, C1)

- **Added:** `Sidebar` component — sliding side panel for feature details on click. Configurable fields per layer, title, position, width. Takes priority over Popup. Exposes `window.llmapsSidebarOpen/Close` JS API.
- **Added:** `FeatureSearch` component — search within map data by feature attributes (not a geocoder). Dropdown with debounce, flyTo/fitBounds on select, integrates with Sidebar.
- **Added:** `Popup(trigger="hover")` — hover mode for popups. Popup follows cursor and disappears on mouseleave.
- **Added:** `compute_color_stops(values, n_stops, colors, percentiles)` in `expressions` — auto-compute color ramp thresholds from data distributions using percentiles (numpy).

## 0.3.0 - Infrastructure improvements (B3–B5)

- **Added:** `Map.add_custom_js(js)` — inject custom JavaScript (string or `Path` to file).
- **Added:** `Map.add_custom_css(css)` — inject custom CSS (string or `Path` to file).
- **Added:** `Map.add_custom_html(html)` — inject custom HTML into `<body>`.
- **Added:** `Map.embed_data(key, data)` — embed arbitrary JSON data as `window.llmapsData.<key>`.
- **Added:** `window.llmapsGetSourceData(sourceId)` — public JS utility to access GeoJSON data from embedded/compressed/remote sources.

## 0.2.0 - Feature-state support (B1, B2, A3)

- **Fixed:** `llmapsOnLayersReady` — now an event queue (multiple callbacks supported).
- **Added:** `promoteId` support in sources (`promote_id` parameter on `BaseSource`).
- **Added:** `FillLayer` now accepts expressions for `fill_color` and `fill_opacity`.
- **Added:** `expressions.feature_state_color()` and `expressions.feature_state_value()` helpers.
- **Added:** `window.llmapsClearFeatureStates()` and `window.llmapsSetFeatureState()` JS utilities.

## 0.1.1 - FillLayer outline fix

- **Fixed:** FillLayer now uses correct MapLibre property `fill-outline-color` instead of invalid `outline-color`/`outline-width`.
- **Added:** For `stroke_width > 1`, an additional line layer `{id}-outline` is automatically generated.
- **Docs:** Updated `docs/api/layers.md` with note about stroke_width behavior.

## 0.1.0 - Initial setup

- Project structure created.
- `pyproject.toml` added.
- MIT license and basic docs initialized.

