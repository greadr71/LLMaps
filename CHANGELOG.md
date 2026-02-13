# Changelog

All notable changes to this project will be documented in this file.

## 0.1.1 - FillLayer outline fix

- **Fixed:** FillLayer now uses correct MapLibre property `fill-outline-color` instead of invalid `outline-color`/`outline-width`.
- **Added:** For `stroke_width > 1`, an additional line layer `{id}-outline` is automatically generated.
- **Docs:** Updated `docs/api/layers.md` with note about stroke_width behavior.

## 0.1.0 - Initial setup

- Project structure created.
- `pyproject.toml` added.
- MIT license and basic docs initialized.

