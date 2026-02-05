"""Controls component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .base import BaseComponent


@dataclass
class Controls(BaseComponent):
    """Map UI controls configuration.

    Parameters
    ----------
    zoom:
        Show zoom in/out buttons.
    scale:
        Show scale bar.
    fullscreen:
        Show fullscreen toggle.
    """

    zoom: bool = True
    scale: bool = True
    fullscreen: bool = False

    def __post_init__(self) -> None:
        self.component_type = "controls"

    def to_dict(self) -> Dict[str, object]:
        base = super().to_dict()
        base.update(
            {
                "zoom": self.zoom,
                "scale": self.scale,
                "fullscreen": self.fullscreen,
            }
        )
        return base

