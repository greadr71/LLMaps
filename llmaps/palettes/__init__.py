"""Embedded geoscience color palettes for llmaps."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any, Dict, List, Optional

DEFAULT_PALETTE_ID = "arctic-chill"


@lru_cache(maxsize=1)
def _load_palettes() -> List[Dict[str, Any]]:
    data_path = resources.files("llmaps.palettes").joinpath("data/palettes.json")
    with data_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def _palette_index() -> Dict[str, Dict[str, Any]]:
    return {palette["id"]: palette for palette in _load_palettes()}


def get_palette(palette_id: str) -> Dict[str, Any]:
    """Return palette metadata by id."""
    palette = _palette_index().get(palette_id)
    if palette is None:
        available = ", ".join(sorted(_palette_index().keys()))
        raise ValueError(f"Unknown palette '{palette_id}'. Available palettes: {available}")
    return palette


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    value = color.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Invalid hex color '{color}'")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def get_palette_colors(palette_id: str, n: Optional[int] = None) -> List[str]:
    """Return palette colors, optionally resampled to exactly *n* colors."""
    colors = list(get_palette(palette_id)["colors"])
    if n is None or n == len(colors):
        return colors
    if n <= 0:
        raise ValueError("n must be > 0")
    if n == 1:
        return [colors[0]]

    rgb_colors = [_hex_to_rgb(color) for color in colors]
    src_last = len(rgb_colors) - 1
    dst_last = n - 1

    resampled: List[str] = []
    for idx in range(n):
        pos = idx * src_last / dst_last
        left = int(pos)
        right = min(left + 1, src_last)
        t = pos - left

        if left == right:
            rgb = rgb_colors[left]
        else:
            rgb = tuple(
                int(round(rgb_colors[left][channel] * (1.0 - t) + rgb_colors[right][channel] * t))
                for channel in range(3)
            )

        resampled.append(_rgb_to_hex(rgb))

    return resampled


def list_palettes(
    type: Optional[str] = None,
    variable: Optional[str] = None,
    blindsafe: Optional[bool] = None,
    perceptually_uniform: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """List available palettes with optional metadata filters."""
    palettes = _load_palettes()
    result: List[Dict[str, Any]] = []

    variable_lower = variable.lower() if variable else None

    for palette in palettes:
        if type is not None and palette.get("type") != type:
            continue
        if blindsafe is not None and palette.get("blindsafe") is not blindsafe:
            continue
        if (
            perceptually_uniform is not None
            and palette.get("perceptually_uniform") is not perceptually_uniform
        ):
            continue
        if variable_lower is not None:
            variable_text = (palette.get("variable") or "").lower()
            also_useful = [str(item).lower() for item in palette.get("also_useful", [])]
            if variable_lower not in variable_text and not any(
                variable_lower in candidate for candidate in also_useful
            ):
                continue

        result.append(palette)

    return result


__all__ = [
    "DEFAULT_PALETTE_ID",
    "get_palette",
    "get_palette_colors",
    "list_palettes",
]
