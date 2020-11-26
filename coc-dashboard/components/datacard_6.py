import pandas as pd
from package.layout.map_card import MapDataCard
from package.elements.nested_dropdown import NestedDropdown

from store import timeit, init_data_set, shapefile


@timeit
def map_reporting_dated_plot(data):

    df = data.get("reporting_dated")

    data_out = {
        f"Reporting rate": df
    }

    return data_out


# DATACARD 6 #

dropdown = NestedDropdown(
    id="Select a way to compare data",
    options=["Compare month on month",
             "Compare three months moving average"])


reporting_map = MapDataCard(
    data=init_data_set,
    data_transform=map_reporting_dated_plot,
    fig_title="$label$",
    # center_value=50,
    excl_outliers_colorscale=False,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
    dropdown=dropdown
)
