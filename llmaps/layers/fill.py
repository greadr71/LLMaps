"""FillLayer implementation for polygon rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

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
        CSS color string or MapLibre expression (list) for the polygon fill.
        Supports feature-state expressions for dynamic styling.
    fill_opacity:
        Opacity 0–1 (number) or MapLibre expression (list) for the fill.
    stroke_color:
        CSS color string for the polygon outline.
    stroke_width:
        Line width in pixels for the polygon outline.
    """

    fill_color: Union[str, List[Any]] = "#3182bd"
    fill_opacity: Union[float, List[Any]] = 0.6
    stroke_color: Optional[str] = "#08519c"
    stroke_width: Optional[float] = 1.0

    layer_type: str = "fill"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        paint: Dict[str, Any] = {
            "fill-color": self.fill_color,
            "fill-opacity": self.fill_opacity,
        }

        # MapLibre GL JS поддерживает только fill-outline-color (ширина всегда 1px)
        # Для толстой обводки (>1px) нужен отдельный line слой
        if self.stroke_color is not None:
            if self.stroke_width is None or self.stroke_width <= 1:
                # Тонкая обводка: используем fill-outline-color
                paint["fill-outline-color"] = self.stroke_color
            else:
                # Толстая обводка: сохраняем в metadata для генерации line слоя
                base["metadata"]["needs_outline_layer"] = True
                base["metadata"]["outline_color"] = self.stroke_color
                base["metadata"]["outline_width"] = self.stroke_width

        base["paint"] = paint
        return base

