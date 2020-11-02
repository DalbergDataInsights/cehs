import os
from datetime import datetime
from pprint import pprint as print

import dash
import dash_auth
import dash_core_components as dcc
import geopandas as gpd
import pandas as pd

import store

from store import credentials, side_nav

from components import (
    country_overview,
    country_overview_scatter,
    district_overview_scatter,
    facility_scatter,
    tree_map_district,
    title,
)

from package.layout.data_story import DataStory

##############
#   LAYOUT   #
##############

ds = DataStory(
    data_cards=[
        title,
        country_overview_scatter,
        country_overview,
        district_overview_scatter,
        tree_map_district,
        facility_scatter,
    ],
    ind_elements=[side_nav],
)

ds.init = False

app = ds.app
app.title = "CEHS Uganda"

auth = dash_auth.BasicAuth(app, credentials)


#     This tool is used to identify data trends, from the national level to the facility level.
#     If you notice any surprising trends, make sure to check the effect of a more stringent outlier exclusion policy on that trend,
#     and explore the reporting tool to better understand whether a reporting issue could explain that trend.
#     For more details, click on the information button on the top right.""",
