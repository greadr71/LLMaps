"""
GeoJSON compression (Geobuf + Gzip + Base64) for LLMaps.

Reduces embedded data size in HTML when use_compression=True.
Uses Geobuf for efficient binary compression.
"""

import base64
import gzip
import json
import logging
from pathlib import Path
from typing import Any, Dict, Union

logger = logging.getLogger(__name__)

try:
    import geobuf
except ImportError as e:
    raise ImportError(
        "geobuf is required for compression in llmaps. "
        "Install with: pip install 'llmaps' or pip install 'geobuf>=2.1'"
    ) from e


def compress_geojson_dict(geojson: Dict[str, Any]) -> str:
    """
    Compress a GeoJSON dict to base64 string (Geobuf + Gzip).

    Parameters
    ----------
    geojson : dict
        GeoJSON FeatureCollection or compatible dict.

    Returns
    -------
    str
        Base64-encoded compressed data (Geobuf encoded and gzipped).
    """
    geobuf_bytes = geobuf.encode(geojson)
    compressed = gzip.compress(geobuf_bytes)
    result = base64.b64encode(compressed).decode("utf-8")
    logger.debug(f"GeoJSON compressed with Geobuf+Gzip: {len(geojson)} features → {len(result)} bytes (base64)")
    return result


def compress_geojson(source: Union[Path, str, Dict[str, Any]]) -> str:
    """
    Compress GeoJSON from path or dict to base64 string (Geobuf + Gzip).

    Parameters
    ----------
    source : Path, str, or dict
        Path to GeoJSON file or GeoJSON dict.

    Returns
    -------
    str
        Base64-encoded compressed data (Geobuf encoded and gzipped).
    """
    if isinstance(source, dict):
        return compress_geojson_dict(source)
    path = Path(source)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return compress_geojson_dict(data)


def generate_decompression_js() -> str:
    """
    Generate JavaScript for decompressing base64 Geobuf+Gzip data in the browser.

    Returns
    -------
    str
        JS code defining async decompressData(compressedBase64) function.
        Includes fallback to JSON parsing if geobuf.js not available in browser.
    """
    return r"""      async function decompressData(compressedBase64) {
        if (!compressedBase64) return null;
        if (typeof compressedBase64 !== "string") return compressedBase64;
        try {
          const binaryString = atob(compressedBase64);
          const len = binaryString.length;
          const bytes = new Uint8Array(len);
          for (let i = 0; i < len; i++) bytes[i] = binaryString.charCodeAt(i);
          const decompressedBytes = pako.inflate(bytes);
          const geobufAvailable = typeof geobuf !== "undefined" && typeof geobuf.decode === "function" && typeof Pbf !== "undefined";
          const firstByte = decompressedBytes[0];
          const isLikelyJSON = firstByte === 0x7B || firstByte === 0x5B;
          if (geobufAvailable && !isLikelyJSON) {
            try {
              const pbf = new Pbf(decompressedBytes);
              return geobuf.decode(pbf);
            } catch (e) {
              const jsonString = new TextDecoder("utf-8").decode(decompressedBytes);
              return JSON.parse(jsonString);
            }
          }
          const jsonString = new TextDecoder("utf-8").decode(decompressedBytes);
          return JSON.parse(jsonString);
        } catch (error) {
          console.error("LLMaps decompression error:", error);
          throw error;
        }
      }"""
