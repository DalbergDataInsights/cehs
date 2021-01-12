from dash.dependencies import State
from components import (
    trends_map_compare,
    compare_map,
    trends_map_period,
    period_map,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
    stacked_bar_district,
    reporting_map_compare,
    reporting_map_period,
    stacked_bar_reporting_country,
)

from dash_extensions.enrich import Input, Output


from store import (
    district_control_group,
    indicator_dropdown_group,
    outlier_policy_dropdown_group,
)

from pprint import pprint as print

from .global_callbacks import (
    global_story_callback,
    update_on_click,
    update_trends_map_compare,
    update_trends_map_period,
    update_tree_map_district,
    update_report_map_compare,
    update_report_map_period,
)

from .user_interface import (
    change_page,
    menu_toggle_button,
    toggle_fade_info,
)


# Input(id, property), Output(id, property)
callback_ids = {
    outlier_policy_dropdown_group.dropdown_ids[-1]: "value",  # Outlier policy
    indicator_dropdown_group.dropdown_ids[-1]: "value",  # Indicator
    "Month of reference": "value",
    "Month of interest": "value",
    district_control_group.dropdown_ids[-1]: "value",  # District
}

dropdown_style = [
    "config_group",
    "config_indicator",
    "SELECT A DISTRICT",
    "Month of reference",
    "Month of interest",
]


def define_callbacks(ds):

    app = ds.app

    callbacks = [
        # Data cards
        {
            "inputs": [
                Input(id, prop)
                for id, prop in stacked_bar_district.callbacks[0].get("input")
            ],
            "outputs": [
                Output(id, prop)
                for id, prop in stacked_bar_district.callbacks[0].get("output")
            ],
            "function": stacked_bar_district.callbacks[0].get("func"),
        },
        {
            "inputs": [
                Input(id, prop)
                for id, prop in reporting_map_compare.callbacks[0].get("input")
            ],
            "outputs": [
                Output(id, prop)
                for id, prop in reporting_map_compare.callbacks[0].get("output")
            ],
            "function": reporting_map_compare.callbacks[0].get("func"),
            "group": "report-map-compare-agg-update",
        },
        {
            "inputs": [
                Input(id, prop)
                for id, prop in reporting_map_period.callbacks[0].get("input")
            ],
            "outputs": [
                Output(id, prop)
                for id, prop in reporting_map_period.callbacks[0].get("output")
            ],
            "function": reporting_map_period.callbacks[0].get("func"),
            "group": "report-map-period-agg-update",
        },
        {
            "inputs": [
                Input(id, prop)
                for id, prop in stacked_bar_reporting_country.callbacks[0].get("input")
            ],
            "outputs": [
                Output(id, prop)
                for id, prop in stacked_bar_reporting_country.callbacks[0].get("output")
            ],
            "function": stacked_bar_reporting_country.callbacks[0].get("func"),
        },
        # Global callbacks
        {
            "inputs": [Input(x, y) for (x, y) in callback_ids.items()],
            "outputs": [Output("ds-container", "children")],
            "function": global_story_callback,
        },
        # User interface
        {
            "inputs": [Input("side-nav__menu-button", "n_clicks")],
            "outputs": [
                Output("side-nav__menu-button", "style"),
                Output("side-nav__menu-button__bar1", "style"),
                Output("side-nav__menu-button__bar2", "style"),
                Output("side-nav__menu-button__bar3", "style"),
                Output("side-nav", "style"),
                Output("ds-wrapper", "className"),
            ],
            "function": menu_toggle_button,
        },
        {
            "inputs": [
                Input("trends", "n_clicks"),
                Input("reporting", "n_clicks"),
                Input("overview", "n_clicks"),
            ],
            "outputs": [
                Output("ds-paginator", "children"),
                Output("nav-buttons", "children"),
                Output("dash-title", "children"),
            ]
            + [Output(x + "_container", "className") for x in dropdown_style],
            "function": change_page,
        },
        {
            "inputs": [
                Input("main-info", "n_clicks"),
                Input("info-pane__close", "n_clicks")
            ],
            "outputs": [
                Output("info-pane", "is_open"),
            ],
            "states":[
                State("info-pane", "is_open")
            ],
            "function": toggle_fade_info,
        },
        # N-click callbacks
        {
            "inputs": [Input(f"{tree_map_district.my_name}_figure", "clickData")],
            "outputs": [
                Output(f"{facility_scatter.my_name}_figure", "figure"),
                Output(f"{facility_scatter.my_name}_fig_title", "children"),
            ],
            "function": update_on_click,
        },
        # Dropdown callbacks
        {
            "inputs": [Input("trends-map-compare-agg-dropdown", "value")],
            "outputs": [
                Output(f"{trends_map_compare.my_name}_figure", "children"),
                Output(f"{trends_map_compare.my_name}_title", "children"),
            ],
            "function": update_trends_map_compare,
            "group": "trends-map-compare-agg-update",
        },
        {
            "inputs": [Input("trends-map-period-agg-dropdown", "value")],
            "outputs": [
                Output(f"{trends_map_period.my_name}_figure", "children"),
                Output(f"{trends_map_period.my_name}_title", "children"),
            ],
            "function": update_trends_map_period,
            "group": "trends-map-period-agg-update",
        },
        {
            "inputs": [Input("treemap-agg-dropdown", "value")],
            "outputs": [
                Output(f"{tree_map_district.my_name}_figure", "figure"),
                Output(f"{tree_map_district.my_name}_fig_title", "children"),
            ],
            "function": update_tree_map_district,
            "group": "treemap-agg-update",
        },
        {
            "inputs": [Input("report-map-compare-agg-dropdown", "value")],
            "outputs": [
                Output(f"{reporting_map_compare.my_name}_figure", "figure"),
                Output(f"{reporting_map_compare.my_name}_fig_title", "children"),
            ],
            "function": update_report_map_compare,
            "group": "report-map-compare-agg-update",
        },
        {
            "inputs": [Input("report-map-period-agg-dropdown", "value")],
            "outputs": [
                Output(f"{reporting_map_period.my_name}_figure", "figure"),
                Output(f"{reporting_map_period.my_name}_fig_title", "children"),
            ],
            "function": update_report_map_period,
            "group": "report-map-period-agg-update",
        },
    ]

    print("==Registering callbacks==")

    for callback in callbacks:
        # print(callback)

        params = {
            "output": callback.get("outputs", []),
            "inputs": callback.get("inputs", []),
            "state": callback.get("states", ()),
        }

        if callback.get("group"):
            params["group"] = callback.get("group")

        # print(params)

        app.callback(**params)(callback.get("function"))

    print("==Callbacks registered==")
