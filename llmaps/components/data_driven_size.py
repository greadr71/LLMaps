"""Data-driven marker size (circle radius or symbol icon-size) from a numeric field.

Optional **color** ramp on the same or another numeric field: MapLibre ``interpolate``
or ``step`` for ``circle-color``, plus per-circle fills in the server-rendered size legend.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Optional, Sequence, Tuple, Union

import numpy as np

ValueFormat = Union[str, Callable[[float], str]]
LegendVisual = Literal["fill", "stroke"]
ColorMode = Literal["interpolate", "step"]


def _percentile_sorted(sorted_arr: np.ndarray, p: float) -> float:
    """Linear interpolation between closest ranks (same idea as Atlas JS)."""
    n = sorted_arr.size
    if n == 0:
        return float("nan")
    if n == 1:
        return float(sorted_arr[0])
    idx = (n - 1) * p
    lo = int(np.floor(idx))
    hi = int(np.ceil(idx))
    if lo == hi:
        return float(sorted_arr[lo])
    t = idx - lo
    return float(sorted_arr[lo] * (1.0 - t) + sorted_arr[hi] * t)


def _format_value(n: float, value_format: ValueFormat, locale: str) -> str:
    if callable(value_format):
        return str(value_format(n))

    vf = str(value_format).lower()
    is_ru = locale.lower().startswith("ru")

    if vf == "raw":
        if abs(n - round(n)) < 1e-6:
            return str(int(round(n)))
        return f"{n:.4g}"

    if vf in ("thousands", "grouped"):
        rounded = int(round(n))
        if is_ru:
            s = f"{rounded:,}".replace(",", "\u00a0")
            return s
        return f"{rounded:,}"

    if vf == "mln_rub":
        m = n / 1_000_000.0
        if is_ru:
            return f"{m:.1f}".replace(".", ",") + " млн\u00a0₽"
        return f"{m:.1f}M\u00a0RUB"

    if abs(n - round(n)) < 1e-6:
        return str(int(round(n)))
    return f"{n:.4g}"


def _build_interpolate_expression(field: str, v0: float, v1: float, v2: float, s0: float, s1: float, s2: float) -> List[Any]:
    return [
        "interpolate",
        ["linear"],
        ["to-number", ["get", field], 0],
        v0,
        s0,
        v1,
        s1,
        v2,
        s2,
    ]


_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def _normalize_hex_color(color: str) -> str:
    """Return ``#RRGGBB`` for a CSS hex string (3- or 6-digit, optional leading ``#``)."""
    s = str(color).strip()
    if not s:
        raise ValueError("empty color")
    if not _HEX_RE.match(s):
        raise ValueError(f"expected #RRGGBB hex color, got {color!r}")
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)
    return f"#{s.lower()}"


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = _normalize_hex_color(hex_color).lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    r = max(0, min(255, int(round(r))))
    g = max(0, min(255, int(round(g))))
    b = max(0, min(255, int(round(b))))
    return f"#{r:02x}{g:02x}{b:02x}"


