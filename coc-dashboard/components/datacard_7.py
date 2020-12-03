from store import reporting_count_transform, reporting_count_transform_tooltip, timeit, init_data_set
from package.layout.chart_card import ChartDataCard


@timeit
def scatter_reporting_district_plot(data):

    data_in = data.get("reporting_district")
    data_out = reporting_count_transform(data_in.copy())

    return data_out


@timeit
def scatter_reporting_district_plot_tooltip(data):

    data_in = data.get("reporting_district")
    data_out = reporting_count_transform_tooltip(data_in.copy())

    return data_out


# DATACARD 7 #


stacked_bar_district = ChartDataCard(
    data=init_data_set,
    data_transform=scatter_reporting_district_plot,
    fig_title="$label$",
    fig_object="Scatter",
    trace_params=scatter_reporting_district_plot_tooltip(init_data_set),
)


stacked_bar_district.set_colors(
    {
        "fig": {
            "Percentage of facilities expected to report which reported on their 105-1 form": "rgb(106, 155, 195)",
            "Percentage of reporting facilities that reported a value of one or above for this indicator": "rgb(200, 19, 60)",
        },
        "title": "white",
        "subtitle": "rgb(34, 94, 140)",
    }
)
