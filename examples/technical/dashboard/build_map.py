"""Build a minimal LLMaps dashboard example."""

from pathlib import Path

from llmaps import Map
from llmaps.components import Controls, Dashboard, Legend, Popup
from llmaps.layers import CircleLayer
from llmaps.sources import FileSource


def main() -> None:
    script_dir = Path(__file__).parent
    output_path = script_dir / "map.html"
    source = FileSource(id="cities", path=str(script_dir / "data" / "cities.geojson"))

    layer = CircleLayer(
        id="cities-layer",
        source=source,
        radius=8,
        color="#0f766e",
        opacity=0.85,
        stroke_width=1,
        stroke_color="#ffffff",
    )
    dashboard = Dashboard(
        dashboard_id="overview",
        title="Map Dashboard",
        position="top-right",
        width=340,
        filters=[
            {
                "id": "period",
                "type": "select",
                "label": "Period",
                "value": "week",
                "options": [
                    {"value": "day", "label": "Day"},
                    {"value": "week", "label": "Week"},
                    {"value": "month", "label": "Month"},
                ],
            },
            {
                "id": "date",
                "type": "date",
                "label": "Snapshot date",
                "value": "2026-03-08",
            },
            {
                "id": "query",
                "type": "text",
                "label": "Quick note",
                "placeholder": "Type any label...",
                "value": "All cities",
            },
        ],
        content_html="""
<div>
  <p style=\"margin:0 0 8px;font-weight:600;\">Interactive summary</p>
  <p style=\"margin:0;color:#4b5563;line-height:1.5;\">Change a filter to update this block from custom JavaScript.</p>
</div>
""",
    )
    legend = Legend(layer_labels={"cities-layer": "Sample cities"})
    popup = Popup(fields=["name", "category"], trigger="hover")
    controls = Controls(zoom=True, scale=True)

    m = Map(
        center=[16.5, 51.2],
        zoom=4.3,
        title="LLMaps Dashboard Example",
        tiles="carto-light",
        embedded=True,
        use_compression=False,
        locale="ru-RU",
    )
    m.add_layer(layer)
    m.add_component(legend)
    m.add_component(popup)
    m.add_component(dashboard)
    m.add_component(controls)
    m.add_custom_js(
        """
window.addEventListener("llmaps:dashboard-filter-change", function(event) {
  var detail = event.detail || {};
  if (detail.dashboardId !== "overview") return;
  var state = window.llmapsDashboardGetState("overview") || {};
  var html = [
    '<div>',
    '<p style="margin:0 0 8px;font-weight:600;">Current dashboard state</p>',
    '<p style="margin:0 0 4px;color:#4b5563;">Period: ' + (state.period || '-') + '</p>',
    '<p style="margin:0 0 4px;color:#4b5563;">Snapshot date: ' + (state.date || '-') + '</p>',
    '<p style="margin:0;color:#4b5563;">Quick note: ' + (state.query || '-') + '</p>',
    '</div>'
  ].join('');
  window.llmapsDashboardSetContent("overview", html);
});
        """
    )

    m.save(output_path)
    print(f"Saved dashboard example to {output_path}")


if __name__ == "__main__":
    main()