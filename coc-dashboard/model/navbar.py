import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


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
        "width": "35px",
        "height": "5px",
        "background-color": "#ddd",
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


# class Methodology:
#     def __init__(self, elements):
#         self.me_layout = [dbc.Row(x.layout) for x in elements]

#     def get_layout(self):
#         button = html.P(
#             html.Span(
#                 "info",
#                 className="material-icons",
#                 style={"color": "black", "font-size": "45px"},
#             ),
#             id="info-button",
#         )

#         modal = dbc.Modal(
#             [
#                 dbc.ModalHeader("Methodology"),
#                 dbc.ModalBody(self.me_layout),
#                 dbc.ModalFooter(
#                     dbc.Button("Close", id="info-close", className="ml-auto")
#                 ),
#             ],
#             id="info-fade",
#             centered=True,
#         )

#         layout = html.Div(
#             [button, modal],
#             style={"position": "fixed", "bottom": "5px", "right": "0.5vw"},
#         )

#         return layout


class Controls:
    def __init__(self, elements):
        self.el_layout = [dbc.Row(x.layout, style={"margin": "0"}) for x in elements]

    def get_layout(self):
        layout = dbc.Col(self.el_layout)
        return layout


# class NavButtons:
#     def __init__(self):
#         self.active = "trends"

#     @property
#     def layout(self):
#         return self.get_nav_buttons()

#     def get_nav_buttons(self, active="trends"):
#         self.active = active

#         active_style = "nav-element active"

#         buttons = dbc.Row(
#             [
#                 # dbc.Col(
#                 #     html.P(
#                 #         "Overview (coming soon)",
#                 #         id="overview",
#                 #         # active_style if active == "overview" else "nav-element",
#                 #         className="nav-element disabled",
#                 #     )
#                 # ),
#                 dbc.Col(
#                     html.P(
#                         "Trends",
#                         id="trends",
#                         className=active_style if active == "trends" else "nav-element",
#                     )
#                 ),
#                 dbc.Col(
#                     html.P(
#                         "Reporting",
#                         id="reporting",
#                         className=active_style
#                         if active == "reporting"
#                         else "nav-element",
#                     )
#                 ),
#             ],
#             style={"position": "fixed", "top": "0", "width": "20vw", "left": "40vw"},
#         )

#         return buttons

#     def _requires_dropdown(self):
#         return False


class SideNav:

    style = {
        "height": "100%",
        "width": "0",
        "position": "fixed",
        "z-index": "1",
        "top": "0",
        "left": "0",
        "background-color": "rgb(217, 214, 214)",
        "overflow-x": "hidden",
        "padding-top": "14px",
        "transition": "0.5s",
    }

    def __init__(self, elements):
        self.elements = elements
        self.active = "trends"
        self.callbacks = []
        self.is_open = False

        self.controls = Controls(elements)
        self.menu_button = MenuButton()

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

    def get_layout(self):

        side_nav = html.Div(
            [dbc.Row(self.controls.get_layout())],
            style=self.get_style(),
            id="side-nav",
            className="shadow-sm",
        )

        return side_nav

    def _requires_dropdown(self):
        return True


class TopNav:
    def __init__(self, methodology):

        self.active = "trends"
        self.methodology = methodology

        # self.methodology_modal = Methodology(methodology)

    @property
    def layout(self):
        layout = html.Div(self.get_layout(), id="topnav-container")

        return layout

    def get_nav_buttons(self, active="trends"):
        self.active = active

        active_style = "nav-element active"

        buttons = [
            # html.P(
            #     "Overview (coming soon)",
            #     id="overview",
            #     # active_style if active == "overview" else "nav-element",
            #     className="nav-element disabled",
            # ),
            html.P(
                "Trends",
                id="trends",
                className=active_style if active == "trends" else "nav-element",
            ),
            html.P(
                "Reporting",
                id="reporting",
                className=active_style if active == "reporting" else "nav-element",
            ),
        ]

        return buttons

    def get_layout(self):
        me_layout = [dbc.Row(x.layout) for x in self.methodology]

        html_nav = html.Div(
            [
                html.Div(
                    self.get_nav_buttons(), className="topnav-left", id="nav-buttons"
                ),
                html.Div(
                    [
                        html.P(
                            html.Span("cloud_download", className="material-icons"),
                            className="nav-element",
                        ),
                        html.P(
                            html.Span("info", className="material-icons"),
                            # html.I(className="fas fa-info-circle"),
                            className="nav-element",
                            id="info-button",
                        ),
                    ],
                    className="topnav-right",
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Methodology"),
                        dbc.ModalBody(me_layout),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="info-close", className="ml-auto")
                        ),
                    ],
                    id="info-fade",
                    centered=True,
                ),
            ],
            className="topnav",
        )

        return html_nav

    def _requires_dropdown(self):
        return False