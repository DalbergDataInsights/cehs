import pandas as pd
from package.layout.map_card import MapDataCard
from package.elements.nested_dropdown import NestedDropdown

from store import timeit, init_data_set, shapefile


@timeit
def map_reporting_compare_plot(data):

    df = data.get("reporting_dated_compare")

    data_out = {
        f"Reporting rate": df
    }

    return data_out


# DATACARD 6 #

dropdown = NestedDropdown(
    id="report-map-compare-agg-dropdown",
    options=["Compare month on month",
             "Compare three months moving average"],
    visible_id=False)


reporting_map_compare = MapDataCard(
    data=init_data_set,
    data_transform=map_reporting_compare_plot,
    fig_title="$label$",
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
    dropdown=dropdown
)
