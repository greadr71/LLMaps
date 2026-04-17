"""CircleLayer implementation for point rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

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
        When set, :meth:`llmaps.map.Map.to_dict` can replace ``circle-radius`` (and
        attach a size legend) using :class:`~llmaps.components.data_driven_size.DataDrivenSize`.

        If ``data_driven_size_values`` is set, percentiles are taken from that numeric
        sample (e.g. values you fetched from an API before ``save()``). Otherwise, when
        the source is a local :class:`~llmaps.sources.file.FileSource`, values are read
        from the file column ``data_driven_size.field``.
    data_driven_size_values:
        Optional numeric sample (list, tuple, 1-D array) for ``DataDrivenSize`` resolution
        at ``to_dict()`` time **without** reading a ``FileSource``. Still **frozen at HTML
        export**—refresh the sample and re-export for newer distributions; for per-session
        updates in the browser, use client-side expressions instead.
    data_driven_size_client:
        If ``True`` with ``data_driven_size`` set, :meth:`~llmaps.map.Map.to_dict` does
        **not** resolve paint at export time. Instead it stores
        ``metadata["llmaps_data_driven_size_spec"]`` for use in the browser with
        ``llmapsApplyDataDrivenSizeFromValues`` (bundled JS). Ignores
        ``data_driven_size_values`` and ``FileSource`` for sizing.
    """

    radius: Union[float, List[Any]] = 6.0
    color: Union[str, List[Any]] = "#3182bd"
    opacity: Union[float, List[Any]] = 0.8
    stroke_width: Union[float, List[Any]] = 0
    stroke_color: Union[str, List[Any]] = "#000000"
    stroke_opacity: Union[float, List[Any]] = 1.0
    data_driven_size: Optional["DataDrivenSize"] = None
    data_driven_size_values: Optional[Sequence[float]] = None
    data_driven_size_client: bool = False

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

