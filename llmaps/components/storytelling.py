"""Storytelling (scrollytelling) component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from .base import BaseComponent


@dataclass
class SceneComparison:
    """Per-scene comparison slider configuration.

    When a :class:`Scene` has a ``comparison`` set, the map shows a
    before/after slider overlay for that scene.  The main map is hidden
    behind two comparison map instances (created lazily on first use).

    Parameters
    ----------
    before_layers:
        Layer ids to show on the *left* (before) side of the slider.
    after_layers:
        Layer ids to show on the *right* (after) side of the slider.
    before_label:
        Optional label displayed on the before panel (e.g. ``"2016"``).
    after_label:
        Optional label displayed on the after panel (e.g. ``"2018"``).
    before_highlight:
        Features to highlight on the before map.
        Mapping of ``{source_id: [feature_id, ...]}``.
    after_highlight:
        Features to highlight on the after map.
        Mapping of ``{source_id: [feature_id, ...]}``.
    """

    before_layers: List[str] = field(default_factory=list)
    after_layers: List[str] = field(default_factory=list)
    before_label: Optional[str] = None
    after_label: Optional[str] = None
    before_highlight: Dict[str, List] = field(default_factory=dict)
    after_highlight: Dict[str, List] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "beforeLayers": self.before_layers,
            "afterLayers": self.after_layers,
        }
        if self.before_label is not None:
            d["beforeLabel"] = self.before_label
        if self.after_label is not None:
            d["afterLabel"] = self.after_label
        if self.before_highlight:
            d["beforeHighlight"] = self.before_highlight
        if self.after_highlight:
            d["afterHighlight"] = self.after_highlight
        return d


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
    comparison:
        Optional per-scene comparison slider configuration.  When set, the
        scene displays a before/after slider overlay.  ``visible_layers``
        and ``highlight`` are ignored in favour of the comparison config.
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
    comparison: Optional[SceneComparison] = None

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
        if self.comparison is not None:
            d["comparison"] = self.comparison.to_dict()
        return d


@dataclass
class Storytelling(BaseComponent):
    """Scrollytelling narrative panel.

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
    comparison_slider_hint:
        Custom tooltip text shown when the comparison slider first appears
        (e.g. ``"Drag to compare"``).  *None* uses a locale-aware default.
        Only relevant when at least one scene has a ``comparison`` set.
    comparison_slider_start_pct:
        Initial slider position as a fraction of map width in ``[0.0, 1.0]``.
        ``0.1`` means 10% from the left edge.
    """

    scenes: List[Scene] = field(default_factory=list)
    position: Literal["left", "right"] = "left"
    width: int = 400
    progress: bool = True
    comparison_slider_hint: Optional[str] = None
    comparison_slider_start_pct: float = 0.5

    def __post_init__(self) -> None:
        self.component_type = "storytelling"

    @property
    def has_comparison(self) -> bool:
        """Return True if any scene uses a comparison slider."""
        return any(s.comparison is not None for s in self.scenes)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "scenes": [s.to_dict() for s in self.scenes],
                "position": self.position,
                "width": self.width,
                "progress": self.progress,
                "hasComparison": self.has_comparison,
            }
        )
        if self.comparison_slider_hint is not None:
            base["comparisonSliderHint"] = self.comparison_slider_hint
        base["comparisonSliderStartPct"] = max(0.0, min(1.0, float(self.comparison_slider_start_pct)))
        return base
