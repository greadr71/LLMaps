from llmaps.expressions import (
    feature_state_fade_color,
    feature_state_fade_mix,
    feature_state_fade_value,
)


def test_feature_state_fade_mix_defaults():
    expr = feature_state_fade_mix()

    assert expr == [
        "coalesce",
        ["feature-state", "fade_mix"],
        ["case", ["==", ["feature-state", "active"], True], 1, 0],
    ]


def test_feature_state_fade_value_with_custom_keys():
    expr = feature_state_fade_value(
        active=0.9,
        inactive=0.1,
        state_key="is_on",
        fade_mix_key="mix",
    )

    assert expr == [
        "interpolate",
        ["linear"],
        [
            "coalesce",
            ["feature-state", "mix"],
            ["case", ["==", ["feature-state", "is_on"], True], 1, 0],
        ],
        0,
        0.1,
        1,
        0.9,
    ]


def test_feature_state_fade_color_structure():
    stops = [(0, "#004d33"), (24, "#FFCC00"), (72, "#CC0000")]
    expr = feature_state_fade_color("delivery_hours", stops, inactive="#f0f0f0")

    assert expr[0:3] == [
        "interpolate",
        ["linear"],
        [
            "coalesce",
            ["feature-state", "fade_mix"],
            ["case", ["==", ["feature-state", "active"], True], 1, 0],
        ],
    ]
    assert expr[3] == 0
    assert expr[4] == "#f0f0f0"
    assert expr[5] == 1
    assert expr[6][0:3] == ["interpolate", ["linear"], ["feature-state", "delivery_hours"]]
    assert expr[6][3:] == [0, "#004d33", 24, "#FFCC00", 72, "#CC0000"]
