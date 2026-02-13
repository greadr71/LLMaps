"""HTML and style generation helpers for LLMaps.

This module converts a serialisable map configuration dictionary (as
produced by :meth:`llmaps.map.Map.to_dict`) into standalone HTML using
Jinja2 templates.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape


def _create_environment() -> Environment:
    template_path = resources.files("llmaps") / "templates"
    loader = FileSystemLoader(str(template_path))
    env = Environment(loader=loader, autoescape=select_autoescape(["html", "xml"]))
    return env


def _load_base_css() -> str:
    """Load base CSS from templates/css/base.css for injection into HTML."""
    css_path = resources.files("llmaps") / "templates" / "css" / "base.css"
    return css_path.read_text(encoding="utf-8")


_JS_TEMPLATES = (
    "js/config.js.j2",
    "js/sources.js.j2",
    "js/layers.js.j2",
    "js/comparison.js.j2",
    "js/components.js.j2",
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


def render_map_html(config: Dict[str, Any]) -> str:
    """Render a map *config* to HTML using the base template."""
    from .legend_generator import generate_legend_html

    env = _create_environment()
    template = env.get_template("base.html")
    use_compression = config.get("use_compression", False)
    
    # Generate server-side legend HTML
    legend_html = generate_legend_html(config)
    
    return template.render(
        title=config.get("title") or "LLMaps",
        map_config_json=json.dumps(config),
        llmaps_css=_load_base_css(),
        llmaps_js=_render_base_js(config),
        use_compression=use_compression,
        legend_html=legend_html,
    )

