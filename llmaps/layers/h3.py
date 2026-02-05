"""H3Layer implementation for hexagonal aggregation and visualization."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple

from .base import BaseLayer

AggregationKind = Literal["count", "sum", "mean", "median"]


@dataclass
class H3Layer(BaseLayer):
    """Hexagon layer with H3 aggregation (count/sum/mean/median).

    Use for large point datasets: points are aggregated into H3 cells
    and rendered as fill polygons with optional gradient by a value field.

    Parameters
    ----------
    id:
        Unique layer identifier.
    source:
        Data source: point geometries, or pre-aggregated data with h3_column.
    h3_column:
        Column name for H3 indices. If None, points are converted to H3.
    resolution:
        H3 resolution 0–15 (default 8, ~460 m).
    aggregation:
        One of count, sum, mean, median.
    property_field:
        Field used for sum/mean/median and for color gradient.
    colors:
        Two or more colors for gradient (data-driven fill).
    opacity:
        Fill opacity 0–1.
    stroke_width:
        Outline width in pixels.
    stroke_color:
        Outline color.
    """

    h3_column: Optional[str] = None
    resolution: int = 8
    aggregation: AggregationKind = "count"
    property_field: str = "value"
    colors: List[str] = field(
        default_factory=lambda: ["#ffffcc", "#800026"]
    )
    opacity: float = 0.7
    stroke_width: float = 0.0
    stroke_color: Optional[str] = None

    # Optional stats (q05, q95) for gradient; set when data is prepared
    _stats: Optional[Dict[str, float]] = field(default=None, repr=False)

    layer_type: str = "fill"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["metadata"] = {
            **base.get("metadata", {}),
            "h3_column": self.h3_column,
            "resolution": self.resolution,
            "aggregation": self.aggregation,
            "property_field": self.property_field,
        }
        if self._stats is not None:
            base["metadata"]["stats"] = self._stats

        q05 = 0.0
        q95 = 1.0
        if self._stats:
            q05 = self._stats.get("q05", q05)
            q95 = self._stats.get("q95", q95)

        # Data-driven fill: interpolate by property_field between colors
        if len(self.colors) >= 2:
            stops: List[Any] = [q05, self.colors[0], q95, self.colors[-1]]
            if len(self.colors) > 2:
                step = (q95 - q05) / (len(self.colors) - 1) if q95 != q05 else 0
                stops = []
                for i, c in enumerate(self.colors):
                    t = q05 + i * step if q95 != q05 else q05
                    stops.extend([t, c])
            base["paint"] = {
                "fill-color": [
                    "interpolate",
                    ["linear"],
                    ["get", self.property_field],
                    *stops,
                ],
                "fill-opacity": self.opacity,
            }
        else:
            base["paint"] = {
                "fill-color": self.colors[0] if self.colors else "#888",
                "fill-opacity": self.opacity,
            }

        if self.stroke_width and self.stroke_color:
            base["paint"]["outline-width"] = self.stroke_width
            base["paint"]["outline-color"] = self.stroke_color

        return base

    def set_stats(self, stats: Dict[str, float]) -> "H3Layer":
        """Set q05/q95 (and optionally min/max) for gradient. Returns self."""
        self._stats = dict(stats)
        return self
