"""FillLayer implementation for polygon rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .base import BaseLayer


@dataclass
class FillLayer(BaseLayer):
    """Polygon layer with fill and optional stroke.

    Parameters
    ----------
    id:
        Unique layer identifier.
    source:
        Underlying data source containing polygon geometries.
    fill_color:
        CSS color string for the polygon fill.
    fill_opacity:
        Opacity for the fill, between 0 and 1.
    stroke_color:
        CSS color string for the polygon outline.
    stroke_width:
        Line width in pixels for the polygon outline.
    """

    fill_color: str = "#3182bd"
    fill_opacity: float = 0.6
    stroke_color: Optional[str] = "#08519c"
    stroke_width: Optional[float] = 1.0

    layer_type: str = "fill"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        paint: Dict[str, Any] = {
            "fill-color": self.fill_color,
            "fill-opacity": self.fill_opacity,
        }

        if self.stroke_color is not None:
            paint["outline-color"] = self.stroke_color
        if self.stroke_width is not None:
            paint["outline-width"] = self.stroke_width

        base["paint"] = paint
        return base

