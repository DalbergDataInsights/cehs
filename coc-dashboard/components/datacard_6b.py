import pandas as pd
from package.layout.map_card import MapDataCard
from package.elements.nested_dropdown import NestedDropdown

from store import timeit, init_data_set, shapefile


@timeit
def map_reporting_period_plot(data):

    df = data.get("reporting_dated_period")

    data_out = {
        f"Reporting rate": df
    }

    return data_out


# DATACARD 6 #

dropdown = NestedDropdown(
    id="Select a way to aggregate data",
    options=["Show only month of interest",
             "Show average over period"])

reporting_map_period = MapDataCard(
    data=init_data_set,
    data_transform=map_reporting_period_plot,
    fig_title="$label$",
    center_value=50,
    excl_outliers_colorscale=False,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
    dropdown=dropdown
)
