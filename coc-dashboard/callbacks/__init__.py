from components import (
    country_overview_scatter,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
)
from dash.dependencies import Input, Output, State
from store import (
    district_control_group,
    indicator_dropdown_group,
    outlier_policy_dropdown_group,
    reference_date,
    target_date,
)

from pprint import pprint as print

from .global_callbacks import (
    global_story_callback,
    change_titles_reporting,
    update_on_click,
    change_titles_trends,
)


from .user_interface import (
    change_page,
    menu_toggle_button,
)

callback_ids = {
    outlier_policy_dropdown_group.dropdown_ids[-1]: "value",  # Outlier policy
    indicator_dropdown_group.dropdown_ids[0]: "value",  # Indicator group
    indicator_dropdown_group.dropdown_ids[-1]: "value",  # Indicator
    reference_date.dropdown_ids[0]: "value",  # Reference date year
    reference_date.dropdown_ids[-1]: "value",  # Reference date month
    target_date.dropdown_ids[0]: "value",  # Target date year
    target_date.dropdown_ids[-1]: "value",  # Target date month
    district_control_group.dropdown_ids[-1]: "value",  # District
}

from components import (
    stacked_bar_district,
    reporting_map,
    stacked_bar_reporting_country,
)


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
                # Input("overview", "n_clicks"),
            ],
            "outputs": [
                Output("ds-paginator", "children"),
                Output("nav-buttons", "children"),
                Output("dash-title", "children"),
            ],
            "function": change_page,
        },
        # Global callbacks
        {
            "inputs": [Input(x, y) for (x, y) in callback_ids.items()],
            "outputs": [Output("ds-container", "children")],
            "function": global_story_callback,
        },
        {
            "inputs": [Input(x, y) for (x, y) in callback_ids.items()],
            "outputs": [
                Output(f"{country_overview_scatter.my_name}_title", "children"),
                Output(f"{district_overview_scatter.my_name}_title", "children"),
                Output(f"{tree_map_district.my_name}_title", "children"),
            ],
            "function": change_titles_trends,
        },
        {
            "inputs": [
                Input(
                    indicator_dropdown_group.dropdown_ids[0], "value"
                ),  # Indicator group
                Input(indicator_dropdown_group.dropdown_ids[-1], "value"),  # Indicator
                Input(target_date.dropdown_ids[0], "value"),
                Input(target_date.dropdown_ids[-1], "value"),
            ],
            "outputs": [
                Output(f"{stacked_bar_reporting_country.my_name}_title", "children"),
            ],
            "function": change_titles_reporting,
        },
        {
            "inputs": [Input(f"{tree_map_district.my_name}_figure", "clickData")],
            "outputs": [
                Output(f"{facility_scatter.my_name}_figure", "figure"),
                Output(f"{facility_scatter.my_name}_fig_title", "children"),
            ],
            "function": update_on_click,
        },
    ]

    # {
    # "inputs": ,
    # "outputs": ,
    # "function": ,
    # },

    print("==Registering callbacks==")

    for callback in callbacks:
        # print(callback)
        app.callback(
            output=callback.get("outputs", []),
            inputs=callback.get("inputs", []),
            state=callback.get("states", ()),
        )(callback.get("function"))
