"""Storytelling (scrollytelling) component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from .base import BaseComponent


@dataclass
class Scene:
    """A single scene (step) in a scrollytelling narrative.

    Parameters
    ----------
    id:
        Unique identifier for the scene.
    title:
        Scene heading displayed in the narrative panel.
    content:
        HTML body text for the scene.
    center:
        Map center ``[lon, lat]`` to fly to.  *None* keeps current position.
    zoom:
        Map zoom level.  *None* keeps current zoom.
    bearing:
        Map bearing (rotation) in degrees.
    pitch:
        Map pitch (tilt) in degrees.
    visible_layers:
        Layer ids to show during this scene.  *None* means "don't change",
        an empty list hides all layers.
    highlight:
        Features to highlight via feature-state.
        Mapping of ``{source_id: [feature_id, ...]}``.
    fly_duration:
        Camera animation duration in milliseconds.
    """

    id: str
    title: str
    content: str
    center: Optional[List[float]] = None
    zoom: Optional[float] = None
    bearing: float = 0
    pitch: float = 0
    visible_layers: Optional[List[str]] = None
    highlight: Dict[str, List] = field(default_factory=dict)
    fly_duration: int = 2000

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "bearing": self.bearing,
            "pitch": self.pitch,
            "flyDuration": self.fly_duration,
        }
        if self.center is not None:
            d["center"] = self.center
        if self.zoom is not None:
            d["zoom"] = self.zoom
        if self.visible_layers is not None:
            d["visibleLayers"] = self.visible_layers
        if self.highlight:
            d["highlight"] = self.highlight
        return d


@dataclass
class Storytelling(BaseComponent):
    """Scrollytelling component with a narrative panel and map reactions.

    Adds a scrollable text panel alongside the map.  As the user scrolls
    through scenes, the map camera, layer visibility, and feature highlights
    update automatically.

    Parameters
    ----------
    scenes:
        Ordered list of :class:`Scene` objects defining the narrative.
    position:
        Side of the screen for the narrative panel.
    width:
        Narrative panel width in pixels.
    progress:
        Whether to show a clickable navigation dot indicator.
    """

    scenes: List[Scene] = field(default_factory=list)
    position: Literal["left", "right"] = "left"
    width: int = 400
    progress: bool = True

    def __post_init__(self) -> None:
        self.component_type = "storytelling"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "scenes": [s.to_dict() for s in self.scenes],
                "position": self.position,
                "width": self.width,
                "progress": self.progress,
            }
        )
        return base
