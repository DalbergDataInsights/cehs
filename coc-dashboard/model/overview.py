from package.layout.base.data_card import DataCard
import dash_bootstrap_components as dbc
import dash_html_components as html


class Overview(DataCard):
    def __init__(self, data, **kwargs):
        super(Overview, self).__init__(data=data, **kwargs)

    def _DataCard__get_figure_layout(self):
        layout = dbc.Col(
            [
                dbc.Row(self.figure, id="overview-card"),
                # dbc.Row(self.__get_link_layout()),
            ]
        )
        return layout

    def _get_figure(self, data):
        cards = []
        df = next(iter(data.values())).reset_index()
        for row in df.iterrows():
            row_data = row[1]
            cards.append(
                IndicatorCard(
                    indicator=row_data.indicator_name,
                    values=[row_data.absolute, row_data.percentage],
                    style={"background-color": row_data.color},
                )
            )
        cards_layout = [x.get_layout() for x in cards]

        return dbc.Col(dbc.Row(cards_layout))


class IndicatorCard:
    def __init__(self, indicator, values, style):
        self.values = values
        self.indicator = indicator

        self.style = style

        # self.style["margin"] = "1em 1.6%"
        # self.style["height"] = "15vh"
        self.style["color"] = "white"
        self.style["box-shadow"] = "5px 5px 5px gray"
        self.style["border"] = f"solid rgba(0, 0, 0, 0.25)"
        self.style["text-align"] = "center"
        self.style["min-height"] = "160px"
        self.top_background = self.style.pop("background-color")
        self.bottom_background = self.top_background.split(")")[0] + ", 0.8)"
        self.style["background-color"] = self.bottom_background

    def format_number(self, number):
        number = number.split(".0")[0]
        if len(number) > 2:
            n_chars = len(number)
            for i in range(n_chars, 1, 3):
                if i != n_chars:
                    number = number[:i] + "`" + number[i:]

        return number

    def get_layout(self):
        layout = dbc.Col(
            html.Div(
                [
                    html.Div(
                        self.indicator,
                        className="p-2",
                        style={
                            "min-height": "70px",
                            "border-bottom": "solid rgba(0, 0, 0, 0.25)",
                            "background-color": self.top_background,
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "center",
                            "font-weight": "bold",
                            "font-style": "italic",
                        },
                    ),
                    html.Div(
                        self.format_number(self.values[0]),
                        className="p-2",
                        style={
                            "font-weight": "bold",
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "center",
                            "font-size": "1.2rem",
                        },
                    ),
                    html.Div(
                        self.values[1],
                        className="p-2",
                        style={
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "center",
                        },
                    ),
                ],
                style=self.style,
                className="d-flex flex-column mb-3",
            ),
            width=3,
        )

        # dbc.Col(
        #     [
        #         dbc.Row(
        #             html.Div(
        #                 self.indicator,
        #                 style={"margin": "7% auto"},
        #                 className="overview-title",
        #             ),
        #             style={"font-size": "1vw", "text-align": "center", "height": "30%"},
        #             className="overview-title-container",
        #         ),
        #         html.Div(
        #             [
        #                 dbc.Row(
        #                     dbc.Col(
        #                         self.values[0],
        #                         className="value",
        #                         style={"padding": "0"},
        #                     ),
        #                 ),
        #                 dbc.Row(
        #                     dbc.Col(
        #                         self.values[1],
        #                         className="value",
        #                         style={"padding": "0"},
        #                     ),
        #                 ),
        #             ],
        #             style={
        #                 "margin": "0 auto",
        #                 "font-size": "1.8vh",
        #                 "text-align": "center",
        #                 "font-weight": "bold",
        #                 "height": "70%",
        #             },
        #             className="value-container",
        #         ),
        #     ],
        #     width=2,
        #     style=self.style,
        #     className="overview-card",
        # )
        return layout