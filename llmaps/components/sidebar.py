"""Sidebar component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Mapping, Optional

from .base import BaseComponent

Position = Literal["left", "right"]


@dataclass
class Sidebar(BaseComponent):
    """Sliding sidebar panel that displays feature attributes on click.

    The sidebar opens when a user clicks on a feature in one of the
    configured layers.  It shows the feature's attributes in a
    structured layout with labelled fields.

    Parameters
    ----------
    position:
        Which side of the screen to attach the sidebar.
    width:
        Panel width in pixels.
    fields_by_layer:
        Mapping from layer id to ordered list of attribute names to
        display when a feature of that layer is clicked.
    field_labels:
        Optional mapping from attribute name to human-readable label.
        Applied across all layers.
    title_field:
        Optional attribute name used as the sidebar header title.
        If the clicked feature has this field, its value is shown as
        the panel title instead of the default "Feature info".
    title_by_layer:
        Optional per-layer static title for the sidebar header.
    show_on_click:
        Whether the sidebar opens automatically on feature click.
    close_on_map_click:
        Whether clicking on the map (not on a feature) closes the sidebar.
    zoom_on_click:
        Optional zoom level to fly to when a feature is clicked.
    """

    position: Position = "right"
    width: int = 400
    fields_by_layer: Mapping[str, List[str]] = field(default_factory=dict)
    field_labels: Mapping[str, str] = field(default_factory=dict)
    title_field: Optional[str] = None
    title_by_layer: Mapping[str, str] = field(default_factory=dict)
    show_on_click: bool = True
    close_on_map_click: bool = True
    zoom_on_click: Optional[float] = None

    def __post_init__(self) -> None:
        self.component_type = "sidebar"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "position": self.position,
                "width": self.width,
                "fields_by_layer": {k: list(v) for k, v in self.fields_by_layer.items()},
                "field_labels": dict(self.field_labels),
                "title_field": self.title_field,
                "title_by_layer": dict(self.title_by_layer),
                "show_on_click": self.show_on_click,
                "close_on_map_click": self.close_on_map_click,
                "zoom_on_click": self.zoom_on_click,
            }
        )
        return base
