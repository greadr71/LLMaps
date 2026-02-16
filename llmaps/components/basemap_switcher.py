"""BasemapSwitcher component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .base import BaseComponent


@dataclass
class BasemapSwitcher(BaseComponent):
    """Dropdown to switch the map basemap (tile layer).

    Parameters
    ----------
    position:
        Where to place the switcher control.
    basemaps:
        List of basemap identifiers (e.g. ["osm", "carto-light", "carto-dark"]).
        If not provided, uses all available basemaps from the map configuration.
    """

    position: str = "top-right"
    basemaps: list = None

    def __post_init__(self) -> None:
        self.component_type = "basemap_switcher"
        if self.basemaps is None:
            self.basemaps = []

    def to_dict(self) -> Dict[str, object]:
        base = super().to_dict()
        base["position"] = self.position
        base["basemaps"] = list(self.basemaps)
        return base
