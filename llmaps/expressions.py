"""Helpers for building MapLibre GL expressions.

Provides convenience functions for constructing feature-state based
expressions used with setFeatureState / promoteId, and utilities for
computing color stops from data distributions.
"""

from __future__ import annotations

from typing import Any, List, Optional, Sequence, Tuple, Union

# Color stop: (threshold_value, css_color)
ColorStop = Tuple[Union[int, float], str]

# Default 5-class diverging palette: green → yellow → red
_DEFAULT_COLORS = ["#004d33", "#00AA44", "#FFCC00", "#FF6600", "#CC0000"]


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


def compute_color_stops(
    values: Any,
    n_stops: int = 5,
    colors: Optional[Sequence[str]] = None,
    percentiles: Optional[Sequence[float]] = None,
    precision: int = 1,
) -> List[ColorStop]:
    """Compute color stops from a numeric data distribution.

    Divides the data into quantile-based thresholds and pairs each
    threshold with a color from the palette.  The result can be passed
    directly to :func:`feature_state_color` or used in a MapLibre
    ``interpolate`` expression.

    Parameters
    ----------
    values:
        Numeric array-like (pandas Series, numpy array, or plain list).
        NaN / None values are dropped automatically.
    n_stops:
        Number of color stops to generate.  Ignored when *percentiles*
        is provided explicitly.
    colors:
        CSS color strings for each stop.  Defaults to a green-yellow-red
        diverging palette.  Length must match *n_stops* (or *percentiles*).
    percentiles:
        Explicit percentile values (0-100) to use as thresholds.
        When omitted, evenly-spaced percentiles are computed from
        *n_stops* (e.g. 5 stops → [0, 25, 50, 75, 100]).
    precision:
        Number of decimal places for threshold values.

    Returns
    -------
    list[ColorStop]
        List of ``(value, color)`` tuples suitable for ``color_stops``
        parameters throughout llmaps.

    Example
    -------
    >>> import pandas as pd
    >>> from llmaps.expressions import compute_color_stops
    >>> stops = compute_color_stops(pd.Series([1, 5, 10, 20, 50]))
    >>> # [(1.0, '#004d33'), (5.0, '#00AA44'), (10.0, '#FFCC00'), ...]
    """
    import numpy as np

    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]

    if len(arr) == 0:
        return []

    if percentiles is None:
        percentiles = [i * 100 / (n_stops - 1) for i in range(n_stops)]
    else:
        percentiles = list(percentiles)
        n_stops = len(percentiles)

    if colors is None:
        if n_stops <= len(_DEFAULT_COLORS):
            colors = _DEFAULT_COLORS[:n_stops]
        else:
            # Fall back to evenly spaced selection from the default palette
            colors = [
                _DEFAULT_COLORS[int(i * (len(_DEFAULT_COLORS) - 1) / (n_stops - 1))]
                for i in range(n_stops)
            ]

    if len(colors) != n_stops:
        raise ValueError(
            f"Number of colors ({len(colors)}) must match n_stops ({n_stops})"
        )

    thresholds = [round(float(np.percentile(arr, p)), precision) for p in percentiles]

    return list(zip(thresholds, colors))
