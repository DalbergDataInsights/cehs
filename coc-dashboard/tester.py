import pandas as pd
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

districts = ['ABIM', 'ADJUMANI', 'AGAGO', 'ALEBTONG', 'AMOLATAR',
             'AMUDAT', 'AMURIA', 'AMURU', 'APAC', 'ARUA', 'BUDAKA']
mock_data = [-1, -0.5, -0.6, -0.3, 0, 1, 2, 6, 9, 45, 55]
df = pd.DataFrame(index=districts, data=mock_data).reset_index()
shapefile = gpd.read_file("./coc-dashboard/data/shapefiles/shapefile.shp")


choropleth_map = go.Choroplethmapbox(
    z=df[df.columns[0]],
    geojson=shapefile,
    locations=df['index'],
    hovertemplate="%{location} <br>"
    + df.columns[0]
    + ": %{z}"
    + "<extra></extra>",
    marker_opacity=1,
    marker_line_width=1,
    colorscale='Viridis',
    zauto=True,
    zmid=0,
)

fig = go.Figure(choropleth_map)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)
