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

        self.style["margin"] = "1em 1.6%"
        self.style["height"] = "15vh"
        self.style["color"] = "white"
        self.style["box-shadow"] = "0 20px 50px rgba(0,0,0,0.6)"

        # self.style["padding-left"] = "20px"
        # self.style["padding-right"] = "20px"
        # self.style["opacity"] = "0.75"

    def get_layout(self):
        layout = dbc.Col(
            [
                dbc.Row(
                    html.Div(
                        self.indicator,
                        style={"margin": "7% auto"},
                        className="overview-title",
                    ),
                    style={"font-size": "1vw", "text-align": "center"},
                    className="overview-title-container",
                ),
                dbc.Row(
                    dbc.Col(self.values[0], className="value", style={"padding": "0"}),
                    style={
                        "margin": "0 auto",
                        "font-size": "1.1vw",
                        "text-align": "center",
                        "font-weight": "bold",
                    },
                    className="value-container",
                ),
                dbc.Row(
                    dbc.Col(self.values[1], className="value", style={"padding": "0"}),
                    style={
                        "margin": "0 auto",
                        "font-size": "1.1vw",
                        "text-align": "center",
                        "font-weight": "bold",
                    },
                    className="value-container",
                ),
            ],
            width=2,
            style=self.style,
            className="overview-card",
        )
        return layout