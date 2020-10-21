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

from .global_callbacks import united_story_callback, update_on_click
from .user_interface import (
    change_page,
    download_data,
    toggle_fade_controls,
    toggle_fade_info,
)

callback_ids = {
    outlier_policy_dropdown_group.dropdown_ids[-1]: "value",  # Outlier policy
    indicator_dropdown_group.dropdown_ids[0]: "value",  # Indicator group
    indicator_dropdown_group.dropdown_ids[-1]: "value",  # Indicator
    reference_date.dropdown_ids[0]: "value",  # Reference date year
    reference_date.dropdown_ids[-1]: "value",  # Reference date month
    target_date.dropdown_ids[0]: "value",  # Reference date year
    target_date.dropdown_ids[-1]: "value",  # Reference date month
    district_control_group.dropdown_ids[-1]: "value",  # District
}


def define_callbacks(ds):

    app = ds.app

    callbacks = [
        # User interface
        {
            "inputs": [Input("fade-button", "n_clicks")],
            "outputs": [Output("fade-controls", "is_in")],
            "function": toggle_fade_controls,
            "states": [State("fade-controls", "is_in")],
        },
        {
            "inputs": [
                Input("info-button", "n_clicks"),
                Input("info-close", "n_clicks"),
            ],
            "outputs": [Output("info-fade", "is_open")],
            "function": toggle_fade_info,
            "states": [State("info-fade", "is_open")],
        },
        # {
        #     "inputs": [Input("download-excel", "n_clicks")],
        #     "outputs": [Output("download-excel", "href")],
        #     "function": download_data,
        # },
        {
            "inputs": [
                Input("trends", "n_clicks"),
                Input("reporting", "n_clicks"),
                # Input("overview", "n_clicks"),
            ],
            "outputs": [
                Output("ds-paginator", "children"),
                Output("nav-buttons", "children"),
            ],
            "function": change_page,
        },
        # Global callbacks
        {
            "inputs": [Input(x, y) for (x, y) in callback_ids.items()],
            "outputs": [
                Output("ds-container", "children"),
                Output(f"{country_overview_scatter.my_name}_title", "children"),
                Output(f"{district_overview_scatter.my_name}_title", "children"),
                Output(
                    f"{stacked_bar_reporting_country.my_name}_title", "children"),
                Output(f"{tree_map_district.my_name}_title", "children"),
            ],
            "function": united_story_callback,
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
    #         "inputs": ,
    #         "outputs": ,
    #         "function": ,
    # },

    print("==Registering callbacks==")

    for callback in callbacks:
        # print(callback)
        app.callback(
            output=callback.get("outputs", []),
            inputs=callback.get("inputs", []),
            state=callback.get("states", ()),
        )(callback.get("function"))
