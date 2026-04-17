"""SymbolLayer — MapLibre GL JS 'symbol' layer (icon markers and text labels).

Supports icon images pre-registered with ``map.addImage()`` and optional text labels.
Works with both GeoJSON sources (FileSource, ApiSource) and vector tile sources
(VectorTileSource) — set ``source_layer`` only for PBF tiles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

from .base import BaseLayer

if TYPE_CHECKING:
    from ..components.data_driven_size import DataDrivenSize


@dataclass
class SymbolLayer(BaseLayer):
    """Point layer rendered as icon markers with optional text labels.

    Parameters
    ----------
    id:
        Unique layer identifier.
    source:
        Data source (FileSource, ApiSource, or VectorTileSource).
    source_layer:
        Layer name inside the PBF.  Set only when using a VectorTileSource.
        If ``None`` or empty string, the ``source-layer`` key is omitted from
        the serialized config (compatible with GeoJSON sources).
    icon_image:
        Name of a pre-registered image (string) or a MapLibre expression
        (list) that resolves to an image name per feature.  If ``None``,
        no icon is drawn (useful for text-only symbol layers).
    icon_size:
        Scaling factor applied to the icon image (1.0 = original size).
    icon_anchor:
        Part of the icon anchored to the feature's coordinate.
        One of: ``"center"``, ``"left"``, ``"right"``, ``"top"``,
        ``"bottom"``, ``"top-left"``, ``"top-right"``, ``"bottom-left"``,
        ``"bottom-right"``.
    icon_allow_overlap:
        If True, icons are always drawn even when they collide with other symbols.
        Recommended True for dense datasets.
    icon_ignore_placement:
        If True, other symbols can overlap this icon.
    icon_offset:
        [dx, dy] offset in pixels from the anchor point.
    icon_opacity:
        Icon opacity (0–1).
    text_field:
        Feature property name whose value is shown as a text label.
        Pass a plain string (e.g. ``"name"``) — it will be auto-wrapped as
        ``["get", "name"]``.  Pass a full MapLibre expression (list) to
        control the text value yourself.  ``None`` disables text.
    text_size:
        Font size for the text label in pixels.
    text_anchor:
        Anchor for the text label (same values as ``icon_anchor``).
    text_offset:
        [dx, dy] offset for the text label in *ems*.
    text_color:
        Text fill color.
    text_opacity:
        Text opacity (0–1).
    text_halo_color:
        Color of the halo drawn around the text for legibility.
    text_halo_width:
        Width of the text halo in pixels (0 = no halo).
    data_driven_size:
        Same as :attr:`CircleLayer.data_driven_size`, applied to ``icon-size`` in the
        layer layout when resolved.
    data_driven_size_values:
        Same as :attr:`CircleLayer.data_driven_size_values` (optional numeric sample for
        resolution without a ``FileSource``).
    data_driven_size_client:
        Same as :attr:`CircleLayer.data_driven_size_client`.
    """

    source_layer: Optional[str] = None

    # Layout — icon
    icon_image: Optional[Union[str, List[Any]]] = None
    icon_size: float = 1.0
    icon_anchor: str = "center"
    icon_allow_overlap: bool = True
    icon_ignore_placement: bool = False
    icon_offset: List[float] = field(default_factory=lambda: [0.0, 0.0])

    # Paint — icon
    icon_opacity: float = 1.0

    # Layout — text
    text_field: Optional[Union[str, List[Any]]] = None
    text_size: float = 12.0
    text_font: List[str] = field(default_factory=lambda: ["Open Sans Regular", "Arial Unicode MS Regular"])
    text_anchor: str = "top"
    text_offset: List[float] = field(default_factory=lambda: [0.0, 0.5])

    # Paint — text
    text_color: str = "#222222"
    text_opacity: float = 1.0
    text_halo_color: str = "rgba(255,255,255,0.8)"
    text_halo_width: float = 0.0
    data_driven_size: Optional["DataDrivenSize"] = None
    data_driven_size_values: Optional[Sequence[float]] = None
    data_driven_size_client: bool = False

    layer_type: str = "symbol"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["type"] = "symbol"

        # ── Layout ────────────────────────────────────────────────────────────
        layout: Dict[str, Any] = {
            "icon-size": self.icon_size,
            "icon-anchor": self.icon_anchor,
            "icon-allow-overlap": self.icon_allow_overlap,
            "icon-ignore-placement": self.icon_ignore_placement,
            "icon-offset": self.icon_offset,
        }

        if self.icon_image is not None:
            layout["icon-image"] = self.icon_image

        # text_field: auto-wrap plain property names
        if self.text_field is not None:
            if isinstance(self.text_field, list):
                tf = self.text_field
            else:
                tf = ["get", self.text_field]
            layout["text-field"] = tf
            layout["text-font"] = self.text_font
            layout["text-size"] = self.text_size
            layout["text-anchor"] = self.text_anchor
            layout["text-offset"] = self.text_offset

        base["layout"] = layout

        # ── Paint ─────────────────────────────────────────────────────────────
        paint: Dict[str, Any] = {
            "icon-opacity": self.icon_opacity,
        }

        if self.text_field is not None:
            paint["text-color"] = self.text_color
            paint["text-opacity"] = self.text_opacity
            if self.text_halo_width > 0:
                paint["text-halo-color"] = self.text_halo_color
                paint["text-halo-width"] = self.text_halo_width

        base["paint"] = paint

        # ── source-layer (VectorTile only) ────────────────────────────────────
        if self.source_layer:
            base["source-layer"] = self.source_layer

        return base
