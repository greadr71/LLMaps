# UI Components API

Components add UI elements to the map: legend, popup on click, search, and controls. Add them with `Map.add_component()`.

## BaseComponent

All components inherit from `BaseComponent` and implement `to_dict()`. They have a `component_type` string used in the generated config.

---

## Legend

Shows layer names and optional visibility toggles. Can display precomputed feature counts per layer, optional collapsible tips, and optional **size-by-value** blocks (from `DataDrivenSize` on layers or from `size_legends`).

```python
from llmaps.components import Legend

Legend(
    position: str = "top-right",
    show_toggle: bool = True,
    layer_labels: Mapping[str, str] = {},
    layer_counts: Mapping[str, int] = {},
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `position` | str | `"top-right"` | Position: `"top-left"`, `"top-right"`, `"bottom-left"`, `"bottom-right"`. |
| `show_toggle` | bool | True | Whether each layer can be toggled on/off from the legend. |
| `layer_labels` | dict | {} | Map layer id → human-readable label. |
| `layer_counts` | dict | {} | Map layer id → precomputed feature count (displayed as static number). |
| `instructions` | list of str or None | None | Tip strings shown in a collapsible section at the bottom of the legend. |
| `collapsed` | bool | True | Whether the tips section starts collapsed. |
| `tips_title` | str or None | None | Heading for the tips block. If omitted, defaults from `Map.locale` (`en-US` → “💡 Tips”, `ru-RU` → “💡 Подсказки”). |
| `size_legends` | list of dict or None | None | Extra size-legend payloads (same shape as layer `metadata["llmaps_size_legend"]`). Usually left unset; use `DataDrivenSize` on `CircleLayer` / `SymbolLayer` instead. |
| `groups` | list of dict or None | None | Declarative legend groups. Each group supports `id`, `title`, `layer_ids`, `size_legend_ids`, optional local `order`, and `collapsed`. |
| `order` | list of str or None | None | Optional top-level display order. Use tokens like `"group:places"`, `"layer:points"`, `"size_legend:population"`, `"entries"`, `"color_ramp"`, `"basemap"`, and `"instructions"`. |

Grouped legend example:

```python
Legend(
    layer_labels={
        "cities": "Cities",
        "stores": "Stores",
    },
    size_legends=[
        {
            "id": "city-population",
            "title": "Population",
            "visual": "fill",
            "circles": [
                {"value": 1000, "size_px": 4, "label": "1k"},
                {"value": 10000, "size_px": 10, "label": "10k"},
                {"value": 50000, "size_px": 18, "label": "50k"},
            ],
        }
    ],
    groups=[
        {
            "id": "places",
            "title": "Places",
            "layer_ids": ["cities"],
            "size_legend_ids": ["city-population"],
        },
        {"id": "commerce", "title": "Commerce", "layer_ids": ["stores"]},
    ],
    order=["group:places", "group:commerce", "instructions"],
)
```

---

## DataDrivenSize

Builds a MapLibre `interpolate` / `linear` expression from three value stops (percentiles by default) and attaches a matching **three-circle** SVG block in the server-rendered legend.

Optionally drives **`circle-color`** on `CircleLayer` from `color_stops`: either **linear interpolate** between any number of `(value, "#hex")` pairs, or a **`step`** ramp (hard bands). Legend circle fills follow `color_stops` at the three size stops, unless you override them with `legend_circle_colors` (low, mid, high — same order as sorted size stops).

Attach to a `CircleLayer` or `SymbolLayer` as `data_driven_size=...`. At `Map.to_dict()` time, if the layer uses a local `FileSource`, LLMaps loads the file, reads the numeric column(s), replaces `circle-radius` / `icon-size`, and stores `metadata["llmaps_size_legend"]`. **`color_stops` / `color_mode` / `color_field` apply only to `CircleLayer`** (they set `circle-color`). `SymbolLayer` resolution affects `icon-size` only; use custom paint or SDF `icon-color` separately if needed. For remote-only sources, set paint/layout yourself.

**Staleness:** anything resolved here is **frozen when the HTML is generated**. Maps backed by databases or APIs that change every day should **not** use `FileSource` + `DataDrivenSize` to imply “always current” data—refresh the file and re-export, or compute size expressions in client-side JS after fetching live GeoJSON.

**Inline sample (no `FileSource`):** pass `data_driven_size_values=[...]` on `CircleLayer` / `SymbolLayer` together with `data_driven_size=...`. LLMaps runs the same `resolve()` logic on that array at `Map.to_dict()` time (e.g. after you `requests.get(...)` and extract the numeric column in your map script). The HTML still reflects **that** sample until you export again.

**Client-side sizing (`data_driven_size_client=True`):** with `data_driven_size=...` set, `Map.to_dict()` does **not** call `resolve()` or touch paint/layout. It only adds `metadata["llmaps_data_driven_size_spec"]` (from `DataDrivenSize.client_spec_dict()`). The generated HTML includes `data_driven_size_client.js`, which exposes `llmapsApplyDataDrivenSizeFromValues(map, layerId, layerType, numericValues, spec, options?)` — call it after you fetch numbers in the browser (e.g. from pg_featureserv). `layerType` is `"circle"` or `"symbol"`. Optional `options.filterPositive` matches common sales-only samples.

```python
from llmaps.components import DataDrivenSize
from llmaps.layers import CircleLayer

