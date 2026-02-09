"""Tile provider presets for LLMaps.

The goal of this module is to provide a small set of named presets that
are easy to use from Python while remaining explicit about attribution.
"""

from __future__ import annotations

from typing import Any, Dict


_TILE_PRESETS: Dict[str, Dict[str, Any]] = {
    "osm": {
        "id": "osm",
        "name": "OpenStreetMap",
        "url_template": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "subdomains": ["a", "b", "c"],
        "attribution": "© OpenStreetMap contributors",
    },
    "carto-light": {
        "id": "carto-light",
        "name": "Carto Light",
        "url_template": "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
        "subdomains": ["a", "b", "c", "d"],
        "attribution": "© OpenStreetMap contributors, © CARTO",
    },
    "carto-dark": {
        "id": "carto-dark",
        "name": "Carto Dark",
        "url_template": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
        "subdomains": ["a", "b", "c", "d"],
        "attribution": "© OpenStreetMap contributors, © CARTO",
    },
    # Yandex and 2GIS
    "yandex": {
        "id": "yandex",
        "name": "Yandex Maps",
        "url_template": "https://core-renderer-tiles.maps.yandex.net/tiles?l=map&x={x}&y={y}&z={z}&lang=ru_RU&projection=web_mercator&scale=4",
        "subdomains": [],
        "attribution": "© Yandex Maps",
    },
    "2gis": {
        "id": "2gis",
        "name": "2GIS",
        "url_template": "https://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}&v=1.1",
        "subdomains": [],
        "attribution": "© 2GIS",
    },
}


def resolve_tile_provider(name: str) -> Dict[str, Any]:
    """Return configuration dict for a tile provider by *name*.

    Parameters
    ----------
    name:
        Provider identifier such as ``"osm"`` or ``"carto-dark"``.
    """

    try:
        return _TILE_PRESETS[name]
    except KeyError as exc:
        raise KeyError(f"Unknown tile provider: {name!r}") from exc


def list_tile_providers() -> Dict[str, Dict[str, Any]]:
    """Return a copy of all registered tile providers."""

    return dict(_TILE_PRESETS)

