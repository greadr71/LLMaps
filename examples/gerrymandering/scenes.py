"""Scene definitions for the gerrymandering story map."""

from __future__ import annotations

from llmaps.components import Scene, SceneComparison
from texts import SCENE_ORDER, format_scene_content, get_texts

# ── Colors (shared with build_map.py) ──
DEM_COLOR = "#2166ac"
REP_COLOR = "#b2182b"

# ── Coordinates ──
PA_CENTER = [-77.53413, 41.01974]
PA_ZOOM = 6.92
PHILLY_CENTER = [-75.15, 40.0]
GOOFY_CENTER = [-75.63987, 40.07844]
GOOFY_ZOOM = 8.95
PHILLY_SUBURBS = [-75.55869, 40.16528]
PHILLY_SUBURBS_ZOOM = 8.58

# ── Popup config ──
POPUP_FIELDS = [
    "district",
    "year",
    "winner",
    "dem_votes",
    "rep_votes",
    "dem_pct",
    "rep_pct",
    "margin",
]

def build_popup_labels(locale: str = "en") -> dict[str, str]:
    return get_texts(locale)["popup_labels"]


def build_scenes(locale: str = "en") -> list[Scene]:
    texts = get_texts(locale)
    scene_texts = texts["scenes"]

    scenes_by_id = {
        "intro": Scene(
            id="intro",
            title=scene_texts["intro"]["title"],
            content=format_scene_content(scene_texts["intro"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
        ),
        "tools": Scene(
            id="tools",
            title=scene_texts["tools"]["title"],
            content=format_scene_content(scene_texts["tools"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
        ),
        "pa_context": Scene(
            id="pa_context",
            title=scene_texts["pa_context"]["title"],
            content=format_scene_content(scene_texts["pa_context"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
            visible_layers=["fill-2016"],
        ),
        "map_2016": Scene(
            id="map_2016",
            title=scene_texts["map_2016"]["title"],
            content=format_scene_content(scene_texts["map_2016"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
            visible_layers=["fill-2016"],
        ),
        "goofy": Scene(
            id="goofy",
            title=scene_texts["goofy"]["title"],
            content=format_scene_content(scene_texts["goofy"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=GOOFY_CENTER,
            zoom=GOOFY_ZOOM,
            comparison=SceneComparison(
                before_layers=["fill-2016"],
                after_layers=["fill-2016"],
                before_highlight={"pa-2016": [7]},
                after_highlight={"pa-2016": [7]},
            ),
        ),
        "packing": Scene(
            id="packing",
            title=scene_texts["packing"]["title"],
            content=format_scene_content(scene_texts["packing"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PHILLY_CENTER,
            zoom=9.5,
            visible_layers=["fill-2016"],
            highlight={"pa-2016": [1, 2, 13]},
        ),
        "cracking": Scene(
            id="cracking",
            title=scene_texts["cracking"]["title"],
            content=format_scene_content(scene_texts["cracking"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PHILLY_SUBURBS,
            zoom=PHILLY_SUBURBS_ZOOM,
            visible_layers=["fill-2016"],
            highlight={"pa-2016": [6, 7, 8]},
        ),
        "results_2016": Scene(
            id="results_2016",
            title=scene_texts["results_2016"]["title"],
            content=format_scene_content(scene_texts["results_2016"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
            visible_layers=["fill-2016"],
        ),
        "court": Scene(
            id="court",
            title=scene_texts["court"]["title"],
            content=format_scene_content(scene_texts["court"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
            visible_layers=["fill-2016"],
        ),
        "map_2018": Scene(
            id="map_2018",
            title=scene_texts["map_2018"]["title"],
            content=format_scene_content(scene_texts["map_2018"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
            comparison=SceneComparison(
                before_layers=["fill-2016"],
                after_layers=["fill-2018"],
                before_label="2016",
                after_label="2018",
            ),
        ),
        "new_d7": Scene(
            id="new_d7",
            title=scene_texts["new_d7"]["title"],
            content=format_scene_content(scene_texts["new_d7"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=GOOFY_CENTER,
            zoom=GOOFY_ZOOM,
            comparison=SceneComparison(
                before_layers=["fill-2016"],
                after_layers=["fill-2018"],
                before_label="2016",
                after_label="2018",
                before_highlight={"pa-2016": [7]},
                after_highlight={"pa-2018": [5, 6]},
            ),
        ),
        "results_2018": Scene(
            id="results_2018",
            title=scene_texts["results_2018"]["title"],
            content=format_scene_content(scene_texts["results_2018"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
            visible_layers=["fill-2018"],
        ),
        "conclusion": Scene(
            id="conclusion",
            title=scene_texts["conclusion"]["title"],
            content=format_scene_content(scene_texts["conclusion"]["content"], dem_color=DEM_COLOR, rep_color=REP_COLOR),
            center=PA_CENTER,
            zoom=PA_ZOOM,
            visible_layers=["fill-2018"],
        ),
    }

    return [scenes_by_id[scene_id] for scene_id in SCENE_ORDER]
