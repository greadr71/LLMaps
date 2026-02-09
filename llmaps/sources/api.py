"""ApiSource implementation for HTTP-based GeoJSON data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base import BaseSource


@dataclass
class ApiSource(BaseSource):
    """Data source that loads GeoJSON from an HTTP endpoint.

    No server-side fetch at config time; the frontend loads the URL
    when initialising the map. Use for live or remote datasets.

    Parameters
    ----------
    id:
        Source identifier used by layers.
    url:
        Full URL that returns GeoJSON (FeatureCollection, Feature, or list of features).
    headers:
        Optional HTTP headers (e.g. Authorization).
    params:
        Optional query parameters appended to the URL.
    """

    url: str
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "type": "api",
                "url": self.url,
                "headers": self.headers or {},
                "params": self.params or {},
            }
        )
        return base
