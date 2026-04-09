#!/usr/bin/env python3
"""Prepare embedded geoscience palettes data for llmaps.

Usage:
    python scripts/prepare_palettes.py
    python scripts/prepare_palettes.py --input /path/to/palettes.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import urlopen

UPSTREAM_URL = "https://raw.githubusercontent.com/dominicroye/color-for-geoscience/main/app/palettes.json"
KEEP_FIELDS = [
    "id",
    "name",
    "type",
    "variable",
    "blindsafe",
    "perceptually_uniform",
    "uniformity_cv",
    "range",
    "center",
    "context",
    "also_useful",
    "colors",
]


def _load_upstream(input_path: Path | None) -> list[dict]:
    if input_path is not None:
        return json.loads(input_path.read_text(encoding="utf-8"))

    with urlopen(UPSTREAM_URL) as response:  # nosec B310
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def _prepare(data: list[dict]) -> list[dict]:
    prepared: list[dict] = []
    for item in data:
        prepared.append({key: item.get(key) for key in KEEP_FIELDS})
    return prepared


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare geoscience palettes JSON for llmaps")
    parser.add_argument("--input", type=Path, help="Path to downloaded palettes.json")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("llmaps/palettes/data/palettes.json"),
        help="Output path for prepared palettes data",
    )
    args = parser.parse_args()

    palettes = _prepare(_load_upstream(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(palettes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Prepared {len(palettes)} palettes -> {args.output}")


if __name__ == "__main__":
    main()