dds = DataDrivenSize(
    field="population",
    size_range=(4.0, 22.0),
    auto_percentiles=(0.1, 0.5, 0.9),
    min_value=None,
    max_value=None,
    value_format="thousands",
    legend_visual="fill",
    legend_color="#64748b",
    legend_title="Population",
    locale="en-US",
    color_stops=[(0, "#ecfccb"), (5000, "#65a30d"), (50000, "#365314")],
    color_mode="interpolate",
)
layer = CircleLayer(id="cities", source=src, color="#3182bd", data_driven_size=dds)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field` | str | required | GeoJSON property used in `["get", field]` for **size**. |
| `size_range` | (float, float) | `(4, 22)` | Output at low / high stops (circle radius in px, or symbol `icon-size` scale). |
| `auto_percentiles` | (float, float, float) | `(0.1, 0.5, 0.9)` | Percentiles for the three domain stops (unless overridden by `min_value` / `max_value`). |
| `min_value`, `max_value` | float or None | None | Optional fixed low / high domain ends for the interpolate stops. |
| `value_format` | str or callable | `"thousands"` | Legend labels: `"thousands"`, `"raw"`, `"mln_rub"`, or `fn(value) -> str`. |
| `legend_visual` | `"fill"` \| `"stroke"` | `"fill"` | Filled disks vs outline rings in the SVG. |
| `legend_color` | str | `"#64748b"` | Single fill (`fill`) or stroke color (`stroke`) when no per-circle fills. |
| `legend_title` | str or None | None | Optional title above the SVG. |
| `locale` | str | `"en-US"` | BCP 47 tag for built-in numeric formats. |
| `color_stops` | list of (float, str) or None | None | `(value, "#hex")` pairs for `circle-color`. At least two pairs for `interpolate`; one or more thresholds for `step`. |
| `color_mode` | `"interpolate"` \| `"step"` | `"interpolate"` | MapLibre expression kind for color. |
| `color_field` | str or None | None | Property for color `get`; defaults to `field`. |
| `color_step_below` | str or None | None | For `step`: color when value **&lt;** first threshold. Defaults to `"#e5e7eb"`. |
| `legend_circle_colors` | (str, str, str) or None | None | Fixed hex colors for the three legend circles (low → high value). Overrides auto colors from `color_stops`; map color still uses `color_stops` when set. Without `color_stops`, only the legend uses these fills. |

**Helpers:** `color_at_value(stops, x)` — linear RGB sample along `color_stops` (exported from `llmaps.components`).

**Example:** `examples/technical/data-driven-size/build_map.py`.

---

## Popup

Shows feature attributes when the user clicks (or hovers) on a layer. Supports a default set of fields and optional per-layer overrides.

```python
from llmaps.components import Popup

