"""FileSource implementation for LLMaps."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal, Optional

from .base import BaseSource

FileFormat = Literal["geojson", "csv", "parquet"]


def _infer_format(path: Path) -> FileFormat:
    suffix = path.suffix.lower()
    if suffix in {".geojson", ".json"}:
        return "geojson"
    if suffix == ".csv":
        return "csv"
    if suffix in {".parquet", ".pq"}:
        return "parquet"
    raise ValueError(f"Cannot infer file format from extension: {suffix}")


@dataclass
class FileSource(BaseSource):
    """Simple file-based data source.

    Parameters
    ----------
    id:
        Source identifier used by layers.
    path:
        Path to the data file (GeoJSON, CSV, Parquet).
    file_format:
        Optional explicit format. If omitted, inferred from the suffix.
    """

    path: str
    file_format: Optional[FileFormat] = None

    def __post_init__(self) -> None:
        if self.file_format is None:
            self.file_format = _infer_format(Path(self.path))

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "type": "file",
                "path": self.path,
                "format": self.file_format,
            }
        )
        return base

