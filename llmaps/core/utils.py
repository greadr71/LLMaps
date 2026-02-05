"""
Shared utility functions for LLMaps internals.

Provides data loading (FileSource -> GeoDataFrame), H3 aggregation,
bounds/zoom calculation, and GeoJSON serialisation for embedded mode.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

AggregationKind = Literal["count", "sum", "mean", "median"]


def load_gdf_from_file_source(source: Any) -> Any:
    """Load a GeoDataFrame from a FileSource.

    Supports GeoJSON, CSV (with lon/lat columns), and Parquet.
    """
    import geopandas as gpd
    import pandas as pd

    path = Path(source.path)
    fmt = getattr(source, "file_format", None) or _infer_format(path)

    if fmt == "geojson":
        return gpd.read_file(path)
    if fmt == "parquet":
        return gpd.read_parquet(path)
    if fmt == "csv":
        df = pd.read_csv(path)
        if "lon" in df.columns and "lat" in df.columns:
            return gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df["lon"], df["lat"]),
                crs="EPSG:4326",
            )
        if "longitude" in df.columns and "latitude" in df.columns:
            return gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
                crs="EPSG:4326",
            )
        raise ValueError(
            "CSV must contain 'lon'/'lat' or 'longitude'/'latitude' columns"
        )
    raise ValueError(f"Unsupported file format: {fmt}")


def _infer_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".geojson", ".json"}:
        return "geojson"
    if suffix == ".csv":
        return "csv"
    if suffix in {".parquet", ".pq"}:
        return "parquet"
    raise ValueError(f"Cannot infer format from extension: {suffix}")


def load_gdf(source: Any) -> Optional[Any]:
    """Load a GeoDataFrame from any supported source.

    Supports FileSource. Returns None for ApiSource and VectorTile-like
    sources (no local geometry). Used by auto_extent and embedded mode.
    """
    from ..sources.base import BaseSource
    from ..sources.file import FileSource

    if isinstance(source, FileSource):
        return load_gdf_from_file_source(source)
    if isinstance(source, BaseSource):
        # ApiSource, etc. — no local load
        return None
    return None


def gdf_to_geojson_dict(gdf: Any) -> Dict[str, Any]:
    """Convert a GeoDataFrame to a GeoJSON-like dict (FeatureCollection)."""
    return gdf.__geo_interface__


def aggregate_h3(
    gdf: Any,
    resolution: int = 8,
    aggregation: AggregationKind = "count",
    h3_column: Optional[str] = None,
    value_field: Optional[str] = None,
) -> Any:
    """Aggregate point geometries into H3 hexagons.

    If h3_column is given and present in gdf, use it and aggregate by it.
    Otherwise convert geometry to H3 at the given resolution and aggregate.

    Parameters
    ----------
    gdf : GeoDataFrame
        Point data (or data with h3_column).
    resolution : int
        H3 resolution 0–15 (used when h3_column is not used).
    aggregation : str
        One of count, sum, mean, median.
    h3_column : str, optional
        Column name for H3 indices; if None, points are converted to H3.
    value_field : str, optional
        Field for sum/mean/median; required for non-count aggregation.

    Returns
    -------
    GeoDataFrame
        One row per H3 cell with geometry (polygon) and value column.
    """
    try:
        import h3
    except ImportError as e:
        raise ImportError(
            "H3 aggregation requires the h3 package. Install with: pip install h3"
        ) from e

    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import Polygon

    out_value_col = value_field or "value"

    if h3_column and h3_column in gdf.columns:
        h3_indices = gdf[h3_column]
    else:

        def point_to_h3(pt):
            if pt is None or pt.is_empty:
                return None
            return h3.latlng_to_cell(pt.y, pt.x, resolution)

        h3_indices = gdf.geometry.apply(point_to_h3)
        h3_indices = h3_indices.dropna()

    if aggregation == "count":
        agg_df = h3_indices.value_counts().reset_index()
        agg_df.columns = ["h3_index", out_value_col]
    elif value_field and value_field in gdf.columns:
        agg = gdf.assign(h3_index=h3_indices).groupby("h3_index")[value_field]
        if aggregation == "sum":
            agg_df = agg.sum().reset_index()
        elif aggregation == "mean":
            agg_df = agg.mean().reset_index()
        elif aggregation == "median":
            agg_df = agg.median().reset_index()
        else:
            raise ValueError(f"Unknown aggregation: {aggregation}")
        agg_df.columns = ["h3_index", out_value_col]
    else:
        raise ValueError(
            f"Aggregation '{aggregation}' requires value_field in the data"
        )

    def h3_to_polygon(cell):
        boundary = h3.cell_to_boundary(cell)
        coords = [(lng, lat) for lat, lng in boundary]
        return Polygon(coords)

    agg_df["geometry"] = agg_df["h3_index"].apply(h3_to_polygon)
    return gpd.GeoDataFrame(agg_df, geometry="geometry", crs="EPSG:4326")


def compute_value_stats(
    gdf: Any, value_field: str
) -> Dict[str, float]:
    """Compute q05/q95 (and min/max) for a numeric column."""
    import pandas as pd

    values = gdf[value_field].dropna()
    if values.empty:
        return {"q05": 0.0, "q95": 1.0, "min": 0.0, "max": 1.0}
    return {
        "q05": float(values.quantile(0.05)),
        "q95": float(values.quantile(0.95)),
        "min": float(values.min()),
        "max": float(values.max()),
    }


def bounds_center(bounds: Sequence[float]) -> List[float]:
    """Return [lon, lat] center from (minx, miny, maxx, maxy)."""
    minx, miny, maxx, maxy = bounds
    return [(minx + maxx) / 2.0, (miny + maxy) / 2.0]


def bounds_to_zoom(
    bounds: Sequence[float],
    padding: float = 0.1,
    min_zoom: int = 1,
    max_zoom: int = 18,
) -> int:
    """Compute zoom level from bbox in degrees.

    Uses log2(360 / max_diff) and optionally reduces zoom for padding.
    """
    minx, miny, maxx, maxy = bounds
    lat_diff = maxy - miny
    lon_diff = maxx - minx
    max_diff = max(lat_diff, lon_diff)
    if max_diff <= 0:
        return max_zoom
    zoom = int(math.log2(360.0 / max_diff))
    if padding > 0:
        zoom = max(min_zoom, zoom - 1)
    return max(min_zoom, min(max_zoom, zoom))
