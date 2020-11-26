from store import (timeit,
                   reporting_count_transform,
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


def get_title_reporting_country(data, indicator_view_name, **controls):
    """
    get title for the reporting section based on a percentage calculation and the inputs
    """
    descrip_reported, descrip_positive = get_report_perc(data, **controls)

    title = f'''Reporting: {controls.get('target_month')}-{controls.get('target_year')}, 
            {descrip_reported} of facilities reported on their 105:1 form, and, out of those, 
            {descrip_positive} reported for {indicator_view_name}'''

    return title

# DATACARD 5 #


db = Database()

default_title = get_title_reporting_country(bar_reporting_country_plot(init_data_set),
                                            db.get_indicator_view(
                                                DEFAULTS.get('indicator')),
                                            **DEFAULTS)

stacked_bar_reporting_country = ChartDataCard(
    data=init_data_set,
    data_transform=bar_reporting_country_plot,
    title=default_title,
    fig_title="$label$",
    fig_object="Bar",
)

stacked_bar_reporting_country.set_colors(
    {"fig": ["rgb(42, 87, 131)", "rgb(247, 190, 178)", "rgb(211, 41, 61)"]}
)