Popup(
    fields: List[str] = [],
    field_labels: Mapping[str, str] = {},
    template: Optional[str] = None,
    fields_by_layer: Mapping[str, List[str]] = {},
    trigger: Literal["click", "hover"] = "click",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fields` | list of str | [] | Default list of attribute names to show. |
| `field_labels` | dict | {} | Attribute name → human-readable label. |
| `template` | str or None | None | Optional HTML template; if None, default table-like layout is used. |
| `fields_by_layer` | dict | {} | Layer id → list of field names (overrides default `fields` per layer). |
| `trigger` | str | `"click"` | `"click"` — popup on click; `"hover"` — popup follows cursor, disappears on mouseleave. |

**Note:** When `trigger="hover"`, a single shared popup instance is used (no close button). When both Popup and Sidebar are configured, layers in `sidebar.fields_by_layer` are excluded from popup handling.

---

## Sidebar

Sliding side panel that shows feature attributes on click. For complex detail views where a popup is too small.

```python
from llmaps.components import Sidebar

Sidebar(
    position: Literal["left", "right"] = "right",
    width: int = 400,
    fields_by_layer: Mapping[str, List[str]] = {},
    field_labels: Mapping[str, str] = {},
    title_field: Optional[str] = None,
    title_by_layer: Mapping[str, str] = {},
    show_on_click: bool = True,
    close_on_map_click: bool = True,
    zoom_on_click: Optional[float] = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `position` | str | `"right"` | `"left"` or `"right"`. |
| `width` | int | 400 | Panel width in pixels. |
| `fields_by_layer` | dict | {} | Layer id → list of attribute names to display. |
| `field_labels` | dict | {} | Attribute name → human-readable label (shared across layers). |
| `title_field` | str or None | None | Attribute name used as sidebar title (from clicked feature). |
| `title_by_layer` | dict | {} | Layer id → static title when no `title_field` match. |
| `show_on_click` | bool | True | Open sidebar automatically on feature click. |
| `close_on_map_click` | bool | True | Close sidebar when clicking empty map area. |
| `zoom_on_click` | float or None | None | Fly to this zoom level on click (Point features only). |

**Priority:** Sidebar takes priority over Popup — layers listed in `fields_by_layer` are excluded from popup click handlers.

**JS API:** `window.llmapsSidebarOpen(layerId, feature)` and `window.llmapsSidebarClose()` are exposed for custom JS integration.

---

## Dashboard

Persistent overlay panel for map dashboards. Use it for always-visible filters, status summaries, and custom HTML blocks that should stay attached to the map viewport.

```python
from llmaps.components import Dashboard

Dashboard(
    dashboard_id: str = "dashboard",
    position: Literal["top-left", "top-right", "bottom-left", "bottom-right"] = "top-right",
    title: Optional[str] = None,
    width: int = 360,
    height: Optional[int] = None,
    collapsible: bool = True,
    collapsed: bool = False,
    filters: List[Dict[str, Any]] = [],
    content_html: str = "",
    empty_state: str = "No dashboard content yet.",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dashboard_id` | str | `"dashboard"` | Stable dashboard identifier used by the frontend JS bridge. |
| `position` | str | `"top-right"` | Overlay position on the map. |
| `title` | str or None | None | Header title shown in the dashboard card. |
| `width` | int | 360 | Dashboard width in pixels. |
| `height` | int or None | None | Optional maximum dashboard height in pixels. |
| `collapsible` | bool | True | Whether the user can collapse the dashboard. |
| `collapsed` | bool | False | Whether the dashboard starts collapsed. |
| `filters` | list of dict | [] | Declarative filter descriptors rendered in the dashboard filter bar. |
| `content_html` | str | `""` | Initial HTML for the dashboard body. |
| `empty_state` | str | `"No dashboard content yet."` | Placeholder text shown when `content_html` is empty. |

### Filter descriptors

Each item in `filters` is a serializable dict. Supported `type` values in v1 are `"select"`, `"date"`, and `"text"`.

```python
Dashboard(
    dashboard_id="overview",
    title="Overview",
    filters=[
        {
            "id": "period",
            "type": "select",
            "label": "Period",
            "value": "week",
            "options": [
                {"value": "day", "label": "Day"},
                {"value": "week", "label": "Week"},
                {"value": "month", "label": "Month"},
            ],
        },
        {
            "id": "date",
            "type": "date",
            "label": "Snapshot date",
            "value": "2026-03-08",
        },
        {
            "id": "query",
            "type": "text",
            "label": "Quick note",
            "placeholder": "Type any label...",
            "value": "All regions",
        },
    ],
)
```

### JS bridge

The generated frontend exposes a minimal dashboard bridge for custom JS integration:

- `window.llmapsDashboardSetContent(id, html)`
- `window.llmapsDashboardSetTitle(id, title)`
- `window.llmapsDashboardGetState(id)`
- `window.llmapsDashboardSetCollapsed(id, collapsed)`

When a filter changes, the page emits a `llmaps:dashboard-filter-change` event on `window`. The event detail contains `dashboardId`, `filterId`, `value`, and `state`.

**Relationship to Sidebar:** `Dashboard` is for persistent controls and context. `Sidebar` remains the primary component for click-driven feature details.

**Current scope note:** v1 supports a single dashboard instance per map. If multiple `Dashboard` components are added, only the first one is initialized on the generated page.

---

## FeatureSearch

Search within map data by feature attributes (not a geocoder). Provides a dropdown with matching features and flies to the selected result.

```python
from llmaps.components import FeatureSearch

FeatureSearch(
    position: Literal["top-left", "top-right", "top-center"] = "top-center",
    placeholder: str = "Search...",
    search_fields: Mapping[str, List[str]] = {},
    field_labels: Mapping[str, str] = {},
    max_results: int = 15,
    zoom_on_select: float = 8,
    debounce_ms: int = 200,
    min_chars: int = 2,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `position` | str | `"top-center"` | Placement of the search bar. |
| `placeholder` | str | `"Search..."` | Input placeholder text. |
| `search_fields` | dict | {} | **Source id** → list of attribute names to search in. |
| `field_labels` | dict | {} | Attribute name → display label in dropdown results. |
| `max_results` | int | 15 | Max results shown in dropdown. |
| `zoom_on_select` | float | 8 | Zoom level to fly to (or max zoom for fitBounds on polygons). |
| `debounce_ms` | int | 200 | Debounce delay before searching. |
| `min_chars` | int | 2 | Minimum characters before triggering search. |

**Note:** `search_fields` keys are **source ids**, not layer ids. Data is loaded via `window.llmapsGetSourceData()` and cached on map load.

**Difference from Search:** `Search` queries an external geocoder API. `FeatureSearch` searches within data already on the map.

**Sidebar integration:** When a result is selected and Sidebar is configured, the sidebar opens with the selected feature's details.

---

## Search

Address search: geocoder URL, optional autocomplete, fly to result.

```python
from llmaps.components import Search

Search(
    geocoder_url: Optional[str] = None,
    geocoder_params: Optional[Dict[str, str]] = None,
    placeholder: str = "Search address...",
    autocomplete: bool = True,
    position: Literal["top-left", "top-right"] = "top-left",
    zoom_on_result: int = 15,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `geocoder_url` | str or None | None | URL of the geocoder API. |
| `geocoder_params` | dict or None | None | Extra query params (e.g. API key). |
| `placeholder` | str | `"Search address..."` | Input placeholder text. |
| `autocomplete` | bool | True | Request suggestions while typing (with debounce). |
| `position` | str | `"top-left"` | Placement of the search box. |
| `zoom_on_result` | int | 15 | Zoom level when flying to the result. |

**Note:** The frontend calls the geocoder; CORS and API terms apply.

---

## Controls

Standard map controls: zoom buttons, scale bar, fullscreen.

```python
from llmaps.components import Controls

Controls(
    zoom: bool = True,
    scale: bool = True,
    fullscreen: bool = False,
    hash: bool = True,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `zoom` | bool | True | Show zoom in/out buttons. |
| `scale` | bool | True | Show scale bar. |
| `fullscreen` | bool | False | Show fullscreen toggle. |
| `hash` | bool | True | Sync map position with URL hash in format `#zoom/lat/lon`. |

---

## Storytelling

Scrollytelling component: a scrollable narrative panel alongside the map. As the user scrolls through scenes, the map camera, layer visibility, and feature highlights update automatically. Uses [Scrollama](https://github.com/russellsamora/scrollama) (loaded from CDN).

```python
from llmaps.components import Storytelling, Scene

Storytelling(
    scenes: List[Scene] = [],
    position: Literal["left", "right"] = "left",
    width: int = 400,
    progress: bool = True,
    snap_mode: Literal["proximity", "mandatory"] = "proximity",
    touch_swipe: bool = True,
    comparison_slider_hint: Optional[str] = None,
    comparison_slider_start_pct: float = 0.5,
    use_swiper_cdn: bool = False,
    expose_scene_bridge: bool = False,
    prewarm_comparison: bool = False,
    keep_main_layers_visible_in_comparison: bool = False,
    mobile_scroll_fallback: bool = False,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scenes` | list of Scene | [] | Ordered list of narrative scenes. |
| `position` | str | `"left"` | Side of the screen for the narrative panel. |
| `width` | int | 400 | Narrative panel width in pixels. |
| `progress` | bool | True | Show clickable navigation dots for quick scene access. |
| `snap_mode` | str | `"proximity"` | CSS scroll-snap behaviour: `"proximity"` snaps only near scene boundaries; `"mandatory"` always snaps to the nearest scene. |
| `touch_swipe` | bool | True | Enable the built-in touch-swipe handler. Set to `False` to rely on native scroll + CSS snap + Scrollama only. |
| `comparison_slider_hint` | str or None | None | Tooltip text shown when comparison slider first appears. `None` = locale-aware default. |
| `comparison_slider_start_pct` | float | 0.5 | Initial comparison slider position as fraction of map width in `[0.0, 1.0]`. |
| `use_swiper_cdn` | bool | False | Include Swiper CDN assets in generated HTML for custom mobile scene transitions. |
| `expose_scene_bridge` | bool | False | Expose `window.llmapsApplySceneByIndex(index)` for custom JS scene control. |
| `prewarm_comparison` | bool | False | Pre-initialize comparison map infrastructure after layers are ready. |
| `keep_main_layers_visible_in_comparison` | bool | False | Keep main-map layers visible while comparison overlay is active. |
| `mobile_scroll_fallback` | bool | False | Enable scroll-event fallback for scene detection when `IntersectionObserver` is unreliable. |

### Scene

Each scene defines one step in the narrative.

```python
Scene(
    id: str,
    title: str,
    content: str,                              # HTML text
    center: Optional[List[float]] = None,      # [lon, lat], None = keep current
    zoom: Optional[float] = None,              # None = keep current
    bearing: float = 0,
    pitch: float = 0,
    visible_layers: Optional[List[str]] = None, # None = don't change, [] = hide all
    highlight: Dict[str, List] = {},            # {source_id: [feature_ids]}
    fly_duration: int = 2000,                   # camera animation in ms
    comparison: Optional[SceneComparison] = None,  # per-scene comparison slider
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Unique scene identifier. |
| `title` | str | required | Scene heading in the narrative panel. |
| `content` | str | required | HTML body text for the scene. |
| `center` | list or None | None | Map center `[lon, lat]` to fly to. `None` = keep current. |
| `zoom` | float or None | None | Zoom level. `None` = keep current. |
| `bearing` | float | 0 | Map rotation in degrees. |
| `pitch` | float | 0 | Map tilt in degrees. |
| `visible_layers` | list or None | None | Layer ids to show. `None` = don't change. `[]` = hide all. |
| `highlight` | dict | {} | Features to highlight: `{source_id: [feature_id, ...]}`. Uses feature-state `highlighted: true`. |
| `fly_duration` | int | 2000 | Camera fly animation duration in ms. |
| `comparison` | SceneComparison or None | None | Per-scene comparison slider. When set, `visible_layers` and `highlight` are ignored. |

### SceneComparison

Per-scene before/after slider configuration. When a `Scene` has a `comparison`, the map shows a draggable slider overlay with two map instances.

```python
SceneComparison(
    before_layers: List[str] = [],
    after_layers: List[str] = [],
    before_label: Optional[str] = None,
    after_label: Optional[str] = None,
    before_highlight: Dict[str, List] = {},
    after_highlight: Dict[str, List] = {},
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `before_layers` | list of str | [] | Layer ids shown on the left (before) side. |
| `after_layers` | list of str | [] | Layer ids shown on the right (after) side. |
| `before_label` | str or None | None | Label displayed on the before panel (e.g. `"2016"`). |
| `after_label` | str or None | None | Label displayed on the after panel (e.g. `"2018"`). |
| `before_highlight` | dict | {} | Features to highlight on the before map: `{source_id: [feature_id, ...]}`. |
| `after_highlight` | dict | {} | Features to highlight on the after map: `{source_id: [feature_id, ...]}`. |

**Difference from `Map.enable_comparison()`:** `enable_comparison()` creates a static full-map slider. `SceneComparison` is dynamic — the slider appears only during specific scenes and is hidden otherwise. Camera, layers, and highlights are managed per-scene.

**Popups:** Click/hover popups automatically work on both comparison map instances (using the same popup configuration as the main map).

**Layers:** Set `visible=False` on layers that should be hidden initially and let scenes control visibility via `visible_layers`.

**Highlights:** Requires `promote_id` on the source. Use feature-state expressions in layer paint to style highlighted features (e.g. brighter color, thicker stroke).

**Navigation dots:** When `progress=True`, clickable dots appear on the side of the map. Hovering shows the scene title as a tooltip. Clicking scrolls to that scene.

---

## See also

- [Map](map.md) — add_component()
- [Storytelling recipe](../recipes/storytelling.md) — full example
- [Storytelling comparison recipe](../recipes/storytelling-comparison.md) — before/after within scenes
