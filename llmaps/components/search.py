"""Search component with geocoder and optional autocomplete."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional

from .base import BaseComponent

Position = Literal["top-left", "top-right"]


@dataclass
class Search(BaseComponent):
    """Address search: geocoder URL, optional autocomplete, fly to result.

    Parameters
    ----------
    geocoder_url:
        URL of the geocoder API. If None, frontend may use env or show an error.
    geocoder_params:
        Extra query params (e.g. API key).
    placeholder:
        Input placeholder text.
    autocomplete:
        Request suggestions while typing (with debounce).
    position:
        Placement of the search box.
    zoom_on_result:
        Zoom level when flying to the result.
    """

    geocoder_url: Optional[str] = None
    geocoder_params: Optional[Dict[str, str]] = None
    placeholder: str = "Search address..."
    autocomplete: bool = True
    position: Position = "top-left"
    zoom_on_result: int = 15

    component_type: str = "search"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "geocoder_url": self.geocoder_url,
                "geocoder_params": self.geocoder_params or {},
                "placeholder": self.placeholder,
                "autocomplete": self.autocomplete,
                "position": self.position,
                "zoom_on_result": self.zoom_on_result,
            }
        )
        return base
