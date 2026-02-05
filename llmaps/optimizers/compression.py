"""
GeoJSON compression (Geobuf + Gzip + Base64) for LLMaps.

Reduces embedded data size in HTML when use_compression=True.
Uses Geobuf when available; falls back to minified JSON + Gzip.
"""

import base64
import gzip
import json
from pathlib import Path
from typing import Any, Dict, Union

try:
    import geobuf
    GEOBUF_AVAILABLE = True
except ImportError:
    GEOBUF_AVAILABLE = False
    geobuf = None


def compress_geojson_dict(geojson: Dict[str, Any]) -> str:
    """
    Compress a GeoJSON dict to base64 string (Geobuf + Gzip, or JSON + Gzip).

    Parameters
    ----------
    geojson : dict
        GeoJSON FeatureCollection or compatible dict.

    Returns
    -------
    str
        Base64-encoded compressed data.
    """
    if GEOBUF_AVAILABLE and geobuf is not None:
        geobuf_bytes = geobuf.encode(geojson)
        compressed = gzip.compress(geobuf_bytes)
    else:
        json_str = json.dumps(geojson, ensure_ascii=False, separators=(",", ":"))
        compressed = gzip.compress(json_str.encode("utf-8"))
    return base64.b64encode(compressed).decode("utf-8")


def compress_geojson(source: Union[Path, str, Dict[str, Any]]) -> str:
    """
    Compress GeoJSON from path or dict to base64 string.

    Parameters
    ----------
    source : Path, str, or dict
        Path to GeoJSON file or GeoJSON dict.

    Returns
    -------
    str
        Base64-encoded compressed data.
    """
    if isinstance(source, dict):
        return compress_geojson_dict(source)
    path = Path(source)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return compress_geojson_dict(data)


def generate_decompression_js() -> str:
    """
    Generate JavaScript for decompressing base64 Geobuf/Gzip data in the browser.

    Returns
    -------
    str
        JS code defining async decompressData(compressedBase64).
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
