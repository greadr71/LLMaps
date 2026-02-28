"""Grid diagram HTML generation for the gerrymandering example.

Builds the hypothetical 50-person population grid + vote-bar diagrams
that appear as overlays on the intro and tools scenes.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional

# ── Grid data (hypothetical 50-person example) ──
GRID_ROWS = 5
GRID_COLS = 10

# Each row: 6 blue + 4 red = 60/40 split
POPULATION = [["B"] * 6 + ["R"] * 4 for _ in range(GRID_ROWS)]

# Fair division: vertical strips of 2 columns each
# D0-D2 = all blue → B wins; D3-D4 = mixed → R wins  →  3:2
FAIR_DISTRICTS = [[c // 2 for c in range(GRID_COLS)] for _ in range(GRID_ROWS)]

# Gerrymandered: D0,D1 packed with all blue; D2-D4 grab blue+red → R wins
# D0=10B→B, D1=10B→B, D2=4B+6R→R, D3=4B+6R→R, D4=2B+8R→R  →  2:3
GERRY_DISTRICTS = [
    [0, 0, 1, 1, 2, 2, 2, 2, 2, 2],
    [0, 0, 1, 1, 2, 2, 2, 2, 3, 3],
    [0, 0, 1, 1, 3, 3, 3, 3, 3, 3],
    [0, 0, 1, 1, 3, 3, 4, 4, 4, 4],
    [0, 0, 1, 1, 4, 4, 4, 4, 4, 4],
]


def _district_centroids(districts: list[list[int]]) -> dict[int, tuple[float, float]]:
    """Compute the centroid (row, col) for each district in cell coordinates."""
    cells: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for r, row in enumerate(districts):
        for c, d in enumerate(row):
            cells[d].append((r, c))
    return {
        d: (
            sum(r for r, _ in pts) / len(pts),
            sum(c for _, c in pts) / len(pts),
        )
        for d, pts in cells.items()
    }


def build_grid_html(
    colors: list[list[str]],
    districts: Optional[list[list[int]]] = None,
    show_labels: bool = False,
    *,
    dem_color: str = "#2166ac",
    rep_color: str = "#b2182b",
) -> str:
    """Build HTML for a 5x10 grid of colored cells with optional district borders."""
    rows = len(colors)
    cols = len(colors[0])
    cells = []
    for r in range(rows):
        for c in range(cols):
            color = dem_color if colors[r][c] == "B" else rep_color
            parts = [f"background:{color}"]
            if districts is not None:
                d = districts[r][c]
                for side, dr, dc in [
                    ("top", -1, 0),
                    ("bottom", 1, 0),
                    ("left", 0, -1),
                    ("right", 0, 1),
                ]:
                    nr, nc = r + dr, c + dc
                    is_edge = (
                        nr < 0
                        or nr >= rows
                        or nc < 0
                        or nc >= cols
                        or districts[nr][nc] != d
                    )
                    if is_edge:
                        parts.append(f"border-{side}:3px solid #333")
                    else:
                        parts.append(f"border-{side}:1px solid rgba(255,255,255,0.3)")
            else:
                parts.append("border:1px solid rgba(255,255,255,0.3)")
            cells.append(f'<div class="gcell" style="{";".join(parts)}"></div>')

    grid_html = f'<div class="gerry-grid">{"".join(cells)}</div>'

    if not show_labels or districts is None:
        return grid_html

    # Add numbered district labels as overlay
    centroids = _district_centroids(districts)
    labels = []
    for d, (cr, cc) in sorted(centroids.items()):
        top_pct = (cr + 0.5) / rows * 100
        left_pct = (cc + 0.5) / cols * 100
        labels.append(
            f'<div class="district-label" style="top:{top_pct:.1f}%;left:{left_pct:.1f}%">'
            f"{d + 1}</div>"
        )
    return (
        f'<div class="grid-with-labels">'
        f'{grid_html}{"".join(labels)}'
        f"</div>"
    )


def build_overlays_html(
    dem_color: str = "#2166ac",
    rep_color: str = "#b2182b",
) -> str:
    """Build HTML for intro and tools grid diagram overlays + court cross."""
    dim_overlay_html = '<div id="map-dim-overlay" class="map-dim-overlay"></div>'
    grid_backdrop_html = '<div id="grid-overlay-backdrop" class="grid-overlay-backdrop"></div>'

    plain = build_grid_html(POPULATION, dem_color=dem_color, rep_color=rep_color)
    fair = build_grid_html(POPULATION, FAIR_DISTRICTS, dem_color=dem_color, rep_color=rep_color)
    gerry = build_grid_html(POPULATION, GERRY_DISTRICTS, dem_color=dem_color, rep_color=rep_color)

    intro_html = f"""
    <div id="grid-overlay-intro" class="grid-overlay">
      <div class="grid-container">
        <div class="grid-panel">
          <div class="grid-title">50 избирателей</div>
          {plain}
          <div class="grid-subtitle">
            <span style="color:{dem_color}">&#9632;</span> 60% синих &ensp;
            <span style="color:{rep_color}">&#9632;</span> 40% красных
          </div>
        </div>
        <div class="grid-panel">
          <div class="grid-title grid-title--fair">Честное деление</div>
          {fair}
          <div class="grid-subtitle">
            <span style="color:{dem_color}"><strong>3</strong> синих</span> &ensp;
            <span style="color:{rep_color}"><strong>2</strong> красных</span>
          </div>
        </div>
        <div class="grid-panel">
          <div class="grid-title grid-title--gerry">Джерримендеринг</div>
          {gerry}
          <div class="grid-subtitle">
            <span style="color:{dem_color}"><strong>2</strong> синих</span> &ensp;
            <span style="color:{rep_color}"><strong>3</strong> красных</span><br>
            <strong>Меньшинство побеждает!</strong>
          </div>
        </div>
      </div>
    </div>
    """

    gerry_labeled = build_grid_html(
        POPULATION, GERRY_DISTRICTS, show_labels=True,
        dem_color=dem_color, rep_color=rep_color,
    )

    # Tools overlay: gerrymandered grid + vote bars per district
    bars_data = [
        (0, 10, 0, "packing"),
        (1, 10, 0, "packing"),
        (2, 4, 6, "cracking"),
        (3, 4, 6, "cracking"),
        (4, 2, 8, "cracking"),
    ]
    bar_rows = []
    for d, blue, red, technique in bars_data:
        total = blue + red
        b_pct = blue / total * 100
        r_pct = red / total * 100
        label = "PACKING" if technique == "packing" else "CRACKING"
        bar_rows.append(f"""
        <div class="vote-bar-row">
          <div class="vote-bar-label">Округ {d + 1}</div>
          <div class="vote-bar">
            <div class="vote-bar-fill" style="width:{b_pct}%;background:{dem_color}"></div>
            <div class="vote-bar-fill" style="width:{r_pct}%;background:{rep_color}"></div>
          </div>
          <div class="vote-bar-tag vote-bar-tag--{technique}">{label}</div>
        </div>
        """)

    tools_html = f"""
    <div id="grid-overlay-tools" class="grid-overlay">
      <div class="grid-container tools-layout">
        <div class="grid-panel">
          <div class="grid-title grid-title--gerry">Те же 50 человек, те же линии</div>
          {gerry_labeled}
        </div>
        <div class="vote-bars">
          <div class="vote-bars-title">Голоса по округам:</div>
          {"".join(bar_rows)}
        </div>
      </div>
    </div>
    """

    court_html = """
    <div id="court-cross" class="court-cross-overlay">
      <svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
        <line class="court-cross-line" x1="10" y1="10" x2="90" y2="90"/>
        <line class="court-cross-line" x1="90" y1="10" x2="10" y2="90"/>
      </svg>
    </div>
    """

    return dim_overlay_html + grid_backdrop_html + intro_html + tools_html + court_html
