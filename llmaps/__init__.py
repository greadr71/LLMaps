"""LLMaps — a Python library for creating interactive web maps."""

from pathlib import Path

from .map import Map
from . import components, expressions, layers, sources, tiles

__all__ = ["Map", "components", "expressions", "layers", "sources", "tiles", "get_llm_context"]

__version__ = "1.0.2"


def get_llm_context() -> str:
    """Return the LLM context markdown (install, Quick Start, API reference) as a string.

    Use this to write a file in your project for LLM context, e.g.:

        python -c "import llmaps; open('llmaps_context.md','w').write(llmaps.get_llm_context())"

    Then in chat use @llmaps_context.md.
    """
    path = Path(__file__).parent / "LLM_CONTEXT.md"
    return path.read_text(encoding="utf-8")

