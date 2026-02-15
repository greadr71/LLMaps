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
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `zoom` | bool | True | Show zoom in/out buttons. |
| `scale` | bool | True | Show scale bar. |
| `fullscreen` | bool | False | Show fullscreen toggle. |

---

## See also

- [Map](map.md) — add_component()
