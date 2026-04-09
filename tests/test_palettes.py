import pytest

from llmaps.expressions import compute_color_stops
from llmaps.palettes import DEFAULT_PALETTE_ID, get_palette_colors, list_palettes


def test_list_palettes_returns_many_entries():
    palettes = list_palettes()
    assert len(palettes) >= 50


def test_list_palettes_filters():
    palettes = list_palettes(type="sequential", blindsafe=True)
    assert palettes
    assert all(p["type"] == "sequential" for p in palettes)
    assert all(p["blindsafe"] is True for p in palettes)


def test_get_palette_colors_resamples():
    colors = get_palette_colors("rain-blues", n=5)
    assert len(colors) == 5
    assert all(color.startswith("#") and len(color) == 7 for color in colors)


def test_get_palette_colors_unknown_palette_raises():
    with pytest.raises(ValueError, match="Unknown palette"):
        get_palette_colors("nonexistent")


def test_compute_color_stops_with_palette():
    values = [1, 5, 10, 20, 50]
    stops = compute_color_stops(values, palette="rain-blues")
    assert len(stops) == 5
    assert all(isinstance(v, (int, float)) for v, _ in stops)
    assert all(c.startswith("#") and len(c) == 7 for _, c in stops)


def test_compute_color_stops_palette_and_colors_conflict():
    with pytest.raises(ValueError, match="either 'colors' or 'palette'"):
        compute_color_stops([1, 2, 3], palette="rain-blues", colors=["#FFFFFF", "#000000", "#FF0000"])


def test_compute_color_stops_default_palette_matches_module_default():
    values = [1, 5, 10, 20, 50]
    stops = compute_color_stops(values)
    expected = get_palette_colors(DEFAULT_PALETTE_ID, n=5)
    assert [color for _, color in stops] == expected


def test_compute_color_stops_rejects_removed_cmap_parameter():
    with pytest.raises(TypeError):
        compute_color_stops([1, 2, 3], cmap="viridis")
