from dash import callback_context
from store import download_file, timeit
from view import ds, side_nav
from components import (
    country_overview_scatter,
    country_overview,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
    reporting_map,
    # grid,
    # statistics,
)


@timeit
def menu_toggle_button(n_clicks):
    """When button is pressed, update the 3 bars of the menu button, update style of the side navbar and update the ds-container margin"""
    if n_clicks:
        side_nav.switch_button_state()
    class_name = "m-l-25vw" if side_nav.is_open else ""
    return (
        [side_nav.menu_button.get_style()]
        + side_nav.menu_button.get_menu_button_style()
        + [side_nav.get_style()]
        + [class_name]
    )


@timeit
def toggle_fade_info(n1, n2, is_open):
    if n1 or n2:
        # Button has never been clicked
        return [not is_open]
    return [is_open]


@timeit
def download_data(n_clicks):
    if n_clicks:
        print("Yes")
        href_data = download_file(dfs)

        return [href_data]
    else:
        return [None]


@timeit
def change_page(*inputs):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    clicked = "trends"

    if "trends" in changed_id:
        ds.data_cards = [
            country_overview_scatter,
            country_overview,
            district_overview_scatter,
            tree_map_district,
            facility_scatter,
        ]
        clicked = "trends"
    elif "reporting" in changed_id:
        ds.data_cards = [
            stacked_bar_reporting_country,
            reporting_map,
            stacked_bar_district,
        ]
        clicked = "reporting"
    # elif "overview" in changed_id:
    #     ds.data_cards = [statistics, grid]
    #     clicked = "overview"

    return [ds.get_container(), side_nav.get_nav_buttons(clicked)]