def _lerp_rgb(a: Tuple[int, int, int], b: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    t = max(0.0, min(1.0, float(t)))
    return (
        a[0] + t * (b[0] - a[0]),
        a[1] + t * (b[1] - a[1]),
        a[2] + t * (b[2] - a[2]),
    )


def color_at_value(
    stops: Sequence[Tuple[float, str]], x: float, *, clamp: bool = True
) -> str:
    """Linear RGB interpolation along ``stops`` (sorted by value).

    Parameters
    ----------
    stops:
        ``(value, #hex)`` pairs. At least two pairs.
    x:
        Domain position.
    clamp:
        If True, values below/above the stop range use the edge colors.
    """
    ordered = sorted((float(v), _normalize_hex_color(c)) for v, c in stops)
    if len(ordered) < 2:
        raise ValueError("color_at_value needs at least two color stops")

    xs = [p[0] for p in ordered]
    if clamp:
        if x <= xs[0]:
            return ordered[0][1]
        if x >= xs[-1]:
            return ordered[-1][1]

    for i in range(len(ordered) - 1):
        x0, x1 = xs[i], xs[i + 1]
        if x0 <= x <= x1:
            c0, c1 = _hex_to_rgb(ordered[i][1]), _hex_to_rgb(ordered[i + 1][1])
            if x1 == x0:
                return ordered[i][1]
            t = (x - x0) / (x1 - x0)
            rgb = _lerp_rgb(c0, c1, t)
            return _rgb_to_hex(*rgb)

    if not clamp and x < xs[0]:
        c0, c1 = _hex_to_rgb(ordered[0][1]), _hex_to_rgb(ordered[1][1])
        if xs[1] == xs[0]:
            return ordered[0][1]
        t = (x - xs[0]) / (xs[1] - xs[0])
        return _rgb_to_hex(*_lerp_rgb(c0, c1, t))
    if not clamp and x > xs[-1]:
        c0, c1 = _hex_to_rgb(ordered[-2][1]), _hex_to_rgb(ordered[-1][1])
        if xs[-1] == xs[-2]:
            return ordered[-1][1]
        t = (x - xs[-2]) / (xs[-1] - xs[-2])
        return _rgb_to_hex(*_lerp_rgb(c0, c1, t))
    return ordered[-1][1]


def _build_color_interpolate_expression(field: str, stops: Sequence[Tuple[float, str]]) -> List[Any]:
    ordered = sorted((float(v), _normalize_hex_color(c)) for v, c in stops)
    if len(ordered) < 2:
        raise ValueError("color_stops must contain at least two (value, color) pairs")
    out: List[Any] = ["interpolate", ["linear"], ["to-number", ["get", field], 0]]
    for v, c in ordered:
        out.extend([v, c])
    return out


def _build_color_step_expression(
    field: str,
    stops: Sequence[Tuple[float, str]],
    default_color: str,
) -> List[Any]:
    """MapLibre ``step``: ``input < first_stop → default``, then each interval."""
    ordered = sorted((float(v), _normalize_hex_color(c)) for v, c in stops)
    if not ordered:
        raise ValueError("color_stops must not be empty for step mode")
    out: List[Any] = [
        "step",
        ["to-number", ["get", field], 0],
        _normalize_hex_color(default_color),
    ]
    for v, c in ordered:
        out.extend([v, c])
    return out


def _size_legend_spec(
    *,
    title: Optional[str],
    visual: LegendVisual,
    stroke_color: str,
    fill_color: str,
    v0: float,
    v1: float,
    v2: float,
    s0: float,
    s1: float,
    s2: float,
    label0: str,
    label1: str,
    label2: str,
    circle_fills: Optional[Tuple[str, str, str]] = None,
) -> Dict[str, Any]:
    """Legend payload consumed by :func:`llmaps.core.legend_generator.generate_legend_html`."""
    circles: List[Dict[str, Any]] = [
        {"value": v0, "size_px": float(s0), "label": label0},
        {"value": v1, "size_px": float(s1), "label": label1},
        {"value": v2, "size_px": float(s2), "label": label2},
    ]
    if circle_fills is not None:
        for d, fc in zip(circles, circle_fills):
            d["fill"] = _normalize_hex_color(fc)
    return {
        "title": title,
        "visual": visual,
        "stroke_color": stroke_color,
        "fill_color": fill_color,
        "circles": circles,
    }


def render_size_legend_svg_fragment(spec: Dict[str, Any]) -> str:
    """Build inline SVG HTML for one size legend (three concentric circles + labels)."""
    circles_cfg = spec.get("circles") or []
    if len(circles_cfg) != 3:
        return ""

    visual = spec.get("visual", "fill")
    stroke_c = html.escape(str(spec.get("stroke_color", "#374151")))
    default_fill = html.escape(str(spec.get("fill_color", "#64748b")))
    title = spec.get("title")
    title_html = ""
    if title:
        title_html = (
            f'<div class="llmaps-size-legend-title">{html.escape(str(title))}</div>'
        )

    # Largest radius first for drawing order (back to front)
    ordered = sorted(circles_cfg, key=lambda c: float(c["size_px"]), reverse=True)
    max_r = max(float(c["size_px"]) for c in ordered)
    pad = 6.0
    cx = max_r + pad
    base_y = max_r * 2.0 + pad
    x_label = cx + max_r + 48.0

    circles_svg: List[str] = []
    for c in ordered:
        r = float(c["size_px"])
        cy = base_y - r
        if visual == "stroke":
            circles_svg.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
                f'stroke="{stroke_c}" stroke-width="2"/>'
            )
        else:
            fill = html.escape(str(c.get("fill", default_fill)))
            circles_svg.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
                f'stroke="#ffffff" stroke-width="1.2"/>'
            )

    min_gap = 12.0
    y_labels: List[float] = []
    for c in ordered:
        r = float(c["size_px"])
        y_labels.append(base_y - 2.0 * r)
    for i in range(1, len(y_labels)):
        if y_labels[i] - y_labels[i - 1] < min_gap:
            y_labels[i] = y_labels[i - 1] + min_gap

    svg_h = max(base_y + pad, y_labels[-1] + 10.0)
    svg_w = x_label + 40.0

    lines_svg: List[str] = []
    texts_svg: List[str] = []
    for c, y in zip(ordered, y_labels):
        lab = html.escape(str(c.get("label", "")))
        lines_svg.append(
            f'<line x1="{cx:.1f}" y1="{y:.1f}" x2="{x_label - 6:.1f}" y2="{y:.1f}" '
            'stroke="#c7ccd6" stroke-width="1" stroke-dasharray="2,2"/>'
        )
        texts_svg.append(
            f'<text x="{x_label:.1f}" y="{y:.1f}" fill="#6b7280" font-size="10" '
            f'text-anchor="start" dominant-baseline="middle">{lab}</text>'
        )

    inner = "".join(circles_svg) + "".join(lines_svg) + "".join(texts_svg)
    svg = (
        f'<svg width="{svg_w:.0f}" height="{svg_h:.0f}" '
        f'class="llmaps-size-legend-svg" style="display:block;overflow:visible;">{inner}</svg>'
    )
    return f'{title_html}<div class="llmaps-size-legend-body" style="display:flex;justify-content:center;">{svg}</div>'


