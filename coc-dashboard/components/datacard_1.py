import pandas as pd
from package.layout.chart_card import ChartDataCard

from store import (
    get_sub_dfs,
    timeit,
    init_data_set,
    get_year_and_month_cols,
    DEFAULTS,
    Database,
    get_time_diff_perc,
)


@timeit
def scatter_country_plot(df):

    df_country = df.get("country")

    df_country = df_country[df_country[df_country.columns[-1]] > 0]

    df_country = get_year_and_month_cols(df_country)

    df_country = get_sub_dfs(df_country, "year", [2018, 2019, 2020], "month")

    return df_country


def get_title_country_overview(data, indicator_view_name, **controls):
    """
    get title for the first section based on a percentage calcution and the inputs
    """
    country_descrip = get_time_diff_perc(data, **controls)

    title = f"""Overview: Across the country, the {indicator_view_name} {country_descrip}
            between {controls.get('reference_month')}-{controls.get('reference_year')}
            and {controls.get('target_month')}-{controls.get('target_year')} """

    return title


# DATACARD 1 #


db = Database()

# TODO The class would need to include this title function by default to avoid repetition

default_title = get_title_country_overview(
    scatter_country_plot(init_data_set),
    db.get_indicator_view(DEFAULTS.get("indicator")),
    **DEFAULTS,
)

country_overview_scatter = ChartDataCard(
    title=default_title,
    fig_title="$label$",
    data=init_data_set,
    data_transform=scatter_country_plot,
    fig_type="Scatter",
)

country_overview_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        },
        "title": "white",
        "subtitle": "rgb(34, 94, 140)",
    }
)
