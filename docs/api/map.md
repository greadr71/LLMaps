# Map API

The `Map` class is the main entry point. You create a map, add layers and components, then render to HTML.

## Constructor

```python
from llmaps import Map

Map(
    center: Sequence[float],   # [lon, lat]
    zoom: float = 10.0,
    title: Optional[str] = None,
    tiles: str = "osm",
    embedded: bool = True,
    use_compression: bool = True,
    locale: str = "en-US",
    lazy_init: bool = False,
    max_active_maps: int = 8,
    map_instance_count: Optional[int] = None,
    hash_position: Optional[bool] = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `center` | `[lon, lat]` | required | Initial map center. |
| `zoom` | float | `10.0` | Initial zoom level (typically 0–22). |
| `title` | str or None | None | Optional title used in the HTML page. |
| `tiles` | str | `"osm"` | Tile provider: `"osm"`, `"carto-light"`, `"carto-dark"`, `"yandex"`, `"2gis"`. |
| `embedded` | bool | True | If True, data is inlined in HTML (works via `file://`). |
| `use_compression` | bool | True | If True and embedded, GeoJSON is compressed (Geobuf + Gzip). |
| `locale` | str | `"en-US"` | Locale for number formatting in Popup and Sidebar. Use `"ru-RU"` for Russian (spaces as thousand separators), or any BCP 47 language tag. |
| `lazy_init` | bool | False | If True and `map_instance_count` ≥ 3, maps are created when their container enters the viewport and disposed when it leaves, avoiding "Too many active WebGL contexts". |
| `max_active_maps` | int | 8 | When lazy_init is active, maximum number of map instances kept at once; oldest (LRU) are disposed when the limit is exceeded. |
| `map_instance_count` | int or None | None | Total map instances on the page. Default: 2 for comparison mode, 1 otherwise. Set to 3+ with `lazy_init=True` to enable lifecycle management. |
| `hash_position` | bool or None | None | Sync map position with URL hash (`#zoom/lat/lon`). If `None`, inferred from `Controls(hash=...)` for backward compatibility. |

### Multiple maps on one page (WebGL)

Browsers limit the number of active WebGL contexts per page (often ~16). If you have 3 or more map instances on one page, set `lazy_init=True` and `map_instance_count` to the total number of maps. Maps will be created when their container enters the viewport and disposed when it leaves; at most `max_active_maps` instances stay active (oldest are evicted).

```python
# Dashboard with 5 map widgets — enable lifecycle so WebGL limit is not exceeded
m = Map(center=[10, 50], zoom=4, lazy_init=True, map_instance_count=5)
```

## Methods

### add_layer(layer)

Attach a visual layer. Returns `self` for chaining.

```python
map.add_layer(CircleLayer(id="points", source=source, ...))
```

### add_component(component)

Attach a UI component (Legend, Popup, Controls, Search). Returns `self` for chaining.

```python
map.add_component(Legend(layer_labels={"points": "Points"}))
```

### enable_comparison(left_layers, right_layers)

Enable before/after comparison: two maps with a slider. Layer ids must exist on the map. Returns `self`.

- `left_layers`: list of layer ids shown on the left (before).
- `right_layers`: list of layer ids shown on the right (after).

```python
map.add_layer(layer_before).add_layer(layer_after)
map.enable_comparison(left_layers=["before-layer"], right_layers=["after-layer"])
```

### auto_extent(sources=None, padding=0.1)

Set `center` and `zoom` from the combined bounds of layer data. Skips ApiSource and VectorTileSource (no local geometry). Returns `self`.

- `sources`: optional sequence of sources to use; if None, all layer sources are used.
- `padding`: padding factor for the computed zoom.

```python
map.auto_extent()
```

### to_html()

Return the map as a single HTML string (with inline or embedded JS/CSS and optional embedded data).

```python
html = map.to_html()
```

### save(path)

Render the map and write it to a file. `path` can be a string or `pathlib.Path`. Returns `self`.

```python
map.save("output.html")
```

### add_custom_js(js)

Inject custom JavaScript. `js` is a `str` (inline code) or `pathlib.Path` (file to read). Appended after the core llmaps JS. Multiple calls are cumulative. Returns `self`.

```python
m.add_custom_js(Path("interactivity.js"))       # from file
m.add_custom_js("console.log('hello');")         # inline
```

### add_custom_css(css)

Inject custom CSS. `css` is a `str` or `pathlib.Path`. Appended after base llmaps CSS inside `<style>`. Returns `self`.

```python
m.add_custom_css(Path("sidebar.css"))
m.add_custom_css("body { background: #222; }")
```

### add_custom_html(html)

Inject custom HTML before `</body>`, after the map container and before scripts. Useful for sidebars, overlays, custom UI. Returns `self`.

```python
m.add_custom_html('<div id="sidebar">...</div>')
```

### embed_data(key, data)

Embed arbitrary JSON-serialisable data into the HTML. Available on the frontend as `window.llmapsData.<key>`. Returns `self`.

```python
m.embed_data("deliveryStats", {"avg_hours": 24, "regions": 85})
# In JS: window.llmapsData.deliveryStats.avg_hours
```

### to_dict()

Return a serialisable configuration dict (used internally by the generator). Useful for debugging or custom pipelines.

## Example

```python
from llmaps import Map
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource
from llmaps.components import Legend, Popup, Controls

source = FileSource(id="points", path="data/points.geojson")
layer = CircleLayer(id="points-layer", source=source, radius=6, color="#3182bd", opacity=0.8)

m = Map(center=[10.0, 50.0], zoom=4, title="My Map", tiles="osm")
m.add_layer(layer)
m.add_component(Legend(layer_labels={"points-layer": "Points"}))
m.add_component(Popup(fields=["name", "value"], field_labels={"name": "Name", "value": "Value"}))
m.add_component(Controls(zoom=True, scale=True))

m.auto_extent()
m.save("my_map.html")
```

## See also

- [Layers](layers.md)
- [Sources](sources.md)
- [Components](components.md)
