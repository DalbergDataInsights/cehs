from store import (
    filter_df_by_dates,
    filter_by_district,
    get_ratio,
    Database,
)

import pandas as pd

# CARD 1

# FIXME Try and run without teh outlier parameter, see if it breaks anything


def scatter_country_data(*, indicator, **kwargs):

    # dfs, static,

    db = Database()

    df = db.raw_data

    df = db.filter_by_indicator(df, indicator)

    df, index = get_ratio(df, indicator, agg_level='country')

    df = df.set_index(index)

    title = f'Total {db.get_indicator_view(indicator)} across the country'

    df = df.rename(columns={indicator: title})

    return df


# CARD 2

def apply_date_filter(
    *,
    outlier,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):
    db = Database()

    df = db.raw_data

    df = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    return df


def map_bar_country_dated_data(
    *,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):

    db = Database()

    df = db.raw_data

    df = db.filter_by_indicator(df, indicator)

    df = get_ratio(df, indicator, agg_level='district')[0]

    data_in = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    # TODO updat teh filter by data function so that this step is no longer needed

    min_date = data_in.date.min()
    max_date = data_in.date.max()

    mask = (data_in.date == min_date) | (data_in.date == max_date)

    data_in = data_in[mask]

    data_in["year"] = data_in.date.apply(lambda x: x.year)

    data_in = data_in.pivot_table(columns="year", values=indicator, index="id")

    data_in[indicator] = (
        (data_in[int(target_year)] - data_in[int(reference_year)])
        / data_in[int(reference_year)]
        * 100
    )
    data_in[indicator] = data_in[indicator].apply(lambda x: round(x, 2))

    data_in = data_in[[indicator]].reset_index()
    data_in = data_in.set_index("id")
    data_out = data_in[~pd.isna(data_in[indicator])]

    title = f'Percentage change of {db.get_indicator_view(indicator)} between {reference_month}-{reference_year} and {target_month}-{target_year}'
    data_out = data_out.rename(columns={indicator: title})

    return data_out


# CARD 3


def scatter_district_data(*,  indicator, district, **kwargs):

    db = Database()

    df = db.raw_data

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    df, index = get_ratio(df, indicator, agg_level='district')

    df = df.set_index(index)

    title = f'Total {db.get_indicator_view(indicator)} in {district} district'

    df = df.rename(columns={indicator: title})

    return df


# CARD 4


def tree_map_district_dated_data(
    *,
    indicator,
    district,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,


):

    db = Database()

    df = db.raw_data

    indicator = db.vet_indic_for_pop_dependency(indicator)

    df = db.filter_by_indicator(df, indicator)

    df = get_ratio(df, indicator, agg_level='facility')[0]

    # TODO check how the date function works such that it shows only target date

    df_district_dated = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    df_district_dated = filter_by_district(df_district_dated, district)

    title = f'"Contribution of individual facilities to {db.get_indicator_view(indicator)} in {district} district'

    df_district_dated = df_district_dated.rename(columns={indicator: title})

    return df_district_dated


def scatter_facility_data(*, indicator, district, facility, **kwargs):

    db = Database()

    df = db.raw_data

    indicator = db.vet_indic_for_pop_dependency(indicator)

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    df, index = get_ratio(df, indicator, agg_level='facility')

    # TODO Reorder such that its the one facility with the on selected data max value that shows

    if not facility:
        facility = (
            df.sort_values(df.columns[-1], ascending=False)
            .reset_index()
            .facility_name[0]
        )

    df = df[df.facility_name == facility].reset_index(drop=True)

    title = f'Evolution of {db.get_indicator_view(indicator)} in {facility}'

    df = df.rename(columns={indicator: title})

    df = df.set_index(index)

    return df


# CARD 5


def bar_reporting_country_data(*, outlier, indicator, **kwargs):

    db = Database()

    df = db.rep_data

    df = db.filter_by_indicator(df, indicator)

    title = f'Total number of facilities reporting on their 105:1 form, and reporting a non-zero number for {db.get_indicator_view(indicator)} across the country'

    df = df.rename(columns={indicator: title})

    return df


# CARD 6


def map_reporting_dated_data(
    *,
    outlier,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):

    db = Database()

    df = db.rep_data

    df = db.filter_by_indicator(df, indicator)

    df = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    title = f'Percentage of reporting facilities that reported a non-zero number for {db.get_indicator_view(indicator)} by district'

    df = df.rename(columns={indicator: title})

    return df


# CARD 7


def scatter_reporting_district_data(*, outlier, indicator, district, **kwargs):

    db = Database()

    df = db.rep_data

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    title = f'Total number of facilities reporting on their 105:1 form, and reporting a non-zero number for {db.get_indicator_view(indicator)} in {district} district'

    df = df.rename(columns={indicator: title})

    return df
