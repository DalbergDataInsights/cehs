import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from package.elements.nested_dropdown import NestedDropdown


class DateDropdownLayout:
    def __init__(self, options):
        self.from_date = NestedDropdown(
            id="date_from", options=options, visible_id=False
        )
        self.to_date = NestedDropdown(id="date_to", options=options, visible_id=False)
        self.callbacks = []

    @property
    def layout(self):
        return dbc.Col(self.get_layout())

    def get_layout(self):
        layout = dbc.Row(
            [
                self.from_date.get_layout(),
                dbc.Col(
                    html.Div("to", className="text-center", style={"color": "white"}),
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                    width=2,
                ),
                self.to_date.get_layout(),
            ]
        )

        return layout
