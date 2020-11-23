import pandas as pd
from package.layout.map_card import MapDataCard

from store import check_index, timeit, init_data_set, shapefile


@timeit
def map_reporting_dated_plot(data):

    df = data.get("reporting_dated")

    data_out = {
        f"Reporting rate": df
    }

    return data_out


# DATACARD 6 #

reporting_map = MapDataCard(
    data=init_data_set,
    data_transform=map_reporting_dated_plot,
    fig_title="$label$",
    center_value=50,
    excl_outliers_colorscale=False,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
)
