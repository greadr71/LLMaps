"""VectorTileLayer for Mapbox Vector Tiles (PBF) with optional dynamic_stats."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple

from .base import BaseLayer
from ..sources.vector_tile import VectorTileSource

GeometryType = Literal["circle", "fill", "line"]


@dataclass
class VectorTileLayer(BaseLayer):
    """Layer that draws data from vector tiles (PBF).

    Parameters
    ----------
    id:
        Unique layer identifier.
    source:
        VectorTileSource (tiles_url).
    source_layer:
        Layer name inside the PBF (MapLibre source-layer).
    geometry_type:
        circle, fill, or line.
    dynamic_stats:
        If True, gradient stats (q05/q95) are computed on the client from viewport data.
    property_field:
        Numeric property for gradient styling.
    colors:
        Two or more colors for gradient.
    radius_range:
        [min, max] radius in pixels for circle type.
    opacity:
        Fill/circle opacity.
    """

    source_layer: str = ""
    geometry_type: GeometryType = "circle"
    dynamic_stats: bool = False
    property_field: Optional[str] = None
    colors: List[str] = field(default_factory=lambda: ["#e0d4f7", "#6829c5"])
    radius_range: Optional[Tuple[float, float]] = None
    opacity: float = 0.8

    def __post_init__(self) -> None:
        if not isinstance(self.source, VectorTileSource):
            raise TypeError("VectorTileLayer requires a VectorTileSource")

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["type"] = self.geometry_type
        base["metadata"] = {
            **base.get("metadata", {}),
            "layer_type": "vector-tile",
            "tiles_url": self.source.tiles_url,
            "source_layer": self.source_layer,
            "geometry_type": self.geometry_type,
            "dynamic_stats": self.dynamic_stats,
            "property_field": self.property_field,
            "colors": self.colors,
            "radius_range": self.radius_range,
            "opacity": self.opacity,
        }

        r_min, r_max = self.radius_range or (5.0, 12.0)
        if self.geometry_type == "circle":
            if self.property_field and len(self.colors) >= 2:
                base["paint"] = {
                    "circle-radius": [
                        "interpolate",
                        ["linear"],
                        ["get", self.property_field],
                        0,
                        r_min,
                        1,
                        r_max,
                    ],
                    "circle-color": [
                        "interpolate",
                        ["linear"],
                        ["get", self.property_field],
                        0,
                        self.colors[0],
                        1,
                        self.colors[-1],
                    ],
                    "circle-opacity": self.opacity,
                }
            else:
                base["paint"] = {
                    "circle-radius": (r_min + r_max) / 2.0,
                    "circle-color": self.colors[0] if self.colors else "#3182bd",
                    "circle-opacity": self.opacity,
                }
        elif self.geometry_type == "fill":
            base["paint"] = {
                "fill-color": self.colors[0] if self.colors else "#3182bd",
                "fill-opacity": self.opacity,
            }
            if self.property_field and len(self.colors) >= 2:
                base["paint"]["fill-color"] = [
                    "interpolate",
                    ["linear"],
                    ["get", self.property_field],
                    0,
                    self.colors[0],
                    1,
                    self.colors[-1],
                ]
        else:
            base["paint"] = {
                "line-color": self.colors[0] if self.colors else "#3182bd",
                "line-width": 2,
                "line-opacity": self.opacity,
            }

        base["source-layer"] = self.source_layer
        return base