@dataclass
class DataDrivenSize:
    """Configure circle radius or symbol icon-size from a numeric feature field.

    Optional **color** styling for ``CircleLayer`` via ``color_stops`` (linear
    interpolation or ``step``). Legend circles use per-value colors from
    ``legend_circle_colors`` or by sampling ``color_stops`` at the three size
    stops.

    Resolved at :meth:`llmaps.map.Map.to_dict` time when the layer uses a
    :class:`llmaps.sources.file.FileSource` so percentiles can be read from
    local data.

    Parameters
    ----------
    field:
        GeoJSON property for size: ``["get", field]``.
    size_range, auto_percentiles, min_value, max_value, value_format:
        See :meth:`resolve`.
    legend_visual, legend_color, legend_title, locale:
        Legend appearance for single-color mode; ``legend_color`` is also the
        stroke color when ``legend_visual="stroke"``.
    color_stops:
        Optional ``(value, "#hex")`` pairs for ``circle-color``. When
        ``color_mode="interpolate"`` (default), builds a linear ``interpolate``
        paint expression (piecewise-linear between any number of stops). When
        ``color_mode="step"``, builds a ``step`` expression; use
        ``color_step_below`` for the output when the value is below the first
        threshold.
    color_mode:
        ``"interpolate"`` or ``"step"`` (MapLibre ``step``).
    color_field:
        Property name for color expressions; defaults to ``field`` (same as size).
    color_step_below:
        Default color for ``step`` when the value is strictly below the first
        stop value. Defaults to ``"#e5e7eb"`` if unset.
    legend_circle_colors:
        Optional ``(low, mid, high)`` hex colors aligned with the sorted three
        size stops. Overrides automatic colors from ``color_stops`` in the SVG
        legend only; map paint still follows ``color_stops`` when that is set.
    """

    field: str
    size_range: Tuple[float, float] = (4.0, 22.0)
    auto_percentiles: Tuple[float, float, float] = (0.1, 0.5, 0.9)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    value_format: ValueFormat = "thousands"
    legend_visual: LegendVisual = "fill"
    legend_color: str = "#64748b"
    legend_title: Optional[str] = None
    locale: str = "en-US"
    color_stops: Optional[Sequence[Tuple[float, str]]] = None
    color_mode: ColorMode = "interpolate"
    color_field: Optional[str] = None
    color_step_below: Optional[str] = None
    legend_circle_colors: Optional[Tuple[str, str, str]] = None

    def resolve(
        self, values: Sequence[float], *, locale: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Compute paint expressions and legend spec from numeric samples.

        Returns
        -------
        dict or None
            Keys: ``interpolate_expression``, ``legend_spec``, and optionally
            ``color_expression`` (list) when ``color_stops`` is set.
        """
        loc = locale if locale is not None else self.locale
        arr = np.asarray(values, dtype=float)
        arr = arr[np.isfinite(arr)]
        if arr.size == 0:
            return None
        arr.sort()

        p0, p1, p2 = self.auto_percentiles
        pv0 = _percentile_sorted(arr, p0)
        pv1 = _percentile_sorted(arr, p1)
        pv2 = _percentile_sorted(arr, p2)

        v0 = float(self.min_value) if self.min_value is not None else float(pv0)
        v2 = float(self.max_value) if self.max_value is not None else float(pv2)
        v1 = float(pv1)
        v0, v1, v2 = sorted((v0, v1, v2))
        if not (v2 > v0):
            return None

        lo, hi = float(self.size_range[0]), float(self.size_range[1])
        t1 = 0.0 if (v2 - v0) == 0 else (v1 - v0) / (v2 - v0)
        s0, s2 = lo, hi
        s1 = s0 + t1 * (s2 - s0)

        expr = _build_interpolate_expression(self.field, v0, v1, v2, s0, s1, s2)
        lab0 = _format_value(v0, self.value_format, loc)
        lab1 = _format_value(v1, self.value_format, loc)
        lab2 = _format_value(v2, self.value_format, loc)

        if self.legend_visual == "stroke":
            stroke_c = self.legend_color
            fill_fallback = "#94a3b8"
        else:
            stroke_c = "#374151"
            fill_fallback = self.legend_color

        circle_fills: Optional[Tuple[str, str, str]] = None
        color_expression: Optional[List[Any]] = None
        cfield = self.color_field or self.field

        if self.color_stops is not None and len(self.color_stops) > 0:
            stops = list(self.color_stops)
            if self.color_mode == "interpolate":
                if len(stops) < 2:
                    raise ValueError("color_stops must have at least two pairs when color_mode='interpolate'")
                color_expression = _build_color_interpolate_expression(cfield, stops)
            else:
                if not stops:
                    raise ValueError("color_stops must not be empty when color_mode='step'")
                below = self.color_step_below or "#e5e7eb"
                color_expression = _build_color_step_expression(cfield, stops, below)

            if self.legend_circle_colors is not None:
                if len(self.legend_circle_colors) != 3:
                    raise ValueError("legend_circle_colors must be a triple (low, mid, high)")
                circle_fills = tuple(_normalize_hex_color(x) for x in self.legend_circle_colors)
            else:
                circle_fills = (
                    color_at_value(stops, v0),
                    color_at_value(stops, v1),
                    color_at_value(stops, v2),
                )
        elif self.legend_circle_colors is not None:
            if len(self.legend_circle_colors) != 3:
                raise ValueError("legend_circle_colors must be a triple (low, mid, high)")
            circle_fills = tuple(_normalize_hex_color(x) for x in self.legend_circle_colors)

        legend = _size_legend_spec(
            title=self.legend_title,
            visual=self.legend_visual,
            stroke_color=stroke_c,
            fill_color=fill_fallback,
            v0=v0,
            v1=v1,
            v2=v2,
            s0=s0,
            s1=s1,
            s2=s2,
            label0=lab0,
            label1=lab1,
            label2=lab2,
            circle_fills=circle_fills,
        )
        out: Dict[str, Any] = {"interpolate_expression": expr, "legend_spec": legend}
        if color_expression is not None:
            out["color_expression"] = color_expression
        return out
