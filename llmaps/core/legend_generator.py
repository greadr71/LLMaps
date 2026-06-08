"""Server-side HTML and JavaScript generation for map legend.

Migrated from client-side DOM generation to server-side rendering,
inspired by wibemaps architecture with llmaps design aesthetics.
"""

from __future__ import annotations

import html
import re
from typing import Any, Dict, List

from llmaps.components.data_driven_size import render_size_legend_svg_fragment


def _extract_simple_color(color_value: Any) -> str:
    """Extract a simple hex color from a paint property value.

    Parameters
    ----------
    color_value:
        Color value from layer paint property. Can be a string "#hex" or
        a MapLibre expression (list). For expressions, returns "#666" fallback.

    Returns
    -------
    str
        Hex color string.
    """
    if isinstance(color_value, str):
        return color_value
    # Expression-based colors show fallback
    return "#666"


def _get_layer_display_info(layer: Dict[str, Any]) -> Dict[str, str]:
    """Extract display information from a layer dict.

    Parameters
    ----------
    layer:
        Layer dict from config["layers"].

    Returns
    -------
    dict
        Dict with keys: layer_id, layer_type, color, icon_class.
    """
    layer_id = layer.get("id", "unknown")
    layer_type = layer.get("type", "circle")
    paint = layer.get("paint", {})

    # Determine color and icon class based on layer type
    if layer_type == "circle":
        color = _extract_simple_color(paint.get("circle-color", "#3182bd"))
        icon_class = "circle"
    elif layer_type == "fill":
        color = _extract_simple_color(paint.get("fill-color", "#3182bd"))
        icon_class = "fill"
    elif layer_type == "line":
        color = _extract_simple_color(paint.get("line-color", "#3182bd"))
        icon_class = "line"
    else:
        # Fallback for unknown types
        color = "#666"
        icon_class = "fill"

    return {
        "layer_id": layer_id,
        "layer_type": layer_type,
        "color": color,
        "icon_class": icon_class,
    }


def _default_tips_title(locale: str) -> str:
    """Localized default heading for the collapsible instructions block."""
    loc = str(locale or "en-US").replace("_", "-").lower()
    if loc.startswith("ru"):
        return "💡 Подсказки"
    return "💡 Tips"


