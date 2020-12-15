import dash_bootstrap_components as dbc
import dash_html_components as html
import base64


class InfoPane:

    def __init__(self, image, text):
        self.image = image
        self.text = text
        self.__layout = None

    @property
    def layout(self):
        self.__layout = self.get_layout()
        return self.__layout

    def get_layout(self):
        layout = dbc.Col(
            dbc.Modal(
                [
                    dbc.ModalHeader("How to use the tool"),
                    dbc.ModalBody(
                        [html.Img(
                            src=self.image,
                            style={
                                "width": "auto",
                                "height": "600px"},
                        ),
                            html.Br(),
                            html.P(self.text)
                        ],
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="info-pane__close",
                                   className="ml-auto")
                    ),
                ],
                id="info-pane",
                centered=True,
                size="xl",
            ))
        return layout

    def _requires_dropdown(self):
        return False
