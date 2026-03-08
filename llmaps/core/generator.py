"""HTML and style generation helpers for LLMaps.

This module converts a serialisable map configuration dictionary (as
produced by :meth:`llmaps.map.Map.to_dict`) into standalone HTML using
Jinja2 templates.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape


def _create_environment() -> Environment:
    template_path = resources.files("llmaps") / "templates"
    loader = FileSystemLoader(str(template_path))
    env = Environment(loader=loader, autoescape=select_autoescape(["html", "xml"]))
    return env


def _load_base_css(config: Optional[Dict[str, Any]] = None) -> str:
    """Load base CSS (+ storytelling CSS if needed) for injection into HTML."""
    css_path = resources.files("llmaps") / "templates" / "css" / "base.css"
    css = css_path.read_text(encoding="utf-8")
    if config and config.get("storytelling"):
        story_css_path = resources.files("llmaps") / "templates" / "css" / "storytelling.css"
        css += "\n" + story_css_path.read_text(encoding="utf-8")
    return css


def _generate_storytelling_html(config: Dict[str, Any]) -> str:
    """Build the narrative panel HTML from storytelling config."""
    story = config.get("storytelling")
    if not story:
        return ""
    scenes = story.get("scenes", [])
    total = len(scenes)

    parts = []
    # Mobile progress counter (hidden on desktop via CSS)
    if story.get("progress") and total > 1:
        parts.append(
            '<div class="llmaps-story-progress-mobile">'
            '<span class="progress-text">1 / {0}</span>'
            '<div class="progress-bar" style="width: {1:.1f}%"></div>'
            '</div>'.format(total, 100 / total)
        )

    for i, scene in enumerate(scenes):
        parts.append(
            f'<section class="story-step" data-index="{i}">'
            f'<h2>{scene["title"]}</h2>'
            f'<div class="step-content">{scene["content"]}</div>'
            f"</section>"
        )

    return "\n".join(parts)


_JS_TEMPLATES = (
    "js/config.js.j2",
    "js/sources.js.j2",
    "js/layers.js.j2",
    "js/comparison.js.j2",
    "js/components.js.j2",
    "js/storytelling.js.j2",
    "js/lifecycle.js.j2",
    "js/init.js.j2",
)


def _render_base_js(config: Dict[str, Any]) -> str:
    """Render all JS templates with config context and concatenate into one string."""
    from llmaps.optimizers.compression import generate_decompression_js
    from llmaps.optimizers.visibility import generate_visibility_optimization_js
    from llmaps.optimizers.multipoint import generate_multipoint_explosion_js
    from .legend_generator import generate_legend_js

    env = _create_environment()
    use_compression = config.get("use_compression", False)
    sources = config.get("sources") or {}
    geojson_source_ids = [sid for sid, s in sources.items() if s.get("type") != "vector"]
    context = {
        "config": config,
        "decompression_js": generate_decompression_js() if use_compression else "",
        "visibility_optimization_js": generate_visibility_optimization_js(geojson_source_ids),
        "multipoint_explosion_js": generate_multipoint_explosion_js(),
    }
    parts = []
    for name in _JS_TEMPLATES:
        template = env.get_template(name)
        parts.append(template.render(**context))
    
    # Add server-rendered legend JS
    parts.append(generate_legend_js())
    
    return "\n".join(parts)


def render_map_html(
    config: Dict[str, Any],
    *,
    custom_js: Optional[List[str]] = None,
    custom_css: Optional[List[str]] = None,
    custom_html: Optional[List[str]] = None,
    user_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Render a map *config* to HTML using the base template."""
    from .legend_generator import generate_legend_html

    env = _create_environment()
    template = env.get_template("base.html")
    use_compression = config.get("use_compression", False)
    html_lang = str(config.get("locale") or "en-US").replace("_", "-")
    components = config.get("components") or []
    use_flatpickr = any(
        component.get("type") == "dashboard"
        and any((filter_item or {}).get("type") == "date" for filter_item in (component.get("filters") or []))
        for component in components
    )
    
    # Generate server-side legend HTML
    legend_html = generate_legend_html(config)

    # Generate storytelling narrative HTML if component is present
    story_cfg = config.get("storytelling") or {}
    storytelling_html = _generate_storytelling_html(config)
    use_scrollama = bool(story_cfg)
    use_compare = bool(config.get("comparison") or story_cfg.get("hasComparison"))
    use_swiper = bool(story_cfg.get("useSwiperCdn"))

    # Combine custom JS snippets
    custom_js_str = "\n".join(custom_js) if custom_js else ""

    # Combine custom CSS
    custom_css_str = "\n".join(custom_css) if custom_css else ""

    # Combine custom HTML blocks
    custom_html_str = "\n".join(custom_html) if custom_html else ""

    # Serialize user data for window.llmapsData
    user_data_json = json.dumps(user_data, ensure_ascii=False) if user_data else ""

    return template.render(
        title=config.get("title") or "LLMaps",
        html_lang=html_lang,
        map_config_json=json.dumps(config),
        llmaps_css=_load_base_css(config),
        llmaps_js=_render_base_js(config),
        use_compression=use_compression,
        use_flatpickr=use_flatpickr,
        use_scrollama=use_scrollama,
        use_compare=use_compare,
        use_swiper=use_swiper,
        legend_html=legend_html,
        storytelling_html=storytelling_html,
        story_position=story_cfg.get("position", "left"),
        story_width=story_cfg.get("width", 400),
        custom_js=custom_js_str,
        custom_css=custom_css_str,
        custom_html=custom_html_str,
        user_data_json=user_data_json,
    )

