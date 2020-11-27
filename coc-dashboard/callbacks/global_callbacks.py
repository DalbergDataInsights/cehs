from datetime import datetime
import time
import base64
import io
import pandas as pd

from components import (
    country_overview_scatter,
    get_title_country_overview,
    country_overview_compare,
    country_overview_period,
    district_overview_scatter,
    get_title_district_overview,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    get_title_reporting_country,
    tree_map_district,
    reporting_map_compare,
    reporting_map_period,
    overview,
    overview,
)

from store import (
    CONTROLS,
    LAST_CONTROLS,
    define_datasets,
    timeit,
    Database,
)

from view import ds


@timeit
def global_story_callback(*inputs):

    db = Database()

    try:

        global LAST_CONTROLS
        LAST_CONTROLS = CONTROLS.copy()

        CONTROLS["outlier"] = inputs[0]
        CONTROLS["indicator"] = inputs[1]
        CONTROLS["district"] = inputs[4]
        CONTROLS["target_year"] = inputs[3].split(" ")[1]
        CONTROLS["target_month"] = inputs[3].split(" ")[0]
        CONTROLS["reference_year"] = inputs[2].split(" ")[1]
        CONTROLS["reference_month"] = inputs[2].split(" ")[0]
        CONTROLS["aggregation_type"] = inputs[5]
        CONTROLS["trends_map_compare_agg"] = inputs[6]
        CONTROLS["trends_map_period_agg"] = inputs[7]
        CONTROLS["trends_treemap_agg"] = inputs[8]
        # CONTROLS["report_map_compare_agg"] = inputs[9]
        # CONTROLS["report_map_period_agg"] = inputs[10]

        db.filter_by_policy(CONTROLS["outlier"])

        df = define_datasets(controls=CONTROLS, last_controls=LAST_CONTROLS)

        for x in [country_overview_scatter,
                  country_overview_compare,
                  country_overview_period,
                  district_overview_scatter,
                  facility_scatter,
                  stacked_bar_district,
                  stacked_bar_reporting_country,
                  tree_map_district,
                  reporting_map_compare,
                  reporting_map_period,
                  overview]:
            try:
                x.data = df
            except Exception as e:
                print(e)

        print(f"Datasets updated for {CONTROLS['indicator']}")
    except:
        print(f"Error updating global callback for {CONTROLS['indicator']}")

    indicator_view = db.get_indicator_view(CONTROLS["indicator"])

    indicator_view_if_ratio = db.get_indicator_view(
        db.switch_indic_to_numerator(CONTROLS["indicator"], popcheck=False)
    )

    try:
        change_titles_reporting(indicator_view_if_ratio, CONTROLS)

    except:
        print(f"Error updating reporting title for {CONTROLS['indicator']}")

    try:
        change_titles_trends(indicator_view, CONTROLS)

    except:
        print(f"Error updating trend title for {CONTROLS['indicator']}")

    return [ds.get_layout()]


@timeit
def change_titles_reporting(indicator_view_name, controls):

    print(
        f"Starting updates for reporting titles with {controls['indicator']}")

    stacked_bar_reporting_country.title = get_title_reporting_country(
        stacked_bar_reporting_country.data, indicator_view_name, **controls
    )

    print(f"Updated reporting titles with {controls['indicator']}")


@timeit
def change_titles_trends(indicator_view_name, controls):

    print(f"Starting updates for trend titles with {controls['indicator']}")

    country_overview_scatter.title = get_title_country_overview(
        country_overview_scatter.data, indicator_view_name, **controls
    )

    district_overview_scatter.title = get_title_district_overview(
        district_overview_scatter.data, indicator_view_name, **controls
    )

    print(f"Updated trend titles with {controls['indicator']} with")


@timeit
def update_on_click(*inputs):

    try:

        label = inputs[0].get("points")[0].get("label")

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
