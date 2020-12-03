import pandas as pd
from model import CardLayout
from package.layout.chart_card import ChartDataCard
from package.layout.map_card import MapDataCard
from package.elements.nested_dropdown import NestedDropdown
from store import shapefile, init_data_set, timeit


@timeit
def map_country_dated_plot(data):

    data = data.get("dated_period")

    data_out = {"Overview between reference and target date": data}

    return data_out


@timeit
def bar_country_dated_plot(data):

    data = data.get("dated_period")

    data["rank"] = data[data.columns[-1]].rank(ascending=True, method="min")
    data = data[data["rank"] < 11].sort_values(by="rank")
    data.drop("rank", axis=1, inplace=True)
    data_out = {"Top/Bottom 10": data}

    return data_out


# DATACARD 2 #

dropdown = NestedDropdown(
    id="trends-map-period-agg-dropdown",
    options=[
        "Show only month of interest",
        "Show sum over period",
        "Show average over period",
    ],
    value="Show only month of interest",
    visible_id=False,
)

period_map = MapDataCard(
    data=init_data_set,
    data_transform=map_country_dated_plot,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
)

bar_chart_ranks_bottom = ChartDataCard(
    data=init_data_set,
    data_transform=bar_country_dated_plot,
    fig_object="Bar",
    fig_orientation="h",
    trace_params={
        "textposition": "inside",
        "texttemplate": "%{x:,.0}",
        "marker": {"color": "rgb(184, 190, 200)"},
        "showlegend": False,
        "hoverinfo": "none",
    },
)

trends_map_period = CardLayout(
    title="$label$",
    elements=[period_map, bar_chart_ranks_bottom],
    dropdown=dropdown,
)
