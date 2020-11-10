import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from sqlalchemy.util.langhelpers import wrap_callable


class MenuButton:

    container_style = {
        "position": "fixed",
        "top": "5px",
        "left": "0.5vw",
        "cursor": "pointer",
        "display": "inline-block",
        "transition": "0.5s",
        "z-index": "2",
    }

    bar_style = {
        "width": "1.7vw",
        "height": "5px",
        "background-color": "rgb(34, 94, 140)",
        "margin": "6px 0",
        "transition": "0.5s",
    }

    bar_transition = [
        {
            "-webkit-transform": "rotate(-45deg) translate(-9px, 6px)",
            "transform": "rotate(-45deg) translate(-9px, 6px)",
        },
        {"opacity": "0"},
        {
            "-webkit-transform": "rotate(45deg) translate(-8px, -8px)",
            "transform": "rotate(45deg) translate(-8px, -8px)",
        },
    ]

    def __init__(self):
        self.is_open = False

    def switch_button_state(self):
        self.is_open = not self.is_open

    def get_style(self):
        style = self.container_style.copy()
        if self.is_open:
            style["left"] = "20.5vw"
        return style

    def get_menu_button_style(self):

        menu_bar_style = []

        if self.is_open:
            for bar_style in self.bar_transition:
                menu_bar_style.append({**self.bar_style, **bar_style})
        else:
            menu_bar_style = 3 * [self.bar_style]

        return menu_bar_style

    def get_layout(self):
        menu_bar_style = self.get_menu_button_style()

        layout = html.Div(
            [
                html.Div(id="side-nav__menu-button__bar1", style=menu_bar_style[0]),
                html.Div(id="side-nav__menu-button__bar2", style=menu_bar_style[1]),
                html.Div(id="side-nav__menu-button__bar3", style=menu_bar_style[2]),
            ],
            style=self.get_style(),
            id="side-nav__menu-button",
        )

        return layout


class Controls:
    def __init__(self, elements):
        self.el_layout = [dbc.Row(x.layout, style={"margin": "0"}) for x in elements]

    def get_layout(self):
        layout = dbc.Col(self.el_layout)
        return layout


class SideNav:

    icon_class = "material-icons align-middle"
    icon_style = {"color": "white", "font-size": "1.5rem"}

    style = {
        "height": "100%",
        "width": "0",
        "position": "fixed",
        "z-index": "1",
        "top": "0",
        "left": "0",
        "background-color": "rgb(34, 94, 140)",
        "overflow-x": "hidden",
        "transition": "0.5s",
    }

    def __init__(self, elements, info=None):
        self.elements = elements
        self.active = "trends"
        self.callbacks = []
        self.is_open = False
        self.info = info
        self.controls = Controls(elements)
        self.menu_button = MenuButton()

        self.trends_info = ""
        self.datarep_info = ""
        self.overview_info = ""

        for els in elements:
            self.callbacks.extend(els.callbacks)

    @property
    def layout(self):
        layout = html.Div(
            [self.get_layout(), self.menu_button.get_layout()],
            id="side-nav__container",
        )

        return layout

    def get_style(self):
        style = self.style.copy()
        if self.is_open:
            style["width"] = "20vw"

        return style

    def switch_button_state(self):
        self.menu_button.is_open = not self.menu_button.is_open
        self.is_open = not self.is_open

    def get_tooltip(self, info, id, icon=True):
        tooltip = [
            html.Span(
                "info",
                className=self.icon_class,
                style={**self.icon_style, "float": "right", "cursor": "help"},
                id=f"{id}",
            )
            if icon
            else None,
            dbc.Tooltip(
                info,
                target=f"{id}",
                placement="left-end",
                autohide=False,
            ),
        ]
        return tooltip

    def get_layout(self):

        side_nav = html.Div(
            [
                html.Div(
                    [
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.P(
                                        ["CEHS APP DASHBOARDS "]
                                        + self.get_tooltip(self.info, "main-info"),
                                        style={
                                            "color": "white",
                                            "font-size": "1.9vh",
                                            "font-weight": "100",
                                            "width": "80%",
                                            "height": "4vh",
                                            "margin": "0 auto",
                                        },
                                        className="text-left",
                                    ),
                                ],
                                align="center",
                            )
                        ),
                        dbc.Row(self.get_nav_buttons(), id="nav-buttons"),
                    ],
                    style={
                        "background-color": "rgb(19, 52, 78)",
                        "padding-top": "2vh",
                        "padding-bottom": "2vh",
                    },
                ),
                dbc.Row(self.controls.get_layout()),
                dbc.Row(
                    dbc.Col(
                        dcc.Link(
                            children="Dalberg Data Insights - Contact Us",
                            href="mailto:ddi_support@dalberg.com",
                            style={"color": "white"},
                        ),
                        style={
                            "text-align": "center",
                        },
                    ),
                    style={
                        "position": "absolute",
                        "bottom": "5px",
                        "right": "5px",
                        "width": "100%",
                    },
                ),
            ],
            style=self.get_style(),
            id="side-nav",
            className="shadow-sm",
        )

        return side_nav

    def _requires_dropdown(self):
        return True

    def get_nav_buttons(self, active="trends"):
        self.active = active

        active_style = "nav-element active text-left"
        passive_style = "nav-element text-left"

        wrapper_style = {
            "width": "80%",
        }

        buttons = [
            dbc.Row(
                dbc.Col(
                    html.P(
                        [
                            html.Span(
                                "language",
                                className=self.icon_class,
                                style=self.icon_style,
                            ),
                            " Overview",
                        ]
                        + self.get_tooltip(
                            self.overview_info, "overview-info", icon=False
                        ),
                        id="overview",
                        className=active_style
                        if active == "overview"
                        else passive_style,
                    ),
                    style=wrapper_style,
                ),
                id="overview-info",
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        [
                            html.Span(
                                "analytics",
                                className=self.icon_class,
                                style=self.icon_style,
                            ),
                            " Trends",
                        ]
                        + self.get_tooltip(self.trends_info, "trends-info", icon=False),
                        id="trends",
                        className=active_style if active == "trends" else passive_style,
                    ),
                    style=wrapper_style,
                ),
                id="trends-info",
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        [
                            html.Span(
                                "center_focus_weak",
                                className=self.icon_class,
                                style=self.icon_style,
                            ),
                            " Data quality",
                        ]
                        + self.get_tooltip(
                            self.datarep_info, "reporting-info", icon=False
                        ),
                        id="reporting",
                        className=active_style
                        if active == "reporting"
                        else passive_style,
                    ),
                    style=wrapper_style,
                ),
                id="reporting-info",
            ),
        ]

        layout = dbc.Col(buttons, align="center")

        return layout
