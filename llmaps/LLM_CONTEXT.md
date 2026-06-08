# LLMaps — reference for LLM-assisted map code

Context for generating Python code that creates interactive web maps with LLMaps. Library is already installed.

## Quick Start

```python
from llmaps import Map
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource
from llmaps.components import Legend, Popup, Controls

source = FileSource(id="points", path="data/points.geojson")
layer = CircleLayer(
    id="points-layer",
    source=source,
    radius=6,
    color="#3182bd",
    opacity=0.8,
)

m = Map(center=[10.0, 50.0], zoom=4, title="My Map", tiles="osm")
m.add_layer(layer)
m.add_component(Legend(layer_labels={"points-layer": "Points"}))
m.add_component(Popup(fields=["name", "value"], field_labels={"name": "Name", "value": "Value"}))
m.add_component(Controls(zoom=True, scale=True))

m.auto_extent()
m.save("my_map.html")
```

## Quick Reference by Scenario

| Scenario | Components |
|----------|------------|
| Small dataset (<10k points) | CircleLayer + FileSource + Legend |
| Large dataset (>100k points) | H3Layer + FileSource + Legend (+ use_compression) |
| Polygons / choropleth | FillLayer + FileSource + Legend + Popup |
| Dynamic polygon coloring | FillLayer + expressions + promote_id + feature_state |
| Rich feature details | Sidebar + FillLayer/CircleLayer (replaces Popup for complex views) |
| Persistent map dashboard | Dashboard + custom JS bridge |
| Search within data | FeatureSearch (+ Sidebar for detail on select) |
| Hover tooltips | Popup(trigger="hover") + FillLayer/CircleLayer |
| Embedded map (no server) | Map() + FileSource (embedded by default) |
| Before/after comparison | Two layers + Map.enable_comparison(left_layers, right_layers) |
| Scrollytelling narrative | Storytelling + Scene + FillLayer/CircleLayer (visible=False) |
| Scrollytelling + comparison | Storytelling + Scene(comparison=SceneComparison(...)) |
| Data from API | CircleLayer/FillLayer + ApiSource + Legend |
| Vector tiles | VectorTileLayer + VectorTileSource |
| Marker size from a numeric column (**snapshot at HTML save**) | `data_driven_size` + either `FileSource` **or** `data_driven_size_values=[...]` (API sample in Python) + Legend — re-export when the sample changes |
| Marker size **live in the browser** (pg_featureserv / custom fetch) | `data_driven_size` + `data_driven_size_client=True` → `metadata.llmaps_data_driven_size_spec` + bundled `llmapsApplyDataDrivenSizeFromValues`; the browser helper also accepts Atlas-style camelCase options and exposes `llmapsApplyRuntimeStyle(s)` for runtime paint/layout/filter on MVT layers |

## Constructors (Python stubs)

