import pandas as pd
from package.layout.chart_card import ChartDataCard

from store import (
    get_sub_dfs,
    timeit,
    init_data_set,
    get_year_and_month_cols,
    get_time_diff_perc,
    DEFAULTS,
    Database,
)


from package.layout.chart_card import ChartDataCard


@timeit
def scatter_district_plot(df):

    df_district = df.get("district")

    df_district = df_district[df_district[df_district.columns[-1]] > 0]

    df_district = get_year_and_month_cols(df_district)

    df_district = get_sub_dfs(df_district, "year", [2018, 2019, 2020], "month")

    return df_district


def get_title_district_overview(data, indicator_view_name, **controls):
    """
    get title for the second section based on a percentage calcution and the inputs
    """
    district_descrip = get_time_diff_perc(data, **controls)

    title = f'''Deep-dive in {controls.get('district')} district: the {indicator_view_name} {district_descrip} 
            between {controls.get('reference_month')}-{controls.get('reference_year')} 
            and {controls.get('target_month')}-{controls.get('target_year')} '''

    return title


# DATACARD 3 #

db = Database()

default_title = get_title_district_overview(scatter_district_plot(init_data_set),
                                            db.get_indicator_view(
                                                DEFAULTS.get('indicator')),
                                            **DEFAULTS)

district_overview_scatter = ChartDataCard(
    title=default_title,
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
