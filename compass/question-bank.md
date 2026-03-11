# Compass Question Bank

Use these questions adaptively. Do not ask all questions in one run.

You must ask all questions marked `Required: Yes` before generating any code.

Each item contains:
- `ID`: stable identifier.
- `Condition`: when to ask.
- `Options`: suggested choices.
- `Default`: fallback if user skips.
- `Effect`: impact on recipe or placeholder values.

## Group 1: Data Discovery

### Q-DAT-01
- Text: Which file should I map?
- Condition: No file path provided.
- Options: GeoJSON, CSV, Parquet, API URL.
- Default: Ask for local path.
- Effect: Sets `{SOURCE_PATH}` and source type.

### Q-DAT-02
- Text: If this is CSV/Parquet, which columns are longitude and latitude?
- Condition: Tabular file without geometry object.
- Options: User-specified column names.
- Default: Try (`lon`, `lng`, `longitude`) + (`lat`, `latitude`).
- Effect: Determines whether points workflow is possible.

### Q-DAT-03
- Text: Should I ignore records with missing geometry?
- Condition: Missing or null geometry detected.
- Options: Ignore missing, keep all, stop and clean data first.
- Default: Ignore missing.
- Effect: Affects feature count and survey summary.

### Q-DAT-04
- Text: Which field should be treated as feature ID (for feature-state/highlight)?
- Condition: Choropleth/comparison/storytelling likely.
- Options: Candidate ID fields from data.
- Default: Best unique field.
- Effect: Sets `promote_id` and feature-state compatibility.

## Group 2: Visualization Intent

### Q-INT-01
- Text: What is the primary goal: explore points, compare areas, or tell a story?
- Condition: Always after survey.
- Required: Yes.
- Options: Explore, Compare, Storytelling.
- Default: Explore.
- Effect: Routes to core recipe family.

### Q-INT-02
- Text: Should marker size or color reflect a numeric value?
- Condition: Point geometry with numeric fields.
- Options: No, size only, color only, both.
- Default: No.
- Effect: `points-basic` vs `points-sized`, and expression placeholders.

### Q-INT-03
- Text: For polygons, should color represent numeric intensity or category groups?
- Condition: Polygon geometry with numeric or categorical fields.
- Options: Numeric, categorical.
- Default: Numeric when valid numeric field exists.
- Effect: `choropleth` vs `categorical` recipe.

### Q-INT-04
- Text: Are you comparing before/after datasets?
- Condition: Two files, time fields, or explicit comparison intent.
- Options: Yes, no.
- Default: No.
- Effect: Selects `comparison` recipe.

## Group 3: Layer Configuration

### Q-LYR-01
- Text: Which data field should drive styling?
- Condition: Styled recipe selected.
- Options: Numeric/categorical candidates.
- Default: First high-signal field from survey.
- Effect: Sets `{VALUE_FIELD}` or `{CATEGORY_FIELD}`.

### Q-LYR-02
- Text: Which classification method should I use for choropleth?
- Condition: Choropleth selected.
- Options: quantile, jenks, equal_interval.
- Default: quantile.
- Effect: Sets `{CLASSIFICATION_METHOD}`.

### Q-LYR-03
- Text: How many color stops should be used?
- Condition: Choropleth selected.
- Options: 4, 5, 7, custom.
- Default: 5.
- Effect: Sets `{N_STOPS}`.

### Q-LYR-04
- Text: Which H3 aggregation should I use?
- Condition: Hexagons selected.
- Options: count, sum, mean, median.
- Default: count.
- Effect: Sets `{AGGREGATION}`.

### Q-LYR-05
- Text: Which H3 resolution is appropriate?
- Condition: Hexagons selected.
- Options: 5 to 10.
- Default: 7.
- Effect: Sets `{RESOLUTION}`.

### Q-LYR-06
- Text: Which color palette should I use?
- Condition: Any styled recipe.
- Options: viridis, plasma, YlOrRd, custom hex list.
- Default: viridis for numeric, explicit map for categorical.
- Effect: Sets `{COLOR_PALETTE}` or `{COLOR_MAP}`.

## Group 4: Components

### Q-CMP-01
- Text: Do you want details on hover/click popup?
- Condition: Any recipe except pure storytelling.
- Required: Yes.
- Options: Hover popup, click popup, no popup.
- Default: Hover popup for exploratory maps.
- Effect: Configures `Popup(trigger=...)` or removes popup.

### Q-CMP-02
- Text: Do you want a sidebar for richer feature details?
- Condition: Many display fields or explicit detail request.
- Options: Yes, no.
- Default: No.
- Effect: Selects `search-sidebar` augmentation.

### Q-CMP-03
- Text: Should users be able to search by name/code?
- Condition: String identifier fields exist.
- Options: Yes, no.
- Default: Yes for POI-style data.
- Effect: Sets `{SEARCH_FIELDS}` and enables `FeatureSearch`.

### Q-CMP-04
- Text: Which fields should appear in popup/sidebar?
- Condition: Popup or sidebar enabled.
- Options: User-selected subset.
- Default: Top 5 meaningful fields.
- Effect: Sets `{DISPLAY_FIELDS}` and field labels.

### Q-CMP-05
- Text: Should I include a legend with layer labels and ramps?
- Condition: Always unless user rejects.
- Required: Yes.
- Options: Yes, no.
- Default: Yes.
- Effect: Adds/removes Legend component.

## Group 5: Style And Output

### Q-STY-01
- Text: Which basemap style do you prefer?
- Condition: Always.
- Required: Yes.
- Options: osm, carto-light, carto-dark, yandex, 2gis.
- Default: Auto by context (light for choropleth, dark for night emphasis).
- Effect: Sets map `tiles` and optional switcher behavior.

### Q-STY-02
- Text: Should map numbers be formatted using a specific locale?
- Condition: Any popup/sidebar with numeric data.
- Options: en-US, ru-RU, custom BCP 47 tag.
- Default: en-US.
- Effect: Sets `Map(locale=...)`.

### Q-STY-03
- Text: Should embedded compression stay enabled?
- Condition: Embedded file output.
- Options: Yes, no.
- Default: Yes.
- Effect: Sets `m.use_compression`.

### Q-STY-04
- Text: Do you want map extent fitted automatically to data?
- Condition: Center/zoom unknown.
- Options: Yes, no.
- Default: Yes.
- Effect: Adds `m.auto_extent()`.
