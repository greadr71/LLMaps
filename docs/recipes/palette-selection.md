# Recipe: Choosing geoscience palettes

Use embedded palettes from `llmaps.palettes` when generating color ramps.

## Quick rules

- Use **sequential** palettes for absolute numeric values.
- Use **diverging** palettes when values have a meaningful center (e.g. anomaly around 0).
- Use **qualitative** palettes for categorical classes.
- Prefer `blindsafe=True` palettes when possible.
- Prefer `perceptually_uniform=True` for smooth numeric gradients.

## Practical defaults

- **Choropleth on light basemap** (light background): `arctic-chill` (white→dark blue, blindsafe, PU).
- **Choropleth on dark basemap** or when shallow/low values must pop (e.g., earthquake depth, temperature): `arctic-chill` (white at low end → dark navy at high end).
- **Population density / warm intensity emphasis**: `crameri-lajolla` (cream-yellow → rich brown, blindsafe, PU).
- **Depth / elevation expert mapping**: `bathymetry` (dark blue at surface → light cyan at depth, blindsafe, PU).
- **Multi-variable generic**: `crameri-batlow` (blindsafe, perceptually smooth).

## API helpers

```python
from llmaps.palettes import list_palettes, get_palette_colors
from llmaps.expressions import compute_color_stops

# Discover palettes
candidates = list_palettes(type="sequential", blindsafe=True, perceptually_uniform=True)

# Build a ramp for map styling
stops = compute_color_stops(values, method="jenks", n_stops=7, palette="arctic-chill")

# Or assign direct color arrays (e.g. H3Layer)
colors = get_palette_colors("bathymetry", n=6)
```

## Manual visual fallback

If automatic suggestions do not match the desired visual style, pick a palette manually here:

- https://dominicroye.github.io/color-for-geoscience/
