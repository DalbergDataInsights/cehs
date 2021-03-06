from dash import callback_context
from store import timeit
from view import ds, side_nav
from components import (
    country_overview_scatter,
    trends_map_compare,
    trends_map_period,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
    reporting_map_compare,
    reporting_map_period,
    title,
    overview,
    # grid,
    # statistics,
)
import os
from store.database import Database
from store import CONTROLS

DATABASE_URI = os.environ["HEROKU_POSTGRESQL_CYAN_URL"]

db = Database(DATABASE_URI)

init = False


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
        return not is_open
    return is_open


@timeit
def change_page(*inputs):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    clicked = "trends"
    navbar = ds.ind_elements[0]

    if "trends" in changed_id:
        ds.data_cards = [
            title,
            country_overview_scatter,
            trends_map_compare,
            trends_map_period,
            district_overview_scatter,
            tree_map_district,
            facility_scatter,
        ]
        clicked = "trends"
    elif "reporting" in changed_id:
        ds.data_cards = [
            title,
            stacked_bar_reporting_country,
            reporting_map_compare,
            reporting_map_period,
            stacked_bar_district,
        ]

        clicked = "reporting"
    elif "overview" in changed_id:
        ds.data_cards = [title, overview]
        clicked = "overview"
    title.dash = clicked

    return [
        ds.get_container(),
        side_nav.get_nav_buttons(clicked),
        title.get_layout(),
    ] + navbar.controls.get_class_names(clicked)