```python
# Map — center [lon, lat], zoom 0–22. tiles: "osm", "carto-light", "carto-dark", "yandex", "2gis"
Map(center=[lon, lat], zoom=10.0, title=None, tiles="osm", embedded=True, use_compression=True, locale="en-US", lazy_init=False, max_active_maps=8, map_instance_count=None, hash_position=None)
# locale: "en-US" (commas: 1,000,000), "ru-RU" (spaces: 1 000 000), or any BCP 47 tag. Formats numbers in Popup/Sidebar.
# lazy_init + map_instance_count>=3: use when many maps on one page to avoid WebGL context limit (lazy create/dispose, LRU cap).
# hash_position: URL hash sync in format #zoom/lat/lon. If None, inferred from Controls(hash=...).
# .add_layer(layer) .add_component(comp) .auto_extent(sources=None, padding=0.1) .save(path) .to_html()
# .enable_comparison(left_layers=[], right_layers=[])  # before/after slider
# .add_custom_js(js) .add_custom_css(css) .add_custom_html(html) .embed_data(key, data)

# Layers — all need id, source
CircleLayer(id, source, radius=6.0, color="#3182bd", opacity=0.8, data_driven_size=None, data_driven_size_values=None, data_driven_size_client=False)
# data_driven_size: optional DataDrivenSize(field=...) — at to_dict: if data_driven_size_client=True, only metadata.llmaps_data_driven_size_spec (no paint change); else uses data_driven_size_values or FileSource; sets circle-radius interpolate + size legend; color_stops also sets circle-color.
FillLayer(id, source, fill_color="#3182bd", fill_opacity=0.6, stroke_color="#08519c", stroke_width=1.0, feature_state=None)
# fill_color/fill_opacity accept MapLibre expressions (e.g. feature-state). feature_state: {"active": True, "color": "POP_EST"} auto-sets state from GeoJSON (no custom JS). stroke_width>1 adds outline layer.
H3Layer(id, source, h3_column=None, resolution=8, aggregation="count", property_field="value",
        colors=["#ffffcc", "#800026"], opacity=0.7, stroke_width=0.0, stroke_color=None)
# aggregation: "count"|"sum"|"mean"|"median"
VectorTileLayer(id, source, source_layer="", geometry_type="circle", dynamic_stats=False,
                property_field=None, colors=["#e0d4f7", "#6829c5"], radius_range=None, opacity=0.8)
# geometry_type: "circle"|"fill"|"line". source must be VectorTileSource.
SymbolLayer(id, source, source_layer=None,
            icon_image=None, icon_size=1.0, icon_anchor="center",
            icon_allow_overlap=True, icon_ignore_placement=False, icon_offset=[0.0, 0.0],
            icon_opacity=1.0,
            text_field=None, text_size=12.0, text_anchor="top", text_offset=[0.0, 0.5],
            text_color="#222222", text_opacity=1.0, text_halo_color="rgba(255,255,255,0.8)", text_halo_width=0.0,
            data_driven_size=None, data_driven_size_values=None, data_driven_size_client=False)
# icon_image: string (pre-registered image name) or MapLibre expression list. text_field: plain property name
# (auto-wrapped to ["get", name]) or expression list. source_layer: set for VectorTileSource only.

# Sources — all have id. Use promote_id= for feature-state / setFeatureState.
FileSource(id, path, file_format=None, *, promote_id=None)   # .geojson, .csv, .parquet
ApiSource(id, url, headers=None, params=None, *, promote_id=None)
VectorTileSource(id, tiles_url, *, promote_id=None)   # URL template with {z},{x},{y}

# Components
Legend(position="top-right", show_toggle=True, layer_labels={}, layer_counts={},
       instructions=None, collapsed=True, tips_title=None, size_legends=None)
# instructions: list of tip strings (collapsible block). tips_title: optional; default from Map.locale (en → "💡 Tips", ru → "💡 Подсказки").
# size_legends: optional extra size-legend dicts; normally use DataDrivenSize on a layer instead.

# DataDrivenSize — percentile-based circle-radius / icon-size + SVG size legend (to_dict: FileSource OR data_driven_size_values; frozen at save) OR client_spec via data_driven_size_client=True
# Optional circle-color: color_stops=[(v,"#hex"),...], color_mode="interpolate"|"step", color_field=None, color_step_below=None,
# legend_circle_colors=(low,mid,high) hex — overrides legend fills only when color_stops set; without color_stops, legend-only fills.
DataDrivenSize(field, size_range=(4.0, 22.0), auto_percentiles=(0.1, 0.5, 0.9),
               min_value=None, max_value=None, value_format="thousands",
               legend_visual="fill", legend_color="#64748b", legend_title=None, locale="en-US",
               color_stops=None, color_mode="interpolate", color_field=None, color_step_below=None, legend_circle_colors=None)
# value_format: "thousands"|"raw"|"mln_rub"|callable. legend_visual: "fill"|"stroke".
# color_at_value(stops, x) — helper to sample the same linear ramp used for legend circles.
Popup(fields=[], field_labels={}, template=None, fields_by_layer={}, trigger="click")
# trigger: "click" or "hover"
Sidebar(position="right", width=400, fields_by_layer={}, field_labels={}, title_field=None,
        title_by_layer={}, show_on_click=True, close_on_map_click=True, zoom_on_click=None,
        hide_empty_fields=False)
# hide_empty_fields: if True, null/empty string values are hidden
Dashboard(dashboard_id="dashboard", position="top-right", title=None, width=360, height=None,
          collapsible=True, collapsed=False, filters=[], content_html="",
          empty_state="No dashboard content yet.")
# filters: list of dicts with serializable descriptors. Supported types: "select", "date", "text".
# current scope: one Dashboard instance per map (first component wins if multiple are added).
FeatureSearch(position="top-center", placeholder="Search...", search_fields={}, field_labels={},
              max_results=15, zoom_on_select=8, debounce_ms=200, min_chars=2)
# search_fields: source_id -> list of attribute names to search
Search(geocoder_url=None, geocoder_params=None, placeholder="Search address...", autocomplete=True,
       position="top-left", zoom_on_result=15)
Controls(zoom=True, scale=True, fullscreen=False, hash=True)

# Storytelling — scrollytelling narrative map
Storytelling(scenes=[Scene(...)], position="left", width=400, progress=True, snap_mode="proximity", touch_swipe=True,
             comparison_slider_hint=None, comparison_slider_start_pct=0.5,
             use_swiper_cdn=False, expose_scene_bridge=False, prewarm_comparison=False,
             keep_main_layers_visible_in_comparison=False, mobile_scroll_fallback=False)
# snap_mode: "proximity" (default) or "mandatory" — CSS scroll-snap behaviour for narrative panel.
# touch_swipe: True (default) enables library touch-swipe handler; False disables it (use native scroll + CSS snap + Scrollama).
# comparison_slider_hint: custom tooltip when comparison slider first appears. None = locale-aware default.
# comparison_slider_start_pct: initial comparison slider position as fraction [0.0, 1.0].
# use_swiper_cdn: include Swiper CDN assets in generated HTML for custom mobile transitions.
# expose_scene_bridge: expose window.llmapsApplySceneByIndex(index) for custom JS.
# prewarm_comparison: pre-initialize comparison infrastructure after layers are ready.
# keep_main_layers_visible_in_comparison: do not hide main-map layers during comparison scenes.
# mobile_scroll_fallback: enable narrative scroll-event fallback scene detection.
Scene(id, title, content,  # content is HTML
      center=None, zoom=None, bearing=0, pitch=0,  # camera (None=keep current)
      visible_layers=None,  # None=don't change, []=hide all, ["id"]=show these
      highlight={},  # {source_id: [feature_ids]} — sets feature-state highlighted=true
      fly_duration=2000,
      comparison=None)  # SceneComparison or None
# Set visible=False on layers; scenes control visibility. Requires promote_id for highlights.
# When comparison is set, the scene shows a before/after slider; visible_layers/highlight are ignored.
SceneComparison(before_layers=[], after_layers=[], before_label=None, after_label=None,
                before_highlight={}, after_highlight={})  # per-side highlight: {source_id: [feature_ids]}
```

