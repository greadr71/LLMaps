"""
Visibility-based resource optimization for LLMaps.

Frees RAM and GPU when the browser tab is hidden by removing GeoJSON sources
and layers and stopping the map; restores them when the tab becomes visible again.
"""

from typing import List


def generate_visibility_optimization_js(geojson_source_ids: List[str]) -> str:
    """
    Generate JavaScript for freeing RAM/GPU when the tab is hidden.

    When the tab is hidden: removes the given sources and their layers,
    stops the map, and hides the canvas. When the tab is visible again:
    calls map._loadLayers() to restore data, then resize and repaint.

    Parameters
    ----------
    geojson_source_ids : list of str
        Source IDs that hold GeoJSON data (to remove on hide). Vector-tile
        and raster sources are not included.

    Returns
    -------
    str
        JS code defining initVisibilityOptimization(maps, sourceIds).
    """
    if not geojson_source_ids:
        return "      function initVisibilityOptimization(maps, sourceIds) {}"
    ids_js = ", ".join(repr(sid) for sid in geojson_source_ids)
    return f"""      function initVisibilityOptimization(maps, sourceIds) {{
        const list = Array.isArray(maps) ? maps : [maps];
        const ids = sourceIds && sourceIds.length ? sourceIds : [{ids_js}];
        document.addEventListener("visibilitychange", async () => {{
          if (document.hidden) {{
            list.forEach(map => {{
              if (!map || !map._layersLoaded) return;
              map.stop();
              ids.forEach(sourceId => {{
                if (!map.getSource(sourceId)) return;
                const style = map.getStyle();
                if (style && style.layers) {{
                  style.layers
                    .filter(layer => layer.source === sourceId)
                    .forEach(layer => {{
                      try {{
                        if (map.getLayer(layer.id)) map.removeLayer(layer.id);
                      }} catch (e) {{}}
                    }});
                }}
                try {{ map.removeSource(sourceId); }} catch (e) {{}}
              }});
              map.getCanvas().style.display = "none";
              map._layersLoaded = false;
            }});
          }} else {{
            list.forEach(async map => {{
              if (!map || map._layersLoaded) {{ if (map) {{ map.getCanvas().style.display = "block"; map.resize(); map.triggerRepaint(); }} return; }}
              map.getCanvas().style.display = "block";
              if (map._loadLayers) await map._loadLayers();
              map._layersLoaded = true;
              map.resize();
              map.triggerRepaint();
            }});
          }}
        }});
      }}"""
