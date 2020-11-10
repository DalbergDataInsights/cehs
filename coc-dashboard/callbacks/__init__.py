from components import (
    country_overview_scatter,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
    stacked_bar_district,
    reporting_map,
    stacked_bar_reporting_country,
)

from dash.dependencies import Input, Output, State

from store import (
    district_control_group,
    indicator_dropdown_group,
    outlier_policy_dropdown_group,
)

from pprint import pprint as print

from .global_callbacks import (
    global_story_callback,
    update_on_click,
)


from .user_interface import (
    change_page,
    menu_toggle_button,
)


# Input(id, property), Output(id, property)
callback_ids = {
    outlier_policy_dropdown_group.dropdown_ids[-1]: "value",  # Outlier policy
    indicator_dropdown_group.dropdown_ids[0]: "value",  # Indicator group
    indicator_dropdown_group.dropdown_ids[-1]: "value",  # Indicator
    "date_from": "value",
    "date_to": "value",
    district_control_group.dropdown_ids[-1]: "value",  # District
}


def define_callbacks(ds):

    app = ds.app

    callbacks = [
        # Global callbacks
        {
            "inputs": [Input(x, y) for (x, y) in callback_ids.items()],
            "outputs": [Output("ds-container", "children")],
            "function": global_story_callback,
        },
        # Data cards

        # TODO : change this manual step below, which results in reporting pane not updating properly

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
                Input(id, prop) for id, prop in reporting_map.callbacks[0].get("input")
            ],
            "outputs": [
                Output(id, prop)
                for id, prop in reporting_map.callbacks[0].get("output")
            ],
            "function": reporting_map.callbacks[0].get("func"),
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
            ],
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

    ]

    print("==Registering callbacks==")

    for callback in callbacks:
        # print(callback)
        app.callback(
            output=callback.get("outputs", []),
            inputs=callback.get("inputs", []),
            state=callback.get("states", ()),
        )(callback.get("function"))
