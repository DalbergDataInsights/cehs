import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from package.elements.nested_dropdown import NestedDropdown


class MethodologySection:
    def __init__(self, **kwargs):
        self.data = kwargs.get("data", "")
        self.title = kwargs.get("title", "")

    @property
    def layout(self):
        el_layout = [
            dbc.Row(
                dbc.Col(
                    [
                        html.H6(
                            html.B(
                                x["sub_title"],
                                style={"font-size": "1rem", "text-align": "left"},
                            )
                        ),
                        html.P(
                            x["body"],
                            style={"font-size": "0.8rem", "text-align": "left"},
                        ),
                        html.Div(
                            [
                                html.P(
                                    d,
                                    style={"font-size": "0.8rem", "text-align": "left"},
                                    className="mb-1",
                                )
                                for d in x["list_data"]
                            ]
                        ),
                    ]
                )
            )
            for x in self.data
        ]

        layout = [
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H4(
                            html.B(self.title),
                            style={
                                "color": "#00000",
                                "text-align": "center",
                                "text-decoration": "underline",
                                "width": "100%",
                            },
                        )
                    )
                )
            )
        ] + el_layout

        return dbc.Col(layout)
