"""Base classes and protocols for data sources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class BaseSource:
    """Abstract data source used by layers.

    Concrete implementations are responsible for loading the underlying
    data and exposing a serialisable configuration that can be consumed
    by the front-end.
    """

    id: str

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable source configuration."""

        return {"id": self.id, "type": "base"}

