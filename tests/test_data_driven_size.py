"""Tests for DataDrivenSize and localized legend tips."""

import json

import numpy as np
import pytest

from llmaps import Map
from llmaps.components import DataDrivenSize, Legend
from llmaps.components.data_driven_size import _percentile_sorted, color_at_value
from llmaps.core.legend_generator import _default_tips_title, generate_legend_html
from llmaps.layers import CircleLayer
from llmaps.sources.file import FileSource


def test_percentile_sorted_edges():
    arr = np.array([1.0, 2.0, 3.0, 4.0, 100.0], dtype=float)
    assert _percentile_sorted(arr, 0.0) == 1.0
    assert _percentile_sorted(arr, 1.0) == 100.0
    mid = _percentile_sorted(arr, 0.5)
    assert 2.0 <= mid <= 4.0


def test_data_driven_size_resolve_expression():
    dds = DataDrivenSize(
        field="pop",
        size_range=(4.0, 22.0),
        auto_percentiles=(0.1, 0.5, 0.9),
        value_format="raw",
        legend_visual="fill",
        legend_color="#3366cc",
        legend_title="Population",
        locale="en-US",
    )
    values = np.array([100, 200, 500, 800, 1000, 5000, 8000], dtype=float)
    out = dds.resolve(values)
    assert out is not None
    expr = out["interpolate_expression"]
    assert expr[0] == "interpolate"
    assert expr[1] == ["linear"]
    assert expr[2] == ["to-number", ["get", "pop"], 0]
    assert len(expr) == 9  # interpolate + linear + input + 3 (value, size) pairs
    leg = out["legend_spec"]
    assert leg["visual"] == "fill"
    assert leg["title"] == "Population"
    assert len(leg["circles"]) == 3


def test_data_driven_size_mln_rub_locale():
    dds = DataDrivenSize(
        field="sales",
        size_range=(0.4, 1.2),
        value_format="mln_rub",
        legend_visual="stroke",
        legend_color="#111827",
        locale="ru-RU",
    )
    out = dds.resolve(np.array([1e6, 2e6, 5e6, 8e6], dtype=float))
    assert out is not None
    labels = [c["label"] for c in out["legend_spec"]["circles"]]
    assert all(isinstance(l, str) for l in labels)


def test_default_tips_title_locale():
    assert "Tips" in _default_tips_title("en-US")
    assert "Подсказки" in _default_tips_title("ru-RU")


def test_legend_html_tips_title_from_locale():
    config = {
        "locale": "ru-RU",
        "title": "T",
        "layers": [],
        "components": [
            {
                "type": "legend",
                "layer_labels": {},
                "instructions": ["one"],
            }
        ],
    }
    html = generate_legend_html(config)
    assert "💡 Подсказки" in html
    assert "💡 Tips" not in html


def test_legend_tips_title_override():
    config = {
        "locale": "en-US",
        "layers": [],
        "components": [
            {
                "type": "legend",
                "layer_labels": {},
                "tips_title": "💡 Hints",
                "instructions": ["a"],
            }
        ],
    }
    html = generate_legend_html(config)
    assert "💡 Hints" in html


def test_map_to_dict_resolves_circle_data_driven_size(tmp_path):
    gj = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"v": float(i * 100)}, "geometry": {"type": "Point", "coordinates": [0, 0]}}
            for i in range(1, 15)
        ],
    }
    p = tmp_path / "t.geojson"
    p.write_text(json.dumps(gj), encoding="utf-8")
    src = FileSource(id="s", path=str(p))
    layer = CircleLayer(
        id="c",
        source=src,
        color="#000",
        data_driven_size=DataDrivenSize(field="v", size_range=(4.0, 20.0), locale="en-US"),
    )
    m = Map(center=[0, 0], zoom=2, embedded=False)
    m.add_layer(layer)
    m.add_component(Legend(layer_labels={"c": "C"}))
    cfg = m.to_dict()
    layer_cfg = next(L for L in cfg["layers"] if L["id"] == "c")
    rad = layer_cfg["paint"]["circle-radius"]
    assert isinstance(rad, list) and rad[0] == "interpolate"
    assert "llmaps_size_legend" in layer_cfg["metadata"]


def test_color_stops_interpolate_and_legend_fills():
    dds = DataDrivenSize(
        field="v",
        size_range=(4.0, 20.0),
        value_format="raw",
        color_stops=[(0, "#ff0000"), (500, "#00ff00"), (1000, "#0000ff")],
        color_mode="interpolate",
    )
    out = dds.resolve(np.array([10, 50, 100, 200, 400, 800], dtype=float))
    assert out is not None
    assert "color_expression" in out
    assert out["color_expression"][0] == "interpolate"
    assert out["color_expression"][2] == ["to-number", ["get", "v"], 0]
    circles = out["legend_spec"]["circles"]
    assert all("fill" in c for c in circles)
    assert len({c["fill"] for c in circles}) == 3


def test_color_mode_step_expression():
    dds = DataDrivenSize(
        field="v",
        size_range=(4.0, 20.0),
        value_format="raw",
        color_stops=[(100, "#aaaaaa"), (500, "#bbbbbb"), (900, "#cccccc")],
        color_mode="step",
        color_step_below="#000000",
    )
    out = dds.resolve(np.array([50, 150, 600, 950], dtype=float))
    assert out is not None
    ce = out["color_expression"]
    assert ce[0] == "step"
    assert ce[1] == ["to-number", ["get", "v"], 0]
    assert ce[2] == "#000000"
    assert ce[3] == 100 and ce[4] == "#aaaaaa"


def test_legend_circle_colors_without_color_stops():
    dds = DataDrivenSize(
        field="v",
        size_range=(4.0, 12.0),
        value_format="raw",
        legend_circle_colors=("#111111", "#222222", "#333333"),
    )
    out = dds.resolve(np.array([1.0, 5.0, 9.0], dtype=float))
    assert out is not None
    assert "color_expression" not in out
    fills = [c["fill"] for c in out["legend_spec"]["circles"]]
    assert fills == ["#111111", "#222222", "#333333"]


def test_map_to_dict_sets_circle_color_from_color_stops(tmp_path):
    gj = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"v": float(i * 50)}, "geometry": {"type": "Point", "coordinates": [0, 0]}}
            for i in range(1, 20)
        ],
    }
    p = tmp_path / "c.geojson"
    p.write_text(json.dumps(gj), encoding="utf-8")
    src = FileSource(id="s", path=str(p))
    dds = DataDrivenSize(
        field="v",
        size_range=(4.0, 18.0),
        color_stops=[(0, "#fde047"), (500, "#22c55e"), (1000, "#15803d")],
    )
    layer = CircleLayer(id="c", source=src, color="#999999", data_driven_size=dds)
    m = Map(center=[0, 0], zoom=2, embedded=False)
    m.add_layer(layer)
    m.add_component(Legend(layer_labels={"c": "C"}))
    cfg = m.to_dict()
    layer_cfg = next(L for L in cfg["layers"] if L["id"] == "c")
    assert layer_cfg["paint"]["circle-color"][0] == "interpolate"
    assert layer_cfg["paint"]["circle-radius"][0] == "interpolate"


def test_color_at_value_midpoint():
    assert color_at_value([(0, "#000000"), (100, "#ffffff")], 50) == "#808080"


def test_normalize_hex_invalid():
    dds = DataDrivenSize(field="v", size_range=(4.0, 10.0), color_stops=[(0, "not-a-color"), (10, "#fff")])
    with pytest.raises(ValueError):
        dds.resolve(np.array([1.0, 5.0, 9.0], dtype=float))
