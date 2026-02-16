"""Legend component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional

from .base import BaseComponent


@dataclass
class Legend(BaseComponent):
    """Simple layer legend configuration.

    Parameters
    ----------
    position:
        CSS-like position token: ``"top-left"``, ``"top-right"``,
        ``"bottom-left"`` or ``"bottom-right"``.
    title:
        Optional title for the legend panel. If not set, the map title
        (config.title) or "Карта" is used.
    description:
        Optional description text displayed under the title.
    entries:
        Optional list of simple legend entries, each with "label" and "color".
        Example: [{"label": "Category A", "color": "#ff0000"}]
    color_ramp:
        Optional color ramp dict with "colors" (list of hex codes) and
        "labels" (list of labels). Alternative to layer_color_ramps for
        simple cases not tied to specific layers.
    collapsible:
        Whether the legend can be collapsed/expanded by the user.
    show_toggle:
        Whether each layer can be toggled on/off from the legend.
    layer_labels:
        Optional mapping from layer id to human-readable label.
    layer_counts:
        Optional mapping from layer id to precomputed feature counts.
        These are displayed as static numbers; dynamic counts in JS are
        intentionally out of scope for the MVP.
    layer_color_ramps:
        Optional mapping from layer id to a dict with ``stops``
        (list of [value, "#hex"]), ``label_min`` and ``label_max``,
        to show a color scale in the legend (e.g. for population).
    layer_descriptions:
        Optional mapping from layer id to text descriptions displayed
        under each layer in the legend.
    instructions:
        Optional list of tip strings to display in a collapsible
        "Tips" section at the bottom of the legend.
    collapsed:
        Whether the Tips section should be collapsed by default.
    """

    position: str = "top-right"
    title: Optional[str] = None
    description: Optional[str] = None
    entries: Optional[list] = None
    color_ramp: Optional[Dict[str, object]] = None
    collapsible: bool = False
    show_toggle: bool = True
    layer_labels: Mapping[str, str] = field(default_factory=dict)
    layer_counts: Mapping[str, int] = field(default_factory=dict)
    layer_color_ramps: Optional[Mapping[str, Dict[str, object]]] = None
    layer_descriptions: Mapping[str, str] = field(default_factory=dict)
    instructions: Optional[list[str]] = None
    collapsed: bool = True

    def __post_init__(self) -> None:
        self.component_type = "legend"

    def to_dict(self) -> Dict[str, object]:
        base = super().to_dict()
        base.update(
            {
                "position": self.position,
                "collapsible": self.collapsible,
                "show_toggle": self.show_toggle,
                "layer_labels": dict(self.layer_labels),
                "layer_counts": dict(self.layer_counts),
                "layer_descriptions": dict(self.layer_descriptions),
                "collapsed": self.collapsed,
            }
        )
        if self.title is not None:
            base["title"] = self.title
        if self.description is not None:
            base["description"] = self.description
        if self.entries is not None:
            base["entries"] = list(self.entries)
        if self.color_ramp is not None:
            base["color_ramp"] = dict(self.color_ramp)
        if self.layer_color_ramps:
            base["layer_color_ramps"] = dict(self.layer_color_ramps)
        if self.instructions:
            base["instructions"] = list(self.instructions)
        return base

