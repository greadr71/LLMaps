"""Core map abstraction for LLMaps.

This module defines the public ``Map`` class that is used in examples and
high-level documentation. The implementation is intentionally small and
data-oriented: it focuses on building a serialisable configuration that
can be consumed by the HTML/JS generator.

The goal is to provide a predictable, LLM-friendly API rather than a
feature-complete mapping framework.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

from .components.base import BaseComponent
from .layers.base import BaseLayer
from .tiles import resolve_tile_provider


@dataclass
class Map:
    """High-level map configuration.

    Parameters
    ----------
    center:
        Initial map center as ``[lon, lat]``.
    zoom:
        Initial zoom level, typically between 0 and 22.
    title:
        Optional map title used in HTML.
    tiles:
        Tile provider identifier, e.g. ``"osm"`` or ``"carto-light"``.
    embedded:
        If ``True``, inline file-based sources into the HTML so the map works
        via ``file://`` without a web server.
    use_compression:
        If ``True`` and ``embedded`` is enabled, compress embedded GeoJSON to
        reduce HTML size.
    locale:
        Locale identifier for number formatting in UI components (Popup, Sidebar).
        Default is ``"en-US"`` (uses commas as thousand separators: 1,000,000).
        Use ``"ru-RU"`` for Russian format (spaces as separators: 1 000 000).
        Supports any valid BCP 47 language tag.
    lazy_init:
        If ``True`` and there are 3+ map instances on the page, the map is created
        only when its container enters the viewport and is disposed when it leaves,
        to avoid exceeding the browser's WebGL context limit.
    max_active_maps:
        Maximum number of map instances to keep active at once when using lazy_init.
        Oldest (least recently used) maps are disposed when the limit is exceeded.
        Default 8; browsers typically allow about 16 WebGL contexts per page.
    map_instance_count:
        Total number of map instances on this page. Used to decide whether to enable
        lifecycle (lazy init + dispose): only when map_instance_count >= 3.
        Default: 2 for comparison mode, 1 otherwise. Set to 3 or more when building
        a page with many map widgets so that lazy_init takes effect.
    hash_position:
        Sync map position with URL hash in format ``#zoom/lat/lon``.
        If ``None`` (default), value is inferred from ``Controls(hash=...)`` for
        backward compatibility; otherwise this explicit map-level setting is used.
    """

    center: Sequence[float]
    zoom: float = 10.0
    title: Optional[str] = None
    tiles: str = "osm"
    tile_providers: Optional[Sequence[str]] = None
    embedded: bool = True
    use_compression: bool = True
    custom_attribution: Optional[str] = '© <a href="https://github.com/greadr71/LLMaps" target="_blank">LLMaps</a>'
    locale: str = "en-US"
    lazy_init: bool = False
    max_active_maps: int = 8
    map_instance_count: Optional[int] = None
    hash_position: Optional[bool] = None

    _layers: List[BaseLayer] = field(default_factory=list, init=False, repr=False)
    _components: List[BaseComponent] = field(default_factory=list, init=False, repr=False)
    _comparison: Optional[Dict[str, List[str]]] = field(
        default=None, init=False, repr=False
    )
    _custom_js: List[str] = field(default_factory=list, init=False, repr=False)
    _custom_css: List[str] = field(default_factory=list, init=False, repr=False)
    _custom_html: List[str] = field(default_factory=list, init=False, repr=False)
    _user_data: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def add_layer(self, layer: BaseLayer) -> "Map":
        """Attach a visual layer to the map.

        The method returns ``self`` to support method chaining::

            map.add_layer(layer).add_component(legend).save("map.html")
        """

        self._layers.append(layer)
        return self

    def add_component(self, component: BaseComponent) -> "Map":
        """Attach a UI component (legend, popup, controls, …).

        Returns ``self`` to support method chaining.
        """

        self._components.append(component)
        return self

    def enable_comparison(
        self, left_layers: List[str], right_layers: List[str]
    ) -> "Map":
        """Enable before/after comparison: two maps with a slider.

        Left map shows left_layers, right map shows right_layers.
        Layer ids must exist on this map.

        Returns ``self`` for chaining.
        """
        layer_ids = {layer.id for layer in self._layers}
        missing = set(left_layers + right_layers) - layer_ids
        if missing:
            raise ValueError(f"Layers not found: {', '.join(sorted(missing))}")
        self._comparison = {"left_layers": list(left_layers), "right_layers": list(right_layers)}
        return self

    def add_custom_js(self, js: Union[str, Path]) -> "Map":
        """Inject custom JavaScript into the generated HTML.

        *js* can be a ``Path`` to a ``.js`` file (contents will be read)
        or a plain string with inline JS code.  Multiple calls are
        cumulative — all snippets are appended in order after the core
        llmaps JS.

        Returns ``self`` for chaining.
        """
        if isinstance(js, Path):
            js = js.read_text(encoding="utf-8")
        self._custom_js.append(js)
        return self

    def add_custom_css(self, css: Union[str, Path]) -> "Map":
        """Inject custom CSS into the generated HTML.

        *css* can be a ``Path`` to a ``.css`` file or an inline CSS string.
        Appended inside ``<style>`` after the base llmaps CSS.

        Returns ``self`` for chaining.
        """
        if isinstance(css, Path):
            css = css.read_text(encoding="utf-8")
        self._custom_css.append(css)
        return self

    def add_custom_html(self, html: str) -> "Map":
        """Inject custom HTML into the ``<body>`` of the generated page.

        The HTML is inserted before ``</body>``, after the map container
        and before scripts.  Useful for sidebars, overlays, or custom
        UI elements.

        Returns ``self`` for chaining.
        """
        self._custom_html.append(html)
        return self

    def embed_data(self, key: str, data: Any) -> "Map":
        """Embed arbitrary JSON-serialisable data into the HTML.

        The data is available on the frontend as
        ``window.llmapsData.<key>``.

        Returns ``self`` for chaining.
        """
        self._user_data[key] = data
        return self

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------
    def _tile_config(self) -> Dict[str, Any]:
        config = dict(resolve_tile_provider(self.tiles))
        # Substitute {lang} placeholder with locale (BCP 47 → underscore)
        lang_tag = self.locale.replace("-", "_")
        config["url_template"] = config["url_template"].replace("{lang}", lang_tag)
        if self.custom_attribution:
            # Merge provider attribution with custom attribution
            provider_attr = config.get("attribution", "")
            config["attribution"] = (
                f"{provider_attr} | {self.custom_attribution}"
                if provider_attr
                else self.custom_attribution
            )
        return config

    def _apply_custom_attribution(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply custom attribution to provider config."""
        config = dict(provider_config)
        if self.custom_attribution:
            provider_attr = config.get("attribution", "")
            config["attribution"] = (
                f"{provider_attr} | {self.custom_attribution}"
                if provider_attr
                else self.custom_attribution
            )
        return config

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable representation of the map.

        This configuration is consumed by the HTML/JS generator and is
        intentionally conservative: plain dicts, lists and primitives only.
        """

        # Serialize layers, generating additional outline layers when needed
        layers_list = []
        for layer in self._layers:
            layer_dict = layer.to_dict()
            layers_list.append(layer_dict)
            
            # If a fill layer needs a thick stroke, create a separate line layer
            metadata = layer_dict.get("metadata", {})
            if metadata.get("needs_outline_layer"):
                outline_layer = {
                    "id": f"{layer_dict['id']}-outline",
                    "type": "line",
                    "source": layer_dict["source"],
                    "visible": layer_dict.get("visible", True),
                    "metadata": {},
                    "paint": {
                        "line-color": metadata["outline_color"],
                        "line-width": metadata["outline_width"],
                    },
                    "layout": {},
                }
                if layer_dict.get("minzoom") is not None:
                    outline_layer["minzoom"] = layer_dict["minzoom"]
                if layer_dict.get("maxzoom") is not None:
                    outline_layer["maxzoom"] = layer_dict["maxzoom"]
                layers_list.append(outline_layer)

        hash_position = self.hash_position
        if hash_position is None:
            for component in self._components:
                if getattr(component, "component_type", "") != "controls":
                    continue
                hash_value = getattr(component, "hash", None)
                if isinstance(hash_value, bool):
                    hash_position = hash_value
                    break
            if hash_position is None:
                hash_position = False

        out: Dict[str, Any] = {
            "title": self.title,
            "center": list(self.center),
            "zoom": self.zoom,
            "tiles": self._tile_config(),
            "layers": layers_list,
            "locale": self.locale,
            "hash_position": hash_position,
        }
        if self.tile_providers is not None:
            out["tile_providers"] = [
                self._apply_custom_attribution(resolve_tile_provider(pid))
                for pid in self.tile_providers
            ]
        out["components"] = [component.to_dict() for component in self._components]
        # Promote storytelling config to top level for template access
        for comp in self._components:
            if getattr(comp, "component_type", "") == "storytelling":
                out["storytelling"] = comp.to_dict()
                break
        out["embedded"] = self.embedded
        out["use_compression"] = self.use_compression
        out["lazy_init"] = self.lazy_init
        out["max_active_maps"] = self.max_active_maps
        # Determine map instance count: explicit override, comparison mode (2),
        # storytelling with comparison scenes (3: main + before + after), or 1.
        story_has_comparison = False
        for comp in self._components:
            if getattr(comp, "component_type", "") == "storytelling":
                story_has_comparison = getattr(comp, "has_comparison", False)
                break
        if self.map_instance_count is not None:
            out["map_instance_count"] = self.map_instance_count
        elif self._comparison:
            out["map_instance_count"] = 2
        elif story_has_comparison:
            out["map_instance_count"] = 3
        else:
            out["map_instance_count"] = 1
        # Collect unique sources from layers for frontend
        source_ids = set()
        for layer in self._layers:
            source_ids.add(layer.source.id)
        sources_dict: Dict[str, Any] = {}
        for layer in self._layers:
            sid = layer.source.id
            if sid not in sources_dict:
                sources_dict[sid] = layer.source.to_dict()
        out["sources"] = sources_dict
        geojson_source_ids = [
            sid for sid, s in sources_dict.items() if s.get("type") != "vector"
        ]
        out["visibility_optimization_source_ids"] = geojson_source_ids
        if self._comparison is not None:
            out["comparison"] = self._comparison
        return out

    # ------------------------------------------------------------------
    # Output helpers
    # ------------------------------------------------------------------
    def _build_embedded_sources(self) -> Dict[str, Any]:
        """Load and optionally aggregate data for all file-based sources.

        Used when embedded=True. Returns dict source_id -> GeoJSON for
        FileSource and H3-aggregated data. Mutates H3Layer stats.
        For .geojson/.json with non-H3 layers, reads raw JSON to preserve
        all properties (e.g. time_readable) without GeoPandas roundtrip.
        """
        from .core.utils import (
            aggregate_h3,
            compute_value_stats,
            gdf_to_geojson_dict,
            load_gdf,
        )
        from .layers.h3 import H3Layer
        from .sources.file import FileSource

        embedded: Dict[str, Any] = {}
        seen: set = set()

        for layer in self._layers:
            src = layer.source
            if not isinstance(src, FileSource) or src.id in seen:
                continue
            seen.add(src.id)
            path = Path(src.path)
            suffix = path.suffix.lower()

            # GeoJSON/JSON with non-H3 layer: embed raw JSON to preserve all properties
            if suffix in (".geojson", ".json") and not isinstance(layer, H3Layer):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        geojson = json.load(f)
                    if self.use_compression:
                        from .optimizers.compression import compress_geojson_dict
                        embedded[src.id] = compress_geojson_dict(geojson)
                    else:
                        embedded[src.id] = geojson
                except (OSError, json.JSONDecodeError):
                    pass  # fall through to load_gdf if read fails
                continue

            gdf = load_gdf(src)
            if gdf is None or gdf.empty:
                continue
            if isinstance(layer, H3Layer):
                gdf = aggregate_h3(
                    gdf,
                    resolution=layer.resolution,
                    aggregation=layer.aggregation,
                    h3_column=layer.h3_column,
                    value_field=layer.property_field if layer.aggregation != "count" else None,
                )
                layer.set_stats(compute_value_stats(gdf, layer.property_field))
            geojson = gdf_to_geojson_dict(gdf)
            if self.use_compression:
                from .optimizers.compression import compress_geojson_dict
                embedded[src.id] = compress_geojson_dict(geojson)
            else:
                embedded[src.id] = geojson

        return embedded

    def to_html(self) -> str:
        """Render the map to a standalone HTML string.

        The actual HTML is produced by :mod:`llmaps.core.generator` and
        the Jinja2 templates under ``llmaps/templates/``. Import is
        local to keep import times low when only the configuration API
        is needed.
        """
        from .core.generator import render_map_html  # lazy import

        config = self.to_dict()
        if self.embedded:
            config["embedded_sources"] = self._build_embedded_sources()
        return render_map_html(
            config,
            custom_js=self._custom_js,
            custom_css=self._custom_css,
            custom_html=self._custom_html,
            user_data=self._user_data,
        )

    def save(self, path: str | Path) -> "Map":
        """Render the map and write it to *path*.

        Returns ``self`` to allow method chaining.
        """

        html = self.to_html()
        output_path = Path(path)
        output_path.write_text(html, encoding="utf-8")
        return self

    def auto_extent(
        self,
        sources: Optional[Sequence[Any]] = None,
        padding: float = 0.1,
    ) -> "Map":
        """Set center and zoom from data bounds.

        Loads geometry from all layer sources (or from *sources* if given),
        computes the combined bounding box, then sets center and zoom.
        ApiSource and VectorTile sources are skipped (no local geometry).

        Returns ``self`` for chaining.
        """
        from .core.utils import (
            bounds_center,
            bounds_to_zoom,
            load_gdf,
            aggregate_h3,
        )
        from .layers.h3 import H3Layer

        include_ids = {layer.source.id for layer in self._layers}
        if sources is not None:
            include_ids = {
                getattr(s, "id", s) for s in sources
            }

        bounds_list: List[Sequence[float]] = []
        for layer in self._layers:
            if layer.source.id not in include_ids:
                continue
            gdf = load_gdf(layer.source)
            if gdf is None or gdf.empty:
                continue
            if isinstance(layer, H3Layer):
                gdf = aggregate_h3(
                    gdf,
                    resolution=layer.resolution,
                    aggregation=layer.aggregation,
                    h3_column=layer.h3_column,
                    value_field=layer.property_field if layer.aggregation != "count" else None,
                )
            if gdf is not None and not gdf.empty:
                bounds_list.append(gdf.total_bounds)

        if not bounds_list:
            return self

        minx = min(b[0] for b in bounds_list)
        miny = min(b[1] for b in bounds_list)
        maxx = max(b[2] for b in bounds_list)
        maxy = max(b[3] for b in bounds_list)
        bounds = (minx, miny, maxx, maxy)

        self.center = bounds_center(bounds)
        self.zoom = float(bounds_to_zoom(bounds, padding=padding))
        return self

