"""Base abstractions for UI components used by LLMaps."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class BaseComponent:
    """Common base for all UI components (legend, popup, controls, …)."""

    component_type: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.component_type}

