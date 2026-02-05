"""Vector tile source for PBF tiles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .base import BaseSource


@dataclass
class VectorTileSource(BaseSource):
    """Source for vector tiles (PBF). Used by VectorTileLayer.

    Parameters
    ----------
    id:
        Source identifier.
    tiles_url:
        URL template with {z}, {x}, {y} placeholders.
    """

    tiles_url: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "type": "vector",
                "tiles": [self.tiles_url],
            }
        )
        return base
