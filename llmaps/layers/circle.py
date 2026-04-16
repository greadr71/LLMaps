"""CircleLayer implementation for point rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .base import BaseLayer

if TYPE_CHECKING:
    from ..components.data_driven_size import DataDrivenSize


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
    stroke_width:
        Stroke width in pixels (number) or MapLibre expression (list).
        Default is 0 (no stroke).
    stroke_color:
        Stroke color (hex string) or MapLibre expression (list).
    stroke_opacity:
        Stroke opacity 0–1 (number) or MapLibre expression (list).
    data_driven_size:
        When set and the layer source is a local :class:`~llmaps.sources.file.FileSource`,
        :meth:`llmaps.map.Map.to_dict` replaces ``circle-radius`` (and attaches a size
        legend) using percentiles of *data_driven_size.field* in the loaded file.
    """

    radius: Union[float, List[Any]] = 6.0
    color: Union[str, List[Any]] = "#3182bd"
    opacity: Union[float, List[Any]] = 0.8
    stroke_width: Union[float, List[Any]] = 0
    stroke_color: Union[str, List[Any]] = "#000000"
    stroke_opacity: Union[float, List[Any]] = 1.0
    data_driven_size: Optional["DataDrivenSize"] = None

    layer_type: str = "circle"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["paint"] = {
            "circle-radius": self.radius,
            "circle-color": self.color,
            "circle-opacity": self.opacity,
            "circle-stroke-width": self.stroke_width,
            "circle-stroke-color": self.stroke_color,
            "circle-stroke-opacity": self.stroke_opacity,
        }
        return base

