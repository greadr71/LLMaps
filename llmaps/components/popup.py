"""Popup component for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Literal, Mapping, Optional

from .base import BaseComponent

Trigger = Literal["click", "hover", "both"]


@dataclass
class Popup(BaseComponent):
    """Feature detail popup configuration.

    Parameters
    ----------
    fields:
        List of attribute names to display in the popup.
    field_labels:
        Optional mapping from attribute name to human-readable label.
    template:
        Optional HTML template string. When omitted, a default table-like
        layout is used on the front-end.
    fields_by_layer:
        Optional per-layer override for ``fields``. Keys are layer ids and
        values are ordered lists of field names.
    trigger:
        Event that opens the popup: ``"click"`` (default), ``"hover"``,
        or ``"both"``.
        When ``"hover"``, the popup follows the cursor and disappears
        when the mouse leaves the feature. ``"both"`` enables hover preview
        and click-to-pin behavior in one component.
    """

    fields: List[str] = field(default_factory=list)
    field_labels: Mapping[str, str] = field(default_factory=dict)
    template: Optional[str] = None
    fields_by_layer: Mapping[str, List[str]] = field(default_factory=dict)
    trigger: Trigger = "click"

    def __post_init__(self) -> None:
        self.component_type = "popup"

    def to_dict(self) -> Dict[str, object]:
        base = super().to_dict()
        base.update(
            {
                "fields": list(self.fields),
                "field_labels": dict(self.field_labels),
                "template": self.template,
                "fields_by_layer": {k: list(v) for k, v in self.fields_by_layer.items()},
                "trigger": self.trigger,
            }
        )
        return base

