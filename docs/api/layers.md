# Layers API

Layers define how data is drawn on the map. All layers inherit from `BaseLayer` and require an `id` and a `source`.

## BaseLayer

Common attributes for all layers:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Unique layer identifier. |
| `source` | BaseSource | required | Data source (FileSource, ApiSource, VectorTileSource). |
| `visible` | bool | True | Initial visibility. |
| `minzoom` | float or None | None | Minimum zoom at which the layer is shown. |
| `maxzoom` | float or None | None | Maximum zoom at which the layer is shown. |
| `metadata` | dict | {} | Extra metadata (passed through to config). |

---

## CircleLayer

Points rendered as circles. Best for small to medium point datasets (&lt;10k points).

```python
from llmaps.layers import CircleLayer

CircleLayer(
    id: str,
    source: BaseSource,
    radius: float = 6.0,
    color: str = "#3182bd",
    opacity: float = 0.8,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Unique layer id. |
| `source` | BaseSource | required | Source with point geometries. |
| `radius` | float | 6.0 | Circle radius in pixels. |
| `color` | str | `"#3182bd"` | Fill color (CSS color). |
| `opacity` | float | 0.8 | Fill opacity (0–1). |

**When to use:** Point data, markers, small datasets. For large point sets use `H3Layer` or `VectorTileLayer`.

---

## FillLayer

Polygons with fill and optional stroke. Use for districts, zones, boundaries, choropleth.

```python
from llmaps.layers import FillLayer

FillLayer(
    id: str,
    source: BaseSource,
    fill_color: str = "#3182bd",
    fill_opacity: float = 0.6,
    stroke_color: Optional[str] = "#08519c",
    stroke_width: Optional[float] = 1.0,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Unique layer id. |
| `source` | BaseSource | required | Source with polygon geometries. |
| `fill_color` | str | `"#3182bd"` | Fill color. |
| `fill_opacity` | float | 0.6 | Fill opacity (0–1). |
| `stroke_color` | str or None | `"#08519c"` | Outline color; None to omit. |
| `stroke_width` | float or None | 1.0 | Outline width in pixels. |

---

## H3Layer

Hexagonal grid using H3 indices. Points are aggregated into H3 cells; fill color can be driven by a value field (count/sum/mean/median). Best for large point datasets (&gt;100k points).

**Optional dependency:** `pip install llmaps[h3]` (h3, geopandas).

```python
from llmaps.layers import H3Layer

H3Layer(
    id: str,
    source: BaseSource,
    h3_column: Optional[str] = None,
    resolution: int = 8,
    aggregation: Literal["count", "sum", "mean", "median"] = "count",
    property_field: str = "value",
    colors: List[str] = ["#ffffcc", "#800026"],
    opacity: float = 0.7,
    stroke_width: float = 0.0,
    stroke_color: Optional[str] = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Unique layer id. |
| `source` | BaseSource | required | Source with point geometries (or pre-aggregated with `h3_column`). |
| `h3_column` | str or None | None | Column name for H3 indices; if None, points are converted to H3. |
| `resolution` | int | 8 | H3 resolution 0–15 (e.g. 8 ≈ 460 m). |
| `aggregation` | str | `"count"` | `"count"`, `"sum"`, `"mean"`, or `"median"`. |
| `property_field` | str | `"value"` | Field used for sum/mean/median and color gradient. |
| `colors` | list of str | `["#ffffcc", "#800026"]` | Two or more colors for gradient. |
| `opacity` | float | 0.7 | Fill opacity. |
| `stroke_width` | float | 0.0 | Outline width. |
| `stroke_color` | str or None | None | Outline color. |

Stats (e.g. q05, q95) for the gradient are set automatically when using embedded mode; for custom stats use `layer.set_stats({"q05": ..., "q95": ...})`.

---

## VectorTileLayer

Renders data from Mapbox Vector Tiles (PBF). Requires a `VectorTileSource`. Supports circle, fill, or line geometry and optional dynamic_stats (viewport-based gradient stats).

```python
from llmaps.layers import VectorTileLayer
from llmaps.sources import VectorTileSource

source = VectorTileSource(id="tiles", tiles_url="https://example.com/tiles/{z}/{x}/{y}.pbf")

VectorTileLayer(
    id: str,
    source: VectorTileSource,
    source_layer: str = "",
    geometry_type: Literal["circle", "fill", "line"] = "circle",
    dynamic_stats: bool = False,
    property_field: Optional[str] = None,
    colors: List[str] = ["#e0d4f7", "#6829c5"],
    radius_range: Optional[Tuple[float, float]] = None,
    opacity: float = 0.8,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Unique layer id. |
| `source` | VectorTileSource | required | Vector tile source. |
| `source_layer` | str | `""` | Name of the layer inside the PBF (MapLibre source-layer). |
| `geometry_type` | str | `"circle"` | `"circle"`, `"fill"`, or `"line"`. |
| `dynamic_stats` | bool | False | If True, gradient stats computed on client from viewport. |
| `property_field` | str or None | None | Numeric property for gradient. |
| `colors` | list of str | `["#e0d4f7", "#6829c5"]` | Colors for gradient. |
| `radius_range` | (min, max) or None | None | Min/max radius in pixels for circle type. |
| `opacity` | float | 0.8 | Fill/circle opacity. |

---

## See also

- [Sources](sources.md) — FileSource, ApiSource, VectorTileSource
- [API_GUIDE.md](../../API_GUIDE.md) — index and keywords
- [Recipes: Heatmap](../recipes/heatmap.md)
