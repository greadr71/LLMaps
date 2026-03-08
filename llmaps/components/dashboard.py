"""Dashboard component for persistent map overlays."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Mapping, Optional

from .base import BaseComponent

DashboardPosition = Literal["top-left", "top-right", "bottom-left", "bottom-right"]
DashboardFilterType = Literal["select", "date", "text"]


@dataclass
class Dashboard(BaseComponent):
    """Persistent overlay panel for map dashboards.

    Parameters
    ----------
    dashboard_id:
        Stable dashboard identifier used by the frontend JS bridge.
    position:
        Overlay position on the map viewport.
    title:
        Optional dashboard title rendered in the header.
    width:
        Panel width in pixels.
    height:
        Optional maximum height in pixels.
    collapsible:
        Whether the panel can be collapsed by the user.
    collapsed:
        Whether the panel starts in collapsed state.
    filters:
        Ordered list of filter descriptors. Supported types: ``select``, ``date``, ``text``.
    content_html:
        Initial HTML rendered in the dashboard body.
    empty_state:
        Fallback text when ``content_html`` is empty.
    """

    dashboard_id: str = "dashboard"
    position: DashboardPosition = "top-right"
    title: Optional[str] = None
    width: int = 360
    height: Optional[int] = None
    collapsible: bool = True
    collapsed: bool = False
    filters: List[Mapping[str, Any]] = field(default_factory=list)
    content_html: str = ""
    empty_state: str = "No dashboard content yet."

    def __post_init__(self) -> None:
        self.component_type = "dashboard"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "dashboard_id": self.dashboard_id,
                "position": self.position,
                "title": self.title,
                "width": self.width,
                "height": self.height,
                "collapsible": self.collapsible,
                "collapsed": self.collapsed,
                "filters": [dict(item) for item in self.filters],
                "content_html": self.content_html,
                "empty_state": self.empty_state,
            }
        )
        return base