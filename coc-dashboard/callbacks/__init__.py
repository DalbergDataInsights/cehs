from components import (
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
    aggregation_dropdown,
)

from pprint import pprint as print

from .global_callbacks import (
    global_story_callback,
    update_on_click,
    update_report_map_compare,
    update_tree_map_district,
)

from .user_interface import (
    change_page,
    menu_toggle_button,
)


# Input(id, property), Output(id, property)
callback_ids = {
    outlier_policy_dropdown_group.dropdown_ids[-1]: "value",  # Outlier policy
    indicator_dropdown_group.dropdown_ids[-1]: "value",  # Indicator
    "date_from": "value",
    "date_to": "value",
    district_control_group.dropdown_ids[-1]: "value",  # District
    aggregation_dropdown.dropdown_ids[0]: "value",
    # "Select a way to compare data for this indicator": "value",
    # "Select a way to aggregate data for this indicator": "value",
    # "Select a way to aggregate facility data for this indicator": "value",
    # "Select a way to compare reporting data": "value",
    # "Select a way to aggregate reporting data": "value",
}

dropdown_style = [
    "config_group",
    "config_indicator",
    "SELECT A DISTRICT",
    "aggregation_type",
    "date_from",
    "date_to",
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
            "group": "reporting-map-compare",
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
            "inputs": [Input("Select a way to compare reporting data", "value")],
            "outputs": [
                Output(f"{reporting_map_compare.my_name}_figure", "figure"),
                Output(f"{reporting_map_compare.my_name}_fig_title", "children"),
            ],
            "function": update_report_map_compare,
            "group": "reporting-map-compare",
        },
        {
            "inputs": [
                Input(
                    "treemap-agg-dropdown",
                    "value",
                )
            ],
            "outputs": [
                Output(f"{tree_map_district.my_name}_figure", "figure"),
                Output(f"{tree_map_district.my_name}_fig_title", "children"),
            ],
            "function": update_tree_map_district,
            "group": "tree-map-update",
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

        app.callback(**params)(callback.get("function"))
