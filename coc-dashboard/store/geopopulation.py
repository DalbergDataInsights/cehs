import geopandas as gpd
import pandas as pd
from store import Database

shapefile = gpd.read_file("./coc-dashboard/data/shapefiles/shapefile.shp")
