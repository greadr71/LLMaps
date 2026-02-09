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
    embedded: bool = False,
    use_compression: bool = False,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `center` | `[lon, lat]` | required | Initial map center. |
| `zoom` | float | `10.0` | Initial zoom level (typically 0–22). |
| `title` | str or None | None | Optional title used in the HTML page. |
| `tiles` | str | `"osm"` | Tile provider: `"osm"`, `"carto-light"`, `"carto-dark"`, `"yandex"`, `"2gis"`. |
| `embedded` | bool | False | If True, data is inlined in HTML (works via `file://`). |
| `use_compression` | bool | False | If True and embedded, GeoJSON is compressed (Geobuf + Gzip). |

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
- [API_GUIDE.md](../../API_GUIDE.md) — index and keywords
