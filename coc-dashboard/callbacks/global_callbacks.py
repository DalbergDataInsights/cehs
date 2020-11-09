from datetime import datetime
import base64
import io
import pandas as pd

from components import (
    country_overview_scatter,
    get_title_country_overview,
    district_overview_scatter,
    get_title_district_overview,
    facility_scatter,
    get_title_district_treemap,
    stacked_bar_district,
    stacked_bar_reporting_country,
    get_title_reporting_country,
    tree_map_district,
    reporting_map,
)

from store import (
    CONTROLS,
    LAST_CONTROLS,
    define_datasets,
    timeit,
    Database,
    get_perc_description,
)

from view import ds


@timeit
def global_story_callback(*inputs):

    db = Database()

    global LAST_CONTROLS
    LAST_CONTROLS = CONTROLS.copy()

    CONTROLS["outlier"] = inputs[0]
    CONTROLS["indicator"] = inputs[2]
    CONTROLS["district"] = inputs[5]
    CONTROLS["target_year"] = inputs[4].split(" ")[1]
    CONTROLS["target_month"] = inputs[4].split(" ")[0]
    CONTROLS["reference_year"] = inputs[3].split(" ")[1]
    CONTROLS["reference_month"] = inputs[3].split(" ")[0]
    CONTROLS["indicator_group"] = inputs[1]

    db.filter_by_policy(CONTROLS["outlier"])

    df = define_datasets(controls=CONTROLS, last_controls=LAST_CONTROLS)

    ds.switch_data_set(df)

    return [ds.get_layout()]


@timeit
def change_titles_reporting(*inputs):

    controls = {}

    controls['indicator_group'] = inputs[1]
    controls['indicator'] = inputs[2]
    controls['reference_year'] = inputs[3].split(" ")[1]
    controls['reference_month'] = inputs[3].split(" ")[0]
    controls['target_year'] = inputs[4].split(" ")[1]
    controls['target_month'] = inputs[4].split(" ")[0]
    controls['district'] = inputs[5]

    db = Database()

    indicator_view_name = db.get_indicator_view(controls['indicator'],
                                                indicator_group=controls['indicator_group'])

    stacked_bar_reporting_country.title = get_title_reporting_country(stacked_bar_reporting_country.data,
                                                                      indicator_view_name,
                                                                      **controls)

    return [stacked_bar_reporting_country.title]


@timeit
def change_titles_trends(*inputs):

    # TODO GET RID OF THIS? SHouldnt the call backs be chained properly and use the CONTROLS object?

    controls = {}

    controls['indicator_group'] = inputs[1]
    controls['indicator'] = inputs[2]
    controls['reference_year'] = inputs[3].split(" ")[1]
    controls['reference_month'] = inputs[3].split(" ")[0]
    controls['target_year'] = inputs[4].split(" ")[1]
    controls['target_month'] = inputs[4].split(" ")[0]
    controls['district'] = inputs[5]

    db = Database()

    indicator_view_name = db.get_indicator_view(controls['indicator'],
                                                indicator_group=controls['indicator_group'])

    indicator_vetted = db.get_indicator_view(controls['indicator'])

    indicator_view_name_vetted = db.get_indicator_view(indicator_vetted,
                                                       indicator_group=controls['indicator_group'])

    # data = db.datasets.get('country')

    country_overview_scatter.title = get_title_country_overview(country_overview_scatter.data,
                                                                indicator_view_name,
                                                                **controls)

    district_overview_scatter.title = get_title_district_overview(district_overview_scatter.data,
                                                                  indicator_view_name,
                                                                  **controls)

    tree_map_district.title = get_title_district_treemap(indicator_view_name_vetted,
                                                         **controls)

    # TODO : delete check

    data = country_overview_scatter.data

    check = (data.get(2020).loc['Aug'].values[0]-data.get(
        2019).loc['Aug'].values[0])/data.get(2019).loc['Aug'].values[0]

    return [
        country_overview_scatter.title,
        district_overview_scatter.title,
        tree_map_district.title,
    ]


@timeit
def update_on_click(*inputs):

    inp = inputs[0]

    try:

        label = inp.get("points")[0].get("label")

        LAST_CONTROLS = CONTROLS.copy()

        CONTROLS["facility"] = label

        ds = define_datasets(controls=CONTROLS, last_controls=LAST_CONTROLS)

        facility_scatter.data = ds
        facility_scatter.figure = facility_scatter._get_figure(
            facility_scatter.data)
        facility_scatter.figure_title = (
            f"Evolution of $label$ in {label} (click on the graph above to filter)"
        )

    except Exception as e:
        print(e)

    return [facility_scatter.figure, facility_scatter.figure_title]
