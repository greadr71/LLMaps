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

Shows feature attributes when the user clicks on a layer. Supports a default set of fields and optional per-layer overrides.

```python
from llmaps.components import Popup

Popup(
    fields: List[str] = [],
    field_labels: Mapping[str, str] = {},
    template: Optional[str] = None,
    fields_by_layer: Mapping[str, List[str]] = {},
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fields` | list of str | [] | Default list of attribute names to show. |
| `field_labels` | dict | {} | Attribute name → human-readable label. |
| `template` | str or None | None | Optional HTML template; if None, default table-like layout is used. |
| `fields_by_layer` | dict | {} | Layer id → list of field names (overrides default `fields` per layer). |

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
- [API_GUIDE.md](../../API_GUIDE.md) — index and keywords
