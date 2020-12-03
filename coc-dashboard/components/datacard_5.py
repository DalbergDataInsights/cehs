from store import (timeit,
                   reporting_count_transform,
                   reporting_count_transform_tooltip,
                   init_data_set,
                   get_report_perc,
                   DEFAULTS,
                   Database)

from package.layout.chart_card import ChartDataCard


@timeit
def bar_reporting_country_plot(data):

    data_in = data.get("reporting_country")
    data_out = reporting_count_transform(data_in.copy())

    return data_out


@timeit
def bar_reporting_country_plot_tooltip(data):

    data_in = data.get("reporting_country")
    data_out = reporting_count_transform_tooltip(data_in.copy())

    return data_out


def get_title_reporting_country(data, indicator_view_name, **controls):
    """
    get title for the reporting section based on a percentage calculation and the inputs
    """
    descrip_reported, descrip_positive = get_report_perc(data, **controls)

    title = f'''Reporting: on {controls.get('target_month')}-{controls.get('target_year')},
            {descrip_reported} of facilities reported on their 105:1 form, and, out of those,
            {descrip_positive} reported one or above for {indicator_view_name}'''

    return title

# DATACARD 5 #


db = Database()

default_title = get_title_reporting_country(bar_reporting_country_plot(init_data_set),
                                            db.get_indicator_view(
                                                DEFAULTS.get('indicator')),
                                            **DEFAULTS)

customdata = [bar_reporting_country_plot_tooltip(init_data_set).get('Reported one or above for selected indicator').iloc[:, -1:],


stacked_bar_reporting_country= ChartDataCard(
    data=init_data_set,
    data_transform=bar_reporting_country_plot,
    title=default_title,
    fig_title="$label$",
    fig_object="Scatter",
    trace_params={
        'customdata':,
        'hovertemplate': 'test:%{customdata:.3f}'},
)

# stacked_bar_reporting_country.set_colors(
#     {"fig": ["rgb(42, 87, 131)", "rgb(247, 190, 178)", "rgb(211, 41, 61)"]}
# )


stacked_bar_reporting_country.set_colors(
    {
        "fig": {
            "Percentage of facilities expected to report which reported on their 105-1 form": "rgb(106, 155, 195)",
            "Percentage of reporting facilities that reported a value of one or above for this indicator": "rgb(200, 19, 60)",
        },
        "title": "white",
        "subtitle": "rgb(34, 94, 140)",
    }
)