## Frontend JS (custom JS via add_custom_js)

For **static** choropleth (colors from GeoJSON property), use layer `feature_state` — no custom JS needed. Use the utilities below for **interactive** updates (e.g. click-to-highlight).

```javascript
await window.llmapsGetSourceData(sourceId)   // Promise<GeoJSON>
window.llmapsSetFeatureState(sourceId, featureId, state)
window.llmapsAnimateFeatureState(sourceId, featureId, targetState, { duration: 280, easing: "easeInOutSine" })
window.llmapsClearFeatureStates(sourceId)
window.llmapsOnLayersReady(fn)
window.llmapsData   // user data from embed_data(key, data)
window.llmapsSidebarOpen(layerId, feature)
window.llmapsSidebarClose()
window.llmapsDashboardSetContent(id, html)
window.llmapsDashboardSetTitle(id, title)
window.llmapsDashboardGetState(id)
window.llmapsDashboardSetCollapsed(id, collapsed)
// window emits "llmaps:dashboard-filter-change" with {dashboardId, filterId, value, state}
```

## Expressions (dynamic styling by feature-state)

Requires promote_id on source. Use with FillLayer(fill_color=..., fill_opacity=...).

```python
from llmaps.expressions import (
    feature_state_color,
    feature_state_value,
    feature_state_fade_mix,
    feature_state_fade_value,
    feature_state_fade_color,
    compute_color_stops,
)

feature_state_color(state_key, color_ramp_key, color_stops, inactive="#F0F0F0", default="#E0E0E0")
# Returns MapLibre expression for fill_color. color_stops: [(value, color), ...]
feature_state_value(state_key, active=0.7, inactive=0.2, default=0.6)
# Returns expression for fill_opacity or circle-radius
feature_state_fade_mix(state_key="active", fade_mix_key="fade_mix")
# Returns robust 0..1 fade mix expression (fallback: active -> 1/0)
feature_state_fade_value(active=0.7, inactive=0.2, state_key="active", fade_mix_key="fade_mix")
# Returns interpolated numeric expression by fade mix (e.g. fill-opacity)
feature_state_fade_color(color_ramp_key, color_stops, inactive="#F0F0F0", state_key="active", fade_mix_key="fade_mix")
# Returns interpolated color expression by fade mix (inactive color -> ramp)
compute_color_stops(values, n_stops=5, colors=None, palette=None, percentiles=None, precision=1, method="quantile")
# values: array-like. Returns list of (value, color) for feature_state_color.
# method: "quantile" (default), "jenks" (natural breaks, requires jenkspy), "equal_interval"
# palette: embedded geoscience palette id from llmaps.palettes (used when colors is not provided)

from llmaps.palettes import get_palette, get_palette_colors, list_palettes
# list_palettes(type="sequential", blindsafe=True, perceptually_uniform=True)  # filter for best palettes
# get_palette_colors("arctic-chill", n=7)  # resample to exactly N colors
# get_palette_colors("crameri-lajolla", n=5)  # for population density
```
