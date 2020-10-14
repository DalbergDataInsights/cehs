from datetime import datetime

from numpy.lib.shape_base import dsplit

from components import (
    country_overview_scatter,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
)

from store import (
    CONTROLS,
    LAST_CONTROLS,
    define_datasets,
    month_order,
    timeit,
    # indicator_groups,
    get_perc_description,
    # get_new_indic_name,
)

from view import ds


@timeit
def global_story_callback(*inputs):

    outlier = inputs[0]
    indicator = inputs[1]
    reference_year = inputs[2]
    reference_month = inputs[3]
    target_year = inputs[4]
    target_month = inputs[5]
    district = inputs[6]
    indicator_group = inputs[7]

    global LAST_CONTROLS
    LAST_CONTROLS = CONTROLS.copy()

    CONTROLS["outlier"] = outlier
    CONTROLS["indicator"] = indicator
    CONTROLS["district"] = district
    CONTROLS["target_year"] = target_year
    CONTROLS["target_month"] = target_month
    CONTROLS["reference_year"] = reference_year
    CONTROLS["reference_month"] = reference_month
    CONTROLS["indicator_group"] = indicator_group

    ds = define_datasets(controls=CONTROLS, last_controls=LAST_CONTROLS)

    ds.switch_data_set(ds)

    return [ds.get_layout()]


@timeit
def change_titles(*inputs):

    outlier = inputs[0]
    indicator = inputs[1]
    reference_year = inputs[2]
    reference_month = inputs[3]
    target_year = inputs[4]
    target_month = inputs[5]
    district = inputs[6]
    indicator_group_select = inputs[7]

    indicator_view_name = indicator
    # indicator_view_name = get_new_indic_name(
    #     indicator_groups, indicator, indicator_group_select)

    # Data card 1

    try:

        data = country_overview_scatter.data
        data_reference = data.get(int(reference_year))
        data_target = data.get(int(target_year))
        perc_first = round(
            (
                (
                    data_target.loc[target_month][0]
                    - data_reference.loc[reference_month][0]
                )
                / data_reference.loc[reference_month][0]
            )
            * 100
        )
        descrip = get_perc_description(perc_first)

    except Exception as e:
        print(e)
        descrip = "changed by an unknown percentage"

    country_overview_scatter.title = f"Overview: Across the country, the {indicator_view_name} {descrip} between {reference_month}-{reference_year} and {target_month}-{target_year}"

    try:

        dis_data = district_overview_scatter.data

        dis_data_reference = dis_data.get(int(reference_year))
        dis_data_target = dis_data.get(int(target_year))

        dist_perc = round(
            (
                (
                    dis_data_target.loc[target_month][0]
                    - dis_data_reference.loc[reference_month][0]
                )
                / dis_data_reference.loc[reference_month][0]
            )
            * 100
        )
        descrip = get_perc_description(dist_perc)

    except Exception as e:
        print(e)
        descrip = "changed by an unknown percentage"

    district_overview_scatter.title = f"Deep-dive in {district} district: the {indicator_view_name} {descrip} between {reference_month}-{reference_year} and {target_month}-{target_year}"

    try:
        data_reporting = stacked_bar_reporting_country.data

        date_reporting = datetime(
            int(target_year), month_order.index(target_month) + 1, 1
        )

        try:
            reported_positive = data_reporting.get("Reported a positive number").loc[
                date_reporting
            ][0]
        except Exception:
            reported_positive = 0
        try:
            did_not_report = data_reporting.get(
                "Did not report on their 105:1 form"
            ).loc[date_reporting][0]
        except Exception:
            did_not_report = 0
        try:
            reported_negative = data_reporting.get(
                "Did not report a positive number"
            ).loc[date_reporting][0]
        except Exception:
            reported_negative = 0

        reported_perc = round(
            (
                (reported_positive + reported_negative)
                / (reported_positive + did_not_report + reported_negative)
            )
            * 100
        )
        reported_positive = round(
            (reported_positive / (reported_positive + reported_negative)) * 100
        )
    except Exception:
        reported_perc = "?"
        reported_positive = "?"

    stacked_bar_reporting_country.title = (
        f"Reporting: On {target_month}-{target_year}, around {reported_perc}% of facilities reported on their 105:1 form, and, out of those, {reported_positive}% reported for {indicator_view_name}",
    )

    tree_map_district.title = f"Contribution of individual facilities in {district} district to the {indicator_view_name} on {target_month}-{target_year}"

    return [
        country_overview_scatter.title,
        district_overview_scatter.title,
        # stacked_bar_reporting_country.title,
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
        facility_scatter.figure = facility_scatter._get_figure(facility_scatter.data)
        facility_scatter.figure_title = (
            f"Evolution of $label$ in {label} (click on the graph above to filter)"
        )

    except Exception as e:
        print(e)

    return [facility_scatter.figure, facility_scatter.figure_title]
