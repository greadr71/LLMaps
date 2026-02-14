"""FeatureSearch component for LLMaps — search within map data attributes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Mapping, Optional

from .base import BaseComponent

Position = Literal["top-left", "top-right", "top-center"]


@dataclass
class FeatureSearch(BaseComponent):
    """Search across GeoJSON feature attributes (not a geocoder).

    Unlike :class:`Search` which queries an external geocoder API,
    ``FeatureSearch`` searches within the data already loaded on the
    map.  It provides a dropdown with matching features and flies to
    the selected one.

    Parameters
    ----------
    position:
        Where to place the search bar on the map.
    placeholder:
        Placeholder text for the search input.
    search_fields:
        Mapping from **source id** to list of attribute names to
        search in.  For example::

            {"warehouses": ["id", "name", "city"],
             "regions": ["name_ru"]}

    field_labels:
        Optional mapping from attribute name to display label used in
        dropdown results.
    max_results:
        Maximum number of results shown in the dropdown.
    zoom_on_select:
        Zoom level to fly to when a result is selected.
    debounce_ms:
        Debounce delay in milliseconds before searching.
    min_chars:
        Minimum characters before triggering search.
    """

    position: Position = "top-center"
    placeholder: str = "Search..."
    search_fields: Mapping[str, List[str]] = field(default_factory=dict)
    field_labels: Mapping[str, str] = field(default_factory=dict)
    max_results: int = 15
    zoom_on_select: float = 8
    debounce_ms: int = 200
    min_chars: int = 2

    def __post_init__(self) -> None:
        self.component_type = "feature_search"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "position": self.position,
                "placeholder": self.placeholder,
                "search_fields": {k: list(v) for k, v in self.search_fields.items()},
                "field_labels": dict(self.field_labels),
                "max_results": self.max_results,
                "zoom_on_select": self.zoom_on_select,
                "debounce_ms": self.debounce_ms,
                "min_chars": self.min_chars,
            }
        )
        return base
