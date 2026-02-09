# Data Sources API

Sources provide geometry and attributes to layers. All sources have an `id` and implement `to_dict()`.

## BaseSource

Abstract base. Concrete sources: `FileSource`, `ApiSource`, `VectorTileSource`.

```python
from llmaps.sources.base import BaseSource

# BaseSource(id: str)
```

---

## FileSource

Load data from a local file (GeoJSON, CSV, or Parquet). Format is inferred from the file extension unless `file_format` is set.

```python
from llmaps.sources import FileSource

FileSource(
    id: str,
    path: str,
    file_format: Optional[Literal["geojson", "csv", "parquet"]] = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Source identifier (used by layers). |
| `path` | str | required | Path to file (.geojson/.json, .csv, .parquet/.pq). |
| `file_format` | str or None | None | Explicit format; if None, inferred from path. |

**When to use:** Local static data, embedded maps. With `Map(embedded=True)` the data is inlined in HTML (optionally compressed).

---

## ApiSource

Load GeoJSON from an HTTP URL. The **frontend** fetches the URL when the map initialises; there is no server-side fetch at config time. Use for live or remote datasets.

```python
from llmaps.sources import ApiSource

ApiSource(
    id: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Source identifier. |
| `url` | str | required | URL that returns GeoJSON (FeatureCollection, Feature, or list of features). |
| `headers` | dict or None | None | Optional HTTP headers (e.g. Authorization). |
| `params` | dict or None | None | Optional query parameters. |

**When to use:** External APIs, dynamic data, CORS-enabled endpoints.

---

## VectorTileSource

Provide a vector tile URL template for Mapbox Vector Tiles (PBF). Used with `VectorTileLayer`.

```python
from llmaps.sources import VectorTileSource

VectorTileSource(
    id: str,
    tiles_url: str,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | str | required | Source identifier. |
| `tiles_url` | str | required | URL template with `{z}`, `{x}`, `{y}` placeholders (e.g. `https://example.com/tiles/{z}/{x}/{y}.pbf`). |

**When to use:** Large datasets served as vector tiles; on-demand loading.

---

## See also

- [Layers](layers.md) — layers consume sources
- [Map](map.md) — embedded mode and config
- [API_GUIDE.md](../../API_GUIDE.md) — index and keywords
