"""Post-generation HTML patches for the gerrymandering story map.

Two patches remain that cannot be solved upstream:
1. Prewarm comparison maps + mobile scroll fallback
2. Keep main-map layers visible under comparison overlay
"""

from __future__ import annotations

import re
from pathlib import Path


def apply(path: Path) -> None:
    """Apply runtime patches to the generated HTML file."""
    if not path.exists():
        print(f"Warning: runtime patch skipped, file not found: {path}")
        return

    html = path.read_text(encoding="utf-8")
    original = html

    def replace_once(pattern: str, new: str, label: str) -> None:
        nonlocal html
        html, count = re.subn(pattern, new, html, count=1, flags=re.DOTALL)
        if count == 0:
            print(f"Warning: runtime patch pattern not found: {label}")

    # Patch 1: Prewarm comparison + mobile scroll fallback
    # Scrollama IntersectionObserver can miss step-enter on mobile in nested
    # scroll-snap containers. This adds a scroll-event listener as fallback
    # and prewarms the comparison infrastructure.
    replace_once(
        r"""window\.llmapsOnLayersReady\(function\(map\)\s*\{\s*storyMap = map;\s*window\.llmapsStoryMap = map;\s*initScrollama\(map\);\s*\}\);""",
        r"""        window.llmapsOnLayersReady(function(map) {
          storyMap = map;
          window.llmapsStoryMap = map;
          initScrollama(map);

          /* ── Mobile scroll fallback ──
           * IntersectionObserver (used by Scrollama) can miss step-enter
           * events on mobile touch scroll inside a nested overflow container
           * with scroll-snap. This scroll-event listener acts as a reliable
           * fallback: on every scroll tick it finds which step is closest to
           * the container midpoint and calls applyScene if the step changed.
           */
          (function() {
            var nar = document.querySelector(".llmaps-story-narrative");
            if (!nar) return;
            var lastFallbackIdx = -1;
            nar.addEventListener("scroll", function() {
              if (isJumping) return;
              var stepsEls = nar.querySelectorAll(".story-step");
              if (!stepsEls.length) return;
              var rect = nar.getBoundingClientRect();
              var mid = rect.top + rect.height * 0.5;
              var best = 0, bestDist = Infinity;
              stepsEls.forEach(function(step, i) {
                var sr = step.getBoundingClientRect();
                var d = Math.abs(sr.top + sr.height * 0.5 - mid);
                if (d < bestDist) { bestDist = d; best = i; }
              });
              if (best !== lastFallbackIdx) {
                lastFallbackIdx = best;
                applyScene(map, scenes[best], best);
              }
            }, { passive: true });
          })();

          if (storyConfig && storyConfig.hasComparison) {
            setTimeout(function() {
              ensureCompReady(function() {});
            }, 0);
          }
        });""",
        "prewarm comparison + scroll fallback after initScrollama",
    )

    # Patch 2: Keep main-map layers visible under comparison overlay
    # The library hides all layers on the main map when entering a comparison
    # scene. This project wants them to remain visible underneath.
    replace_once(
        r"""/\* Hide all layers on main map too \*/\s*allLayerIdsWithOutline\.forEach\(function\(layerId\)\s*\{\s*if \(!map\.getLayer\(layerId\)\) return;\s*map\.setLayoutProperty\(layerId, "visibility", "none"\);\s*\}\);""",
        "/* Main map layers kept visible under comparison overlay */",
        "remove early main-map hide in comparison branch",
    )

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"Applied {2} patches to {path}")
