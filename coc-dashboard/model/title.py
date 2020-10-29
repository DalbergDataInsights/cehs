import dash_html_components as html
import dash_bootstrap_components as dbc


class Title:

    icon_class = "material-icons align-middle"
    icon_style = {"color": "rgb(19, 52, 78)", "font-size": "6rem"}

    def __init__(self, title, subtitles, icons=None, active_dash="trends"):

        self.title = title
        self.subtitles = subtitles
        self.icons = icons or {}
        self.dash = active_dash

    @property
    def layout(self):
        return dbc.Col(self.get_layout(), id="dash-title")

    def get_subtitle(self):

        sub = self.subtitles.get(self.dash)

        layout = html.P(
            sub,
            style={"font-size": "2rem", "margin-bottom": "0", "font-weight": "bold"},
        )

        return dbc.Col(layout)

    def get_icon(self):

        icon_name = self.icons.get(self.dash)

        layout = html.Span(
            icon_name,
            className=self.icon_class,
            style=self.icon_style,
        )

        return dbc.Col(layout)

    def get_layout(self):
        layout = [
            dbc.Row(
                [
                    self.get_icon(),
                    dbc.Col(
                        [
                            dbc.Row(self.get_subtitle()),
                            dbc.Row(
                                dbc.Col(
                                    html.P(
                                        self.title,
                                        style={
                                            "font-size": "2rem",
                                            "margin-bottom": "0",
                                        },
                                    )
                                )
                            ),
                        ],
                        width=11,
                    ),
                ]
            )
        ]

        return layout

    def _requires_dropdown(self):
        return False