import pandas as pd
from package.layout.chart_card import ChartDataCard

from store import (
    get_sub_dfs,
    timeit,
    init_data_set,
    get_year_and_month_cols,
)


from package.layout.chart_card import ChartDataCard


@timeit
def scatter_district_plot(df):

    df_district = df.get("district")

    df_district = df_district[df_district[df_district.columns[-1]] > 0]

    df_district = get_year_and_month_cols(df_district)

    df_district = get_sub_dfs(df_district, "year", [2018, 2019, 2020], "month")

    return df_district


# DATACARD 3 #


district_overview_scatter = ChartDataCard(
    title="dummy",
    fig_title="$label$",
    data=init_data_set,
    data_transform=scatter_district_plot,
    fig_type="Scatter",
)

district_overview_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        }
    }
)