def _collect_size_legend_specs(
    config: Dict[str, Any], legend_config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    specs: List[Dict[str, Any]] = []
    for layer_index, layer in enumerate(config.get("layers", [])):
        meta = layer.get("metadata") or {}
        leg = meta.get("llmaps_size_legend")
        if isinstance(leg, dict):
            spec = dict(leg)
            spec.setdefault("id", layer.get("id") or f"layer-{layer_index}")
            specs.append(spec)
    extra = legend_config.get("size_legends")
    if isinstance(extra, list):
        for item_index, item in enumerate(extra):
            if isinstance(item, dict):
                spec = dict(item)
                spec.setdefault("id", f"extra-{item_index}")
                specs.append(spec)
    return specs


def _slugify_legend_group_id(value: Any, fallback: str) -> str:
    raw = str(value or "").strip().lower()
    slug = re.sub(r"[^a-z0-9_-]+", "-", raw).strip("-")
    return slug or fallback


def _legend_html_id(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-")
    return safe or "legend-group"


def _append_separator(html_block: str) -> str:
    if 'class="llmaps-legend-group' in html_block:
        if 'class="llmaps-legend-group llmaps-legend-section-separator' in html_block:
            return html_block
        return html_block.replace(
            'class="llmaps-legend-group',
            'class="llmaps-legend-group llmaps-legend-section-separator',
            1,
        )
    if "llmaps-legend-section-separator" in html_block:
        return html_block
    return html_block.replace(
        'class="llmaps-legend-section',
        'class="llmaps-legend-section llmaps-legend-section-separator',
        1,
    )


def _render_legend_items(items: List[Dict[str, str]]) -> str:
    rendered: List[str] = []
    total = len(items)
    for i, item in enumerate(items):
        html_block = item["html"]
        if i < total - 1:
            html_block = _append_separator(html_block)
        rendered.append(html_block)
    return chr(10).join(rendered)


def _render_layer_section(info: Dict[str, Any], show_toggle: bool) -> str:
    layer_id = str(info["layer_id"])
    label = html.escape(str(info["label"]))
    color = html.escape(str(info["color"]), quote=True)
    icon_class = html.escape(str(info["icon_class"]), quote=True)
    count = info["count"]
    description = info["description"]
    color_ramp = info["color_ramp"]

    desc_parts = []
    if description:
        desc_parts.append(html.escape(str(description)))
    if count is not None:
        desc_parts.append(f"({int(count):,})")

    desc_html = ""
    if desc_parts:
        desc_html = f'\n            <div class="llmaps-legend-description">{" ".join(desc_parts)}</div>'

    toggle_html = ""
    if show_toggle:
        toggle_html = f'''
                <label class="llmaps-layer-toggle">
                    <input type="checkbox" checked data-layer-id="{html.escape(layer_id, quote=True)}">
                    <span class="llmaps-toggle-slider"></span>
                </label>'''

    ramp_html = ""
    if color_ramp and color_ramp.get("stops"):
        stops = color_ramp["stops"]
        colors = [str(stop[1]) for stop in stops]
        gradient = f"linear-gradient(to right, {', '.join(colors)})"
        label_min = html.escape(str(color_ramp.get("label_min", stops[0][0])))
        label_max = html.escape(str(color_ramp.get("label_max", stops[-1][0])))
        ramp_html = f'''
            <div class="llmaps-legend-ramp" style="background: {html.escape(gradient, quote=True)};"></div>
            <div class="llmaps-legend-ramp-labels">
                <span class="llmaps-legend-ramp-min">{label_min}</span>
                <span class="llmaps-legend-ramp-max">{label_max}</span>
            </div>'''

    return f'''        <div class="llmaps-legend-section" data-legend-layer-id="{html.escape(layer_id, quote=True)}">
            <div class="llmaps-legend-layer-header">
                <div class="llmaps-legend-icon {icon_class}" style="background-color: {color};"></div>
                <div class="llmaps-legend-item-label">{label}</div>{toggle_html}
            </div>{desc_html}{ramp_html}
        </div>'''


def _render_legend_group(group: Dict[str, Any], items: List[Dict[str, str]]) -> str:
    group_id = _slugify_legend_group_id(
        group.get("id") or group.get("key") or group.get("title"),
        "group",
    )
    title = group.get("title")
    collapsible = bool(group.get("collapsible", False) or group.get("collapsed", False))
    collapsed = bool(group.get("collapsed", False))
    collapsed_class = " collapsed" if collapsed else ""
    content_id = f"llmaps-legend-group-{_legend_html_id(group_id)}"
    title_html = ""
    if title and collapsible:
        title_html = f'''            <button class="llmaps-legend-group-header{collapsed_class}" type="button" data-legend-group-target="{html.escape(content_id, quote=True)}" aria-expanded="{str(not collapsed).lower()}">
                <span class="llmaps-legend-group-title">{html.escape(str(title))}</span>
                <span class="llmaps-legend-group-arrow">▼</span>
            </button>'''
    elif title:
        title_html = f'''            <div class="llmaps-legend-group-title llmaps-legend-group-title-static">{html.escape(str(title))}</div>'''
    if group.get("item_separators"):
        content_html = _render_legend_items(items)
    else:
        content_html = chr(10).join(item["html"] for item in items)
    return f'''        <div class="llmaps-legend-group" data-legend-group-id="{html.escape(group_id, quote=True)}">
{title_html}
            <div class="llmaps-legend-group-content{collapsed_class}" id="{html.escape(content_id, quote=True)}">
{content_html}
            </div>
        </div>'''


def generate_legend_html(config: Dict[str, Any]) -> str:
    """Generate server-side HTML for the legend component.

    Parameters
    ----------
    config:
        Full map configuration dict from Map.to_dict().
        Must contain "components" list with a legend component and
        "layers" list with layer definitions.

    Returns
    -------
    str
        HTML string for the legend, ready to insert into base template.
    """
    # Find legend config in components
    legend_config = None
    for comp in config.get("components", []):
        if comp.get("type") == "component_type" and comp.get("component_type") == "legend":
            legend_config = comp
            break
        if comp.get("type") == "legend":
            legend_config = comp
            break

    if not legend_config:
        return ""  # No legend configured

    # Extract legend configuration
    position = legend_config.get("position", "top-right")
    title = legend_config.get("title") or config.get("title") or "Map"
    description = legend_config.get("description")
    entries = legend_config.get("entries")
    color_ramp = legend_config.get("color_ramp")
    show_toggle = legend_config.get("show_toggle", True)
    layer_labels = legend_config.get("layer_labels", {})
    layer_counts = legend_config.get("layer_counts", {})
    layer_descriptions = legend_config.get("layer_descriptions", {})
    layer_color_ramps = legend_config.get("layer_color_ramps", {})
    instructions = legend_config.get("instructions")
    collapsed_tips = legend_config.get("collapsed", True)
    tips_title_raw = legend_config.get("tips_title")
    map_locale = str(config.get("locale") or "en-US")
    if tips_title_raw is not None:
        tips_title_display = html.escape(str(tips_title_raw))
    else:
        tips_title_display = html.escape(_default_tips_title(map_locale))
    size_legend_specs = _collect_size_legend_specs(config, legend_config)
    has_size_legends = len(size_legend_specs) > 0

    # Build layer information
    # A layer appears in the legend if it has a label OR a color ramp
    layers_info = []
    for layer in config.get("layers", []):
        layer_id = layer.get("id")
        if not layer_id:
            continue
        if layer_id not in layer_labels and layer_id not in layer_color_ramps:
            continue  # Skip layers not mentioned in legend config

        info = _get_layer_display_info(layer)
        info["label"] = layer_labels.get(layer_id, layer_id)
        info["count"] = layer_counts.get(layer_id)
        info["description"] = layer_descriptions.get(layer_id)
        info["color_ramp"] = layer_color_ramps.get(layer_id)
        layers_info.append(info)

    # Check if basemap switcher should be embedded
    tile_providers = config.get("tile_providers", [])
    has_basemap = len(tile_providers) > 0
    basemap_in_legend = False
    for comp in config.get("components", []):
        if comp.get("type") == "basemap_switcher":
            basemap_in_legend = True
            break

    # Build legend items. Flat legends keep the historical visual order, while
    # grouped legends can reorder the same item pool declaratively.
    items: List[Dict[str, str]] = []

    if entries:
        entry_sections = []
        for entry in entries:
            label = html.escape(str(entry.get("label", "Unnamed")))
            color = html.escape(str(entry.get("color", "#999")), quote=True)
            entry_sections.append(f'''        <div class="llmaps-legend-section">
            <div class="llmaps-legend-layer-header">
                <div class="llmaps-legend-icon circle" style="background-color: {color};"></div>
                <div class="llmaps-legend-item-label">{label}</div>
            </div>
        </div>''')
        items.append({"key": "entries", "html": _render_legend_items([{"html": s} for s in entry_sections])})

    if color_ramp and color_ramp.get("colors") and color_ramp.get("labels"):
        colors = [str(c) for c in color_ramp["colors"]]
        labels = color_ramp["labels"]
        gradient = f"linear-gradient(to right, {', '.join(colors)})"
        items.append({"key": "color_ramp", "html": f'''        <div class="llmaps-legend-section">
            <div class="llmaps-legend-ramp" style="background: {html.escape(gradient, quote=True)};"></div>
            <div class="llmaps-legend-ramp-labels">
                <span class="llmaps-legend-ramp-min">{html.escape(str(labels[0]))}</span>
                <span class="llmaps-legend-ramp-max">{html.escape(str(labels[-1]))}</span>
            </div>
        </div>'''})

    for info in layers_info:
        layer_id = str(info["layer_id"])
        items.append(
            {
                "key": f"layer:{layer_id}",
                "html": _render_layer_section(info, show_toggle),
            }
        )

    if has_basemap and basemap_in_legend:
        options_html = []
        for provider in tile_providers:
            provider_id = str(provider.get("id", ""))
            provider_name = str(provider.get("name", provider_id))
            options_html.append(
                f'<option value="{html.escape(provider_id, quote=True)}">{html.escape(provider_name)}</option>'
            )

        items.append({"key": "basemap", "html": f'''        <div class="llmaps-legend-section llmaps-legend-basemap">
            <div class="llmaps-basemap-select-wrap">
                <select class="llmaps-basemap-select" id="llmaps-basemap-select">
                    {chr(10).join(f"                    {opt}" for opt in options_html)}
                </select>
            </div>
        </div>'''})

    if size_legend_specs:
        for spec in size_legend_specs:
            svg_block = render_size_legend_svg_fragment(spec)
            if not svg_block:
                continue
            spec_id = str(spec.get("id"))
            items.append(
                {
                    "key": f"size_legend:{spec_id}",
                    "html": f'''        <div class="llmaps-legend-section llmaps-size-legend-section" data-size-legend-id="{html.escape(spec_id, quote=True)}">
            <div class="llmaps-size-legend-wrap">
                {svg_block}
            </div>
        </div>''',
                }
            )

    if instructions:
        tips_items = [f"<li>{html.escape(str(tip))}</li>" for tip in instructions]
        collapsed_class = " collapsed" if collapsed_tips else ""

        items.append({"key": "instructions", "html": f'''        <div class="llmaps-legend-instructions">
            <div class="llmaps-legend-instructions-header{collapsed_class}" id="llmaps-tips-header">
                <span class="llmaps-legend-instructions-title">{tips_title_display}</span>
                <span class="llmaps-legend-instructions-arrow">▼</span>
            </div>
            <div class="llmaps-legend-instructions-content{collapsed_class}" id="llmaps-tips-content">
                <ul class="llmaps-legend-instructions-list">
                    {chr(10).join(f"                    {item}" for item in tips_items)}
                </ul>
            </div>
        </div>'''})

    item_by_key = {item["key"]: item for item in items}
    rendered_keys: set[str] = set()
    sections: List[str] = []
    groups = legend_config.get("groups") or []
    order = legend_config.get("order") or []

    if groups:
        group_by_key: Dict[str, Dict[str, Any]] = {}
        for i, group in enumerate(groups):
            if not isinstance(group, dict):
                continue
            group_id = _slugify_legend_group_id(
                group.get("id") or group.get("key") or group.get("title"),
                f"group-{i}",
            )
            group_by_key[f"group:{group_id}"] = group

        def render_group(group: Dict[str, Any]) -> str:
            group_items: List[Dict[str, str]] = []
            group_keys: List[str] = []
            for layer_id in group.get("layer_ids") or []:
                group_keys.append(f"layer:{layer_id}")
            for size_legend_id in group.get("size_legend_ids") or []:
                group_keys.append(f"size_legend:{size_legend_id}")
            for key in group.get("order") or []:
                if isinstance(key, str):
                    group_keys.append(key)

            for key in dict.fromkeys(group_keys):
                item = item_by_key.get(key)
                if item is None or key in rendered_keys:
                    continue
                group_items.append(item)
                rendered_keys.add(key)
            if not group_items:
                return ""
            rendered = _render_legend_group(group, group_items)
            if group.get("separator_after"):
                rendered = _append_separator(rendered)
            return rendered

        ordered_refs = [str(ref) for ref in order] if order else list(group_by_key.keys())
        for ref in ordered_refs:
            if ref.startswith("group:"):
                rendered = render_group(group_by_key.get(ref, {}))
                if rendered:
                    sections.append(rendered)
                continue
            item = item_by_key.get(ref)
            if item is not None and ref not in rendered_keys:
                sections.append(item["html"])
                rendered_keys.add(ref)

        for group_key, group in group_by_key.items():
            if group_key not in ordered_refs:
                rendered = render_group(group)
                if rendered:
                    sections.append(rendered)

        for item in items:
            if item["key"] not in rendered_keys:
                sections.append(item["html"])
                rendered_keys.add(item["key"])
    else:
        sections = [item["html"] for item in items]

    if groups:
        sections_html = chr(10).join(sections)
    else:
        sections_html = _render_legend_items([{"html": s} for s in sections])

    # Assemble final legend HTML
    description_html = ""
    if description:
        description_html = f'\n            <div class="llmaps-legend-description" style="padding: 0 20px 12px 20px; font-size: 13px; color: #6b7280;">{html.escape(str(description))}</div>'
    
    return f'''    <!-- Legend (server-rendered) -->
    <div class="llmaps-legend {position}">
        <div class="llmaps-legend-header">
            <div class="llmaps-legend-title">{html.escape(str(title))}</div>
            <div class="llmaps-legend-toggle-btn" id="llmaps-legend-toggle">
                <svg class="llmaps-chevron-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg class="llmaps-layers-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </div>
        </div>{description_html}
        <div class="llmaps-legend-content">
{sections_html}
        </div>
    </div>'''


def generate_legend_js() -> str:
    """Generate JavaScript code for legend interactivity.

    Returns
    -------
    str
        JavaScript code for toggle layer visibility, collapse/expand,
        and instructions toggle.
    """
    return '''        // Legend interactivity (server-rendered legend)
        (function() {
            const legendEl = document.querySelector('.llmaps-legend');
            if (!legendEl) return;

            // Toggle legend collapse/expand
            const toggleBtn = document.getElementById('llmaps-legend-toggle');
            if (toggleBtn) {
                toggleBtn.addEventListener('click', function() {
                    legendEl.classList.toggle('collapsed');
                });
            }

            // Layer visibility toggles (iOS-style switches)
            const toggles = legendEl.querySelectorAll('.llmaps-layer-toggle input[type="checkbox"]');
            toggles.forEach(function(checkbox) {
                checkbox.addEventListener('change', function() {
                    const layerId = this.getAttribute('data-layer-id');
                    const visibility = this.checked ? 'visible' : 'none';
                    
                    // Apply to all maps (supports comparison mode)
                    const maps = window.llmaps_maps || [window.llmaps_map];
                    maps.forEach(function(map) {
                        if (map && map.getLayer && map.getLayer(layerId)) {
                            map.setLayoutProperty(layerId, 'visibility', visibility);
                        }
                    });
                });
            });

            // Basemap switcher
            const basemapSelect = document.getElementById('llmaps-basemap-select');
            if (basemapSelect && window.llmaps_switchBasemap) {
                basemapSelect.addEventListener('change', function() {
                    window.llmaps_switchBasemap(this.value);
                });
            }

            // Instructions toggle
            const tipsHeader = document.getElementById('llmaps-tips-header');
            const tipsContent = document.getElementById('llmaps-tips-content');
            if (tipsHeader && tipsContent) {
                tipsHeader.addEventListener('click', function() {
                    tipsHeader.classList.toggle('collapsed');
                    tipsContent.classList.toggle('collapsed');
                });
            }

            // Legend groups
            const groupHeaders = legendEl.querySelectorAll('.llmaps-legend-group-header[data-legend-group-target]');
            groupHeaders.forEach(function(header) {
                header.addEventListener('click', function() {
                    const targetId = header.getAttribute('data-legend-group-target');
                    const content = targetId ? document.getElementById(targetId) : null;
                    if (!content) return;
                    const collapsed = !content.classList.contains('collapsed');
                    header.classList.toggle('collapsed', collapsed);
                    content.classList.toggle('collapsed', collapsed);
                    header.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
                });
            });
        })();'''
