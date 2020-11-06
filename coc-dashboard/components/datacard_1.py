import pandas as pd
from package.layout.chart_card import ChartDataCard

from store import (
    get_sub_dfs,
    timeit,
    init_data_set,
    get_year_and_month_cols,
    DEFAULTS,
    Database,
)


@timeit
def scatter_country_plot(df):

    df_country = df.get("country")

    df_country = df_country[df_country[df_country.columns[-1]] > 0]

    df_country = get_year_and_month_cols(df_country)

    df_country = get_sub_dfs(df_country, "year", [2018, 2019, 2020], "month")

    return df_country


# DATACARD 1 #

db = Database()

country_overview_scatter = ChartDataCard(
    title=f"Total {db.get_indicator_view(DEFAULTS.get('default_indicator'))} across the country",
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
