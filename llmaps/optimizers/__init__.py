"""
Performance and UX optimizers for LLMaps.

Modules:
- compression.py: Geobuf + Gzip compression (compress_geojson, generate_decompression_js)
- visibility.py: visibility-based resource optimization (generate_visibility_optimization_js)
- multipoint.py: MULTIPOINT explosion (generate_multipoint_explosion_js)
"""

from .compression import (
    compress_geojson,
    compress_geojson_dict,
    generate_decompression_js,
)
from .visibility import generate_visibility_optimization_js
from .multipoint import generate_multipoint_explosion_js

__all__ = [
    "compress_geojson",
    "compress_geojson_dict",
    "generate_decompression_js",
    "generate_visibility_optimization_js",
    "generate_multipoint_explosion_js",
]

