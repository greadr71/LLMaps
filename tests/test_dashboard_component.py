from llmaps import Map
from llmaps.components import Dashboard


def test_dashboard_to_dict_serializes_filters_and_content():
    dashboard = Dashboard(
        dashboard_id="analytics",
        position="bottom-left",
        title="Analytics",
        width=420,
        height=500,
        collapsed=True,
        filters=[
            {
                "id": "period",
                "type": "select",
                "label": "Period",
                "value": "week",
                "options": ["day", "week", "month"],
            },
            {
                "id": "start_date",
                "type": "date",
                "label": "Start date",
                "value": "2026-03-01",
            },
        ],
        content_html="<strong>Ready</strong>",
    )

    data = dashboard.to_dict()

    assert data["type"] == "dashboard"
    assert data["dashboard_id"] == "analytics"
    assert data["position"] == "bottom-left"
    assert data["width"] == 420
    assert data["height"] == 500
    assert data["collapsed"] is True
    assert data["filters"][0]["id"] == "period"
    assert data["filters"][1]["type"] == "date"
    assert data["content_html"] == "<strong>Ready</strong>"


def test_dashboard_defaults_are_explicit_and_serializable():
    dashboard = Dashboard()

    data = dashboard.to_dict()

    assert data == {
        "type": "dashboard",
        "dashboard_id": "dashboard",
        "position": "top-right",
        "title": None,
        "width": 360,
        "height": None,
        "collapsible": True,
        "collapsed": False,
        "filters": [],
        "content_html": "",
        "empty_state": "No dashboard content yet.",
    }


def test_dashboard_date_filter_uses_map_locale_in_rendered_html():
    dashboard = Dashboard(
        filters=[
            {
                "id": "snapshot_date",
                "type": "date",
                "label": "Snapshot date",
                "value": "2026-03-08",
            }
        ]
    )
    map_obj = Map(center=[0, 0], locale="en-US", embedded=False, use_compression=False)
    map_obj.add_component(dashboard)

    html = map_obj.to_html()

    assert '<html lang="en-US">' in html
    assert 'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css' in html
    assert 'window.flatpickr(input, {' in html
    assert 'locale: dashboardResolveDateLocale(),' in html