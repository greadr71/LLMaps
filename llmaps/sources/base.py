"""Base classes and protocols for data sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class BaseSource:
    """Abstract data source used by layers.

    Concrete implementations are responsible for loading the underlying
    data and exposing a serialisable configuration that can be consumed
    by the front-end.

    Parameters
    ----------
    id:
        Source identifier used by layers.
    promote_id:
        Feature property to use as the feature id (MapLibre promoteId).
        Required for setFeatureState / feature-state expressions.
        Keyword-only to avoid conflicts with positional args in subclasses.
    """

    id: str

    # keyword-only (after KW_ONLY sentinel) so subclasses with required
    # positional fields don't break dataclass inheritance rules.
    promote_id: Optional[str] = field(default=None, repr=False, kw_only=True)

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable source configuration."""

        d: Dict[str, Any] = {"id": self.id, "type": "base"}
        if self.promote_id is not None:
            d["promoteId"] = self.promote_id
        return d

