import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from package.elements.nested_dropdown import NestedDropdown


class DateDropdownLayout:
    def __init__(
        self, options, from_default="", to_default="", title="SELECT ANALYSIS TIMEFRAME"
    ):
        self.from_date = NestedDropdown(
            id="date_from", options=options, visible_id=False, value=from_default
        )
        self.to_date = NestedDropdown(
            id="date_to", options=options, visible_id=False, value=to_default
        )
        self.title = title
        self.callbacks = []

    @property
    def layout(self):
        return dbc.Col(self.get_layout())

    def get_layout(self):
        layout = [
            dbc.Row(
                dbc.Col(
                    html.P(
                        [self.title],
                        className="text-left",
                        style={
                            "border-bottom": "0.5px solid white",
                            "margin-left": "5px",
                            "margin-right": "5px",
                            "margin-bottom": "3px",
                            "color": "white",
                            "font-size": "1.6vh",
                        },
                    ),
                    style={
                        "width": "100%",
                    },
                )
            )
            if self.title
            else None,
            dbc.Row(
                [
                    self.from_date.get_layout(),
                    dbc.Col(
                        html.Div(
                            "to", className="text-center", style={"color": "white"}
                        ),
                        style={
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "center",
                        },
                        width=2,
                    ),
                    self.to_date.get_layout(),
                ]
            ),
        ]

        return layout
