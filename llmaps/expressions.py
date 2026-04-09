"""Helpers for building MapLibre GL expressions.

Provides convenience functions for constructing feature-state based
expressions used with setFeatureState / promoteId, and utilities for
computing color stops from data distributions.
"""

from __future__ import annotations

from typing import Any, List, Optional, Sequence, Tuple, Union

from .palettes import DEFAULT_PALETTE_ID, get_palette_colors

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


def feature_state_fade_mix(
    state_key: str = "active",
    fade_mix_key: str = "fade_mix",
) -> List[Any]:
    """Build a robust fade-mix expression with fallback to boolean state.

    Returns a 0..1 numeric expression suitable for interpolation in paint
    properties. When ``fade_mix_key`` is absent, falls back to ``state_key``
    semantics (``True -> 1``, otherwise ``0``).
    """
    return [
        "coalesce",
        ["feature-state", fade_mix_key],
        ["case", ["==", ["feature-state", state_key], True], 1, 0],
    ]


def feature_state_fade_value(
    active: Union[int, float] = 0.7,
    inactive: Union[int, float] = 0.2,
    *,
    state_key: str = "active",
    fade_mix_key: str = "fade_mix",
) -> List[Any]:
    """Build an interpolated numeric expression by fade mix.

    Useful for smooth ``fill-opacity`` (and other numeric paint values) where
    state changes should be animated via ``fade_mix``.
    """
    return [
        "interpolate",
        ["linear"],
        feature_state_fade_mix(state_key=state_key, fade_mix_key=fade_mix_key),
        0,
        inactive,
        1,
        active,
    ]


def feature_state_fade_color(
    color_ramp_key: str,
    color_stops: Sequence[ColorStop],
    inactive: str = "#F0F0F0",
    *,
    state_key: str = "active",
    fade_mix_key: str = "fade_mix",
) -> List[Any]:
    """Build an interpolated color expression by fade mix.

    At ``fade_mix=0`` color is ``inactive``. At ``fade_mix=1`` color is taken
    from the ``color_ramp_key`` interpolation built from ``color_stops``.
    """
    ramp: List[Any] = [
        "interpolate",
        ["linear"],
        ["feature-state", color_ramp_key],
    ]
    for value, color in color_stops:
        ramp.extend([value, color])

    return [
        "interpolate",
        ["linear"],
        feature_state_fade_mix(state_key=state_key, fade_mix_key=fade_mix_key),
        0,
        inactive,
        1,
        ramp,
    ]


def _jenks_breaks(arr: Any, n_stops: int) -> List[float]:
    """Compute Jenks natural breaks thresholds."""
    try:
        import jenkspy
    except ImportError:
        raise ImportError(
            "jenkspy is required for method='jenks'. "
            "Install it with: pip install jenkspy"
        ) from None

    breaks = jenkspy.jenks_breaks(arr.tolist(), n_classes=n_stops - 1)
    # jenkspy returns n_classes+1 boundaries (including min and max)
    return [float(b) for b in breaks]


def compute_color_stops(
    values: Any,
    n_stops: int = 5,
    colors: Optional[Sequence[str]] = None,
    palette: Optional[str] = None,
    percentiles: Optional[Sequence[float]] = None,
    precision: int = 1,
    method: str = "quantile",
) -> List[ColorStop]:
    """Compute color stops from a numeric data distribution.

    Divides the data into thresholds using the chosen classification
    *method* and pairs each threshold with a color.  The result can be
    passed directly to :func:`feature_state_color` or used in a MapLibre
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
        CSS color strings for each stop.  Cannot be combined with *palette*.
        Highest-priority color source.
    palette:
        Embedded geoscience palette id from :mod:`llmaps.palettes`.
        Used when *colors* is not provided.
    percentiles:
        Explicit percentile values (0-100).  Only used with
        ``method="quantile"`` (the default).
    precision:
        Number of decimal places for threshold values.
    method:
        Classification method: ``"quantile"`` (default), ``"jenks"``
        (natural breaks, requires *jenkspy*), or ``"equal_interval"``.

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
    >>> # Uses default geoscience palette
    >>> stops = compute_color_stops([0, 50, 200, 500], method="jenks", palette="bathymetry")
    """
    import numpy as np

    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]

    if len(arr) == 0:
        return []

    # --- resolve n_stops from explicit percentiles (quantile only) ---
    if percentiles is not None:
        percentiles = list(percentiles)
        n_stops = len(percentiles)

    # --- resolve colors ---
    if colors is not None and palette is not None:
        raise ValueError("Provide either 'colors' or 'palette', not both")

    if colors is None:
        palette_id = palette or DEFAULT_PALETTE_ID
        colors = get_palette_colors(palette_id, n=n_stops)

    if len(colors) != n_stops:
        raise ValueError(
            f"Number of colors ({len(colors)}) must match n_stops ({n_stops})"
        )

    # --- compute thresholds ---
    if method == "quantile":
        if percentiles is None:
            percentiles = [i * 100 / (n_stops - 1) for i in range(n_stops)]
        thresholds = [round(float(np.percentile(arr, p)), precision) for p in percentiles]
    elif method == "jenks":
        thresholds = [round(v, precision) for v in _jenks_breaks(arr, n_stops)]
    elif method == "equal_interval":
        thresholds = [
            round(float(v), precision)
            for v in np.linspace(float(arr.min()), float(arr.max()), n_stops)
        ]
    else:
        raise ValueError(
            f"Unknown method {method!r}. Use 'quantile', 'jenks', or 'equal_interval'."
        )

    return list(zip(thresholds, colors))
