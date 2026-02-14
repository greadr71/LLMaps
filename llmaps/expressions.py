"""Helpers for building MapLibre GL expressions.

Provides convenience functions for constructing feature-state based
expressions used with setFeatureState / promoteId.
"""

from __future__ import annotations

from typing import Any, List, Sequence, Tuple, Union

# Color stop: (threshold_value, css_color)
ColorStop = Tuple[Union[int, float], str]


def feature_state_color(
    state_key: str,
    color_ramp_key: str,
    color_stops: Sequence[ColorStop],
    inactive: str = "#F0F0F0",
    default: str = "#E0E0E0",
) -> List[Any]:
    """Build a MapLibre expression that colors features by feature-state.

    When ``state_key`` is ``true``, the fill color interpolates linearly
    over ``color_ramp_key`` using ``color_stops``.  When ``state_key`` is
    ``false`` the feature gets ``inactive`` color.  Otherwise ``default``.

    Parameters
    ----------
    state_key:
        Boolean feature-state key (e.g. ``"active"``).
    color_ramp_key:
        Numeric feature-state key used for interpolation (e.g. ``"delivery_hours"``).
    color_stops:
        Sequence of ``(value, color)`` pairs for the color ramp.
    inactive:
        Color when ``state_key`` is ``false``.
    default:
        Fallback color when ``state_key`` is not set.

    Returns
    -------
    list
        A MapLibre ``case`` expression ready for ``fill-color`` or similar.
    """
    interpolate: List[Any] = [
        "interpolate",
        ["linear"],
        ["feature-state", color_ramp_key],
    ]
    for value, color in color_stops:
        interpolate.extend([value, color])

    return [
        "case",
        ["==", ["feature-state", state_key], True],
        interpolate,
        ["==", ["feature-state", state_key], False],
        inactive,
        default,
    ]


def feature_state_value(
    state_key: str,
    active: Union[int, float] = 0.7,
    inactive: Union[int, float] = 0.2,
    default: Union[int, float] = 0.6,
) -> List[Any]:
    """Build a MapLibre expression that returns a numeric value by feature-state.

    Useful for ``fill-opacity``, ``circle-radius``, etc.

    Parameters
    ----------
    state_key:
        Boolean feature-state key (e.g. ``"active"``).
    active:
        Value when ``state_key`` is ``true``.
    inactive:
        Value when ``state_key`` is ``false``.
    default:
        Fallback value when ``state_key`` is not set.

    Returns
    -------
    list
        A MapLibre ``case`` expression.
    """
    return [
        "case",
        ["==", ["feature-state", state_key], True],
        active,
        ["==", ["feature-state", state_key], False],
        inactive,
        default,
    ]
