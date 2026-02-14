"""Server-side HTML and JavaScript generation for map legend.

Migrated from client-side DOM generation to server-side rendering,
inspired by wibemaps architecture with llmaps design aesthetics.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


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
    show_toggle = legend_config.get("show_toggle", True)
    layer_labels = legend_config.get("layer_labels", {})
    layer_counts = legend_config.get("layer_counts", {})
    layer_descriptions = legend_config.get("layer_descriptions", {})
    layer_color_ramps = legend_config.get("layer_color_ramps", {})
    instructions = legend_config.get("instructions")
    collapsed_tips = legend_config.get("collapsed", True)

    # Build layer information
    layers_info = []
    for layer in config.get("layers", []):
        layer_id = layer.get("id")
        if not layer_id or layer_id not in layer_labels:
            continue  # Skip layers not in legend

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

    # Build HTML sections
    sections = []

    # 1. Map title section (with border-bottom separator)
    sections.append(f'''        <div class="llmaps-legend-section llmaps-legend-map-title-section">
            <div class="llmaps-legend-map-title">{title}</div>
        </div>''')

    # 2. Layer sections
    for i, info in enumerate(layers_info):
        is_last_layer = (i == len(layers_info) - 1)
        layer_id = info["layer_id"]
        label = info["label"]
        color = info["color"]
        icon_class = info["icon_class"]
        count = info["count"]
        description = info["description"]
        color_ramp = info["color_ramp"]

        # Build description HTML
        desc_parts = []
        if description:
            desc_parts.append(description)
        if count is not None:
            desc_parts.append(f"({count:,})")

        desc_html = ""
        if desc_parts:
            desc_html = f'\n            <div class="llmaps-legend-description">{" ".join(desc_parts)}</div>'

        # Build toggle HTML (iOS-style switch)
        toggle_html = ""
        if show_toggle:
            toggle_html = f'''
                <label class="llmaps-layer-toggle">
                    <input type="checkbox" checked data-layer-id="{layer_id}">
                    <span class="llmaps-toggle-slider"></span>
                </label>'''

        # Build color ramp HTML
        ramp_html = ""
        if color_ramp and color_ramp.get("stops"):
            stops = color_ramp["stops"]
            colors = [stop[1] for stop in stops]
            gradient = f"linear-gradient(to right, {', '.join(colors)})"
            label_min = color_ramp.get("label_min", stops[0][0])
            label_max = color_ramp.get("label_max", stops[-1][0])
            ramp_html = f'''
            <div class="llmaps-legend-ramp" style="background: {gradient};"></div>
            <div class="llmaps-legend-ramp-labels">
                <span class="llmaps-legend-ramp-min">{label_min}</span>
                <span class="llmaps-legend-ramp-max">{label_max}</span>
            </div>'''

        # Section separator class (only if not last layer or there's more content after)
        separator_class = ""
        if not is_last_layer or has_basemap or instructions:
            separator_class = " llmaps-legend-section-separator"

        sections.append(f'''        <div class="llmaps-legend-section{separator_class}">
            <div class="llmaps-legend-layer-header">
                <div class="llmaps-legend-icon {icon_class}" style="background-color: {color};"></div>
                <div class="llmaps-legend-item-label">{label}</div>{toggle_html}
            </div>{desc_html}{ramp_html}
        </div>''')

    # 3. Basemap switcher section (if present)
    if has_basemap and basemap_in_legend:
        options_html = []
        for provider in tile_providers:
            provider_id = provider.get("id", "")
            provider_name = provider.get("name", provider_id)
            options_html.append(f'<option value="{provider_id}">{provider_name}</option>')

        separator_class = " llmaps-legend-section-separator" if instructions else ""
        sections.append(f'''        <div class="llmaps-legend-section llmaps-legend-basemap{separator_class}">
            <div class="llmaps-basemap-select-wrap">
                <select class="llmaps-basemap-select" id="llmaps-basemap-select">
                    {chr(10).join(f"                    {opt}" for opt in options_html)}
                </select>
            </div>
        </div>''')

    # 4. Collapsible Tips section (if instructions provided)
    if instructions:
        tips_items = [f'<li>{tip}</li>' for tip in instructions]
        collapsed_class = " collapsed" if collapsed_tips else ""

        sections.append(f'''        <div class="llmaps-legend-instructions">
            <div class="llmaps-legend-instructions-header{collapsed_class}" id="llmaps-tips-header">
                <span class="llmaps-legend-instructions-title">💡 Tips</span>
                <span class="llmaps-legend-instructions-arrow">▼</span>
            </div>
            <div class="llmaps-legend-instructions-content{collapsed_class}" id="llmaps-tips-content">
                <ul class="llmaps-legend-instructions-list">
                    {chr(10).join(f"                    {item}" for item in tips_items)}
                </ul>
            </div>
        </div>''')

    # Assemble final legend HTML
    return f'''    <!-- Legend (server-rendered) -->
    <div class="llmaps-legend {position}">
        <div class="llmaps-legend-header">
            <div class="llmaps-legend-title">{title}</div>
            <div class="llmaps-legend-toggle-btn" id="llmaps-legend-toggle">
                <svg class="llmaps-chevron-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg class="llmaps-layers-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </div>
        </div>
        <div class="llmaps-legend-content">
{chr(10).join(sections)}
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
        })();'''
