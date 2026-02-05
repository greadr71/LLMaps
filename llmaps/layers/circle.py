"""CircleLayer implementation for point rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Union

from .base import BaseLayer


@dataclass
class CircleLayer(BaseLayer):
    """Point layer rendered as circles.

    Parameters
    ----------
    id:
        Unique layer identifier.
    source:
        Underlying data source containing point geometries.
    radius:
        Circle radius in pixels (number) or MapLibre expression (list).
    color:
        Fill color (hex string) or MapLibre expression (list).
    opacity:
        Fill opacity 0–1 (number) or MapLibre expression (list).
    """

    radius: Union[float, List[Any]] = 6.0
    color: Union[str, List[Any]] = "#3182bd"
    opacity: Union[float, List[Any]] = 0.8

    layer_type: str = "circle"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["paint"] = {
            "circle-radius": self.radius,
            "circle-color": self.color,
            "circle-opacity": self.opacity,
        }
        return base

