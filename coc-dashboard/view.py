import os
from datetime import datetime
from pprint import pprint as print

import dash
import dash_auth
import dash_core_components as dcc
import geopandas as gpd
import pandas as pd

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

# ds = DataStory(data_cards=[overview], ind_elements=[side_nav])

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
