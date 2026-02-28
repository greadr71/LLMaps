# UI Components API

Components add UI elements to the map: legend, popup on click, search, and controls. Add them with `Map.add_component()`.

## BaseComponent

All components inherit from `BaseComponent` and implement `to_dict()`. They have a `component_type` string used in the generated config.

---

## Legend

Shows layer names and optional visibility toggles. Can display precomputed feature counts per layer.

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
