"""Build the gerrymandering scrollytelling story map.

Usage:
    cd llmaps/examples/gerrymandering
    python build_map.py
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Popup, Storytelling
from llmaps.layers import FillLayer
from llmaps.sources import FileSource

from grid_diagram import build_overlays_html
from scenes import (
    DEM_COLOR,
    PA_CENTER,
    PA_ZOOM,
    POPUP_FIELDS,
    REP_COLOR,
    build_popup_labels,
    build_scenes,
)
from texts import get_texts

# ── Paths ──
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SOURCE_2016 = DATA_DIR / "pa_gerrymandered_2016.geojson"
SOURCE_2018 = DATA_DIR / "pa_remedial_2018.geojson"
GOOFY_IMAGE = DATA_DIR / "goofy_kicks_donald.png"

# ── Styling ──
NO_DATA = "#c7c7c7"
COLOR_EXPR = ["match", ["get", "winner"], "D", DEM_COLOR, "R", REP_COLOR, NO_DATA]

HIGHLIGHT_COLOR = [
    "case",
    ["boolean", ["feature-state", "highlighted"], False],
    ["match", ["get", "winner"], "D", "#4393c3", "R", "#d6604d", "#e0e0e0"],
    COLOR_EXPR,
]
HIGHLIGHT_OPACITY = [
    "case",
    ["boolean", ["feature-state", "highlighted"], False],
    0.9,
    0.6,
]
HIGHLIGHT_STROKE = [
    "case",
    ["boolean", ["feature-state", "highlighted"], False],
    "#ffd700",
    "#ffffff",
]
HIGHLIGHT_STROKE_WIDTH = [
    "case",
    ["boolean", ["feature-state", "highlighted"], False],
    3.0,
    0.5,
]

# ── Goofy overlay bounds ──
GOOFY_OVERLAY_BOUNDS = [
    [-76.35, 40.34],
    [-74.99, 40.34],
    [-74.99, 39.74],
    [-76.35, 39.74],
]


def _encode_image_as_data_url(path: Path) -> str | None:
    if not path.exists():
        return None
    mime_type, _ = mimetypes.guess_type(path.name)
    content_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{content_type};base64,{encoded}"


def _map_locale(locale: str) -> str:
    return "ru-RU" if locale == "ru" else "en-US"


def _output_path(locale: str) -> Path:
    suffix = "en" if locale == "en" else "ru"
    return BASE_DIR / f"gerrymandering_{suffix}.html"


def build_map(locale: str = "en") -> Map:
    texts = get_texts(locale)
    scenes = build_scenes(locale)

    m = Map(
        center=PA_CENTER,
        zoom=PA_ZOOM,
        title=texts["map_title"],
        tiles="carto-light",
        locale=_map_locale(locale),
        embedded=True,
        use_compression=False,
    )

    # Sources
    source_2016 = FileSource(id="pa-2016", path=str(SOURCE_2016), promote_id="district")
    source_2018 = FileSource(id="pa-2018", path=str(SOURCE_2018), promote_id="district")

    # Layers
    layer_2016 = FillLayer(
        id="fill-2016",
        source=source_2016,
        fill_color=HIGHLIGHT_COLOR,
        fill_opacity=HIGHLIGHT_OPACITY,
        stroke_width=HIGHLIGHT_STROKE_WIDTH,
        stroke_color=HIGHLIGHT_STROKE,
        visible=True,
    )
    layer_2018 = FillLayer(
        id="fill-2018",
        source=source_2018,
        fill_color=HIGHLIGHT_COLOR,
        fill_opacity=HIGHLIGHT_OPACITY,
        stroke_width=HIGHLIGHT_STROKE_WIDTH,
        stroke_color=HIGHLIGHT_STROKE,
        visible=False,
    )

    m.add_layer(layer_2016)
    m.add_layer(layer_2018)

    # Popup
    m.add_component(
        Popup(
            fields_by_layer={
                "fill-2016": POPUP_FIELDS,
                "fill-2018": POPUP_FIELDS,
            },
            field_labels=build_popup_labels(locale),
            trigger="click",
        )
    )

    # Storytelling (upstream snap_mode + touch_swipe eliminate CSS override + touch patch)
    m.add_component(
        Storytelling(
            scenes=scenes,
            position="left",
            width=420,
            progress=True,
            snap_mode="mandatory",
            touch_swipe=False,
            comparison_slider_hint=texts["comparison_slider_hint"],
            comparison_slider_start_pct=0.03,
            use_swiper_cdn=True,
            expose_scene_bridge=True,
            prewarm_comparison=True,
            keep_main_layers_visible_in_comparison=True,
        )
    )

    m.add_component(Controls(zoom=True, scale=True))

    # ── Embed data for JS overlays ──
    scene_ids = [s.id for s in scenes]
    m.embed_data(
        "sceneConfig",
        {
            "introIdx": scene_ids.index("intro"),
            "toolsIdx": scene_ids.index("tools"),
            "paCtxIdx": scene_ids.index("pa_context"),
            "courtIdx": scene_ids.index("court"),
            "sceneIds": scene_ids,
        },
    )
    m.embed_data(
        "scrollHintConfig",
        {
            "texts": texts["scroll_hints"],
            "showDelayMs": 900,
        },
    )

    # Goofy overlay
    image_data_url = _encode_image_as_data_url(GOOFY_IMAGE)
    if image_data_url:
        goofy_idx = scene_ids.index("goofy")
        m.embed_data(
            "goofyConfig",
            {
                "imageDataUrl": image_data_url,
                "bounds": GOOFY_OVERLAY_BOUNDS,
                "sceneIndex": goofy_idx,
            },
        )
        m.add_custom_js(Path(BASE_DIR / "goofy_overlay.js"))
    else:
        print(f"Warning: overlay image not found at {GOOFY_IMAGE}")

    # Grid diagram HTML overlays
    m.add_custom_html(build_overlays_html(dem_color=DEM_COLOR, rep_color=REP_COLOR, locale=locale))

    # External CSS & JS
    m.add_custom_css(Path(BASE_DIR / "overlays.css"))

    # Handle URL step parameter BEFORE loading scene_effects.js
    # This runs before Swiper initialization
    m.add_custom_js("""
    (function() {
        try {
            var params = new URLSearchParams(window.location.search);
            var stepParam = params.get('step');
            console.log('[llmaps] Step parameter detected:', stepParam);
            if (stepParam !== null) {
                var stepIndex = parseInt(stepParam, 10);
                if (!isNaN(stepIndex) && stepIndex >= 0) {
                    // Store the desired initial slide globally
                    window.llmapsDesiredInitialSlide = stepIndex;
                    console.log('[llmaps] Will jump to slide:', stepIndex);
                }
            }
        } catch(e) {
            console.error('[llmaps] Error reading step parameter:', e);
        }
    })();
    """)

    m.add_custom_js(Path(BASE_DIR / "scene_effects.js"))

    # Apply desired initial slide after Swiper is initialized
    m.add_custom_js("""
    (function() {
        if (window.llmapsDesiredInitialSlide !== undefined) {
            var stepIndex = window.llmapsDesiredInitialSlide;
            var attempts = 0;
            var maxAttempts = 30;

            console.log('[llmaps] Starting to apply initial slide:', stepIndex);

            var checkAndSet = setInterval(function() {
                if (window.llmapsStorySwiper) {
                    console.log('[llmaps] Swiper found, setting to slide:', stepIndex, 'attempt:', attempts);
                    window.llmapsStorySwiper.slideTo(stepIndex);
                    attempts++;
                    // Keep trying to ensure it sticks
                    if (attempts >= maxAttempts) {
                        console.log('[llmaps] Max attempts reached');
                        clearInterval(checkAndSet);
                    }
                } else {
                    attempts++;
                    if (attempts >= maxAttempts) {
                        console.log('[llmaps] Swiper not found after max attempts');
                        clearInterval(checkAndSet);
                    }
                }
            }, 100);
        } else {
            console.log('[llmaps] No desired initial slide set');
        }
    })();
    """)

    return m


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build gerrymandering story map")
    parser.add_argument(
        "--locale",
        choices=["en", "ru", "all"],
        default="all",
        help="Output locale(s): en, ru, or all",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    locales = ["en", "ru"] if args.locale == "all" else [args.locale]

    for locale in locales:
        output_path = _output_path(locale)
        m = build_map(locale)
        m.save(str(output_path))
        print(f"Saved {locale} gerrymandering story map to {output_path}")


OUTPUT_HTML = _output_path("en")


if __name__ == "__main__":
    main()
