import pandas as pd
from model import CardLayout
from package.layout.chart_card import ChartDataCard
from package.layout.map_card import MapDataCard
from package.elements.nested_dropdown import NestedDropdown
from store import shapefile, init_data_set, timeit


@timeit
def map_country_compare_plot(data):

    data = data.get("dated_compare").copy()

    data[data.columns[-1]] = data[data.columns[-1]] * 100

    data_out = {"Change between reference and target date": data}

    return data_out


@timeit
def bar_country_compare_plot(data):

    data = data.get("dated_compare")

    data["rank"] = data[data.columns[-1]].rank(ascending=True, method="min")
    data = data[data["rank"] < 11].sort_values(by="rank")
    data.drop("rank", axis=1, inplace=True)
    data_out = {"Top/Bottom 10": data}

    return data_out


# DATACARD 2 #

dropdown = NestedDropdown(
    id="trends-map-compare-agg-dropdown",
    options=["Compare month on month", "Compare three months moving average"],
    value="Compare month on month",
    visible_id=False,
)

compare_map = MapDataCard(
    data=init_data_set,
    data_transform=map_country_compare_plot,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
)

bar_chart_ranks_bottom = ChartDataCard(
    data=init_data_set,
    data_transform=bar_country_compare_plot,
    fig_object="Bar",
    bar_mode="overlay",
    fig_orientation="h",
    trace_params={
        "textposition": "inside",
        "texttemplate": "%{x:%}",
        "marker": {"color": "rgb(211, 41, 61)"},
        "showlegend": False,
        "hoverinfo": "none",
    },
)

trends_map_compare = CardLayout(
    title="$label$",
    elements=[compare_map, bar_chart_ranks_bottom],
    dropdown=dropdown,
)
