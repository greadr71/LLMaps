"""BasemapSwitcher component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .base import BaseComponent


@dataclass
class BasemapSwitcher(BaseComponent):
    """Dropdown to switch the map basemap (tile layer).

    Requires Map to be created with tile_providers set (list of provider ids).
    """

    position: str = "top-left"

    def __post_init__(self) -> None:
        self.component_type = "basemap_switcher"

    def to_dict(self) -> Dict[str, object]:
        base = super().to_dict()
        base["position"] = self.position
        return base
