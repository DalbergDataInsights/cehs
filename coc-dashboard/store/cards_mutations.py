from store import (
    filter_df_by_dates,
    filter_by_district,
    get_ratio,
    Database,
    get_df_compare,
    get_df_period
)

import pandas as pd
import numpy as np
from datetime import datetime


# Overview

def overview_data(
    *,
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


# CARD 1


def scatter_country_data(*, indicator, **kwargs):

    # dfs, static,

    db = Database()

    df = db.raw_data

    df = db.filter_by_indicator(df, indicator)

    df, index = get_ratio(df, indicator, agg_level='country')[0:2]

    df = df.set_index(index)

    title = f'Total {db.get_indicator_view(indicator)} across the country'

    df = df.rename(columns={indicator: title})

    return df


# CARD 2

def map_bar_country_compare_data(
    *,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    trends_map_compare_agg,
    **kwargs,
):

    db = Database()

    df = db.raw_data

    df = db.filter_by_indicator(df, indicator)

    df = get_ratio(df, indicator, agg_level='district')[0]

    df = get_df_compare(df, indicator,
                        target_year, target_month,
                        reference_year, reference_month, trends_map_compare_agg)

    if trends_map_compare_agg == "Compare three months moving average":
        quarter = 'the three months periods ending in '
    else:
        quarter = ''

    title = f'Percentage change in {db.get_indicator_view(indicator)} between {quarter}{reference_month}-{reference_year} and {target_month}-{target_year}'

    df = df.rename(columns={indicator: title})

    return df


def map_bar_country_period_data(
    *,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    trends_map_period_agg,
    **kwargs,
):

    db = Database()

    df = db.raw_data

    df = db.filter_by_indicator(df, indicator)

    df = get_ratio(df, indicator, agg_level='district')[0]

    isratio = get_ratio(df, indicator, agg_level='district')[2]

    df = get_df_period(df, indicator,
                       target_year, target_month,
                       reference_year, reference_month, trends_map_period_agg, isratio=isratio)

    if trends_map_period_agg == "Show only month of interest":
        title = title = f'Total {db.get_indicator_view(indicator)} on {reference_month}-{reference_year} by district'

    else:
        if trends_map_period_agg == "Show sum over period":
            if isratio:
                data = 'Average'
            else:
                data = 'Total'
        else:
            data = 'Average'

        title = f'{data} {db.get_indicator_view(indicator)} between {reference_month}-{reference_year} and {target_month}-{target_year}'

    df = df.rename(columns={indicator: title})

    return df

# CARD 3


def scatter_district_data(*,  indicator, district, **kwargs):

    db = Database()

    df = db.raw_data

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    df, index = get_ratio(df, indicator, agg_level='district')[0:2]

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
    trends_treemap_agg,
    **kwargs,

):

    db = Database()

    df = db.raw_data

    indicator = db.switch_indic_to_numerator(indicator)

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    df = get_ratio(df, indicator, agg_level='facility')[0]

    isratio = get_ratio(df, indicator, agg_level='facility')[2]

    df_district_dated = get_df_period(df, indicator,
                                      target_year, target_month,
                                      reference_year, reference_month, trends_treemap_agg,
                                      index=['id', 'facility_name'], isratio=isratio)

    if trends_treemap_agg == "Show only month of interest":
        agg = 'Contribution'
        period = f'on {target_month}-{target_year}'
    elif trends_treemap_agg == "Show sum over period":
        if isratio:
            agg = 'Average contribution'
            period = f'on {target_month}-{target_year}'
        else:
            agg = 'Total contribution'
            period = f'between {reference_month}-{reference_year} and {target_month}-{target_year}'
    else:
        agg = 'Average contribution'
        period = f'on {target_month}-{target_year}'

    title = f'''{agg} of individual facilities in {district} district to 
            {db.get_indicator_view(indicator)} {period}'''

    df_district_dated = df_district_dated.rename(columns={indicator: title})

    return df_district_dated


def scatter_facility_data(*, indicator, district, facility, **kwargs):

    db = Database()

    df = db.raw_data

    indicator = db.switch_indic_to_numerator(indicator)

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    df, index = get_ratio(df, indicator, agg_level='facility')[0:2]

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


def bar_reporting_country_data(*, indicator, **kwargs):

    db = Database()

    df = db.rep_data

    indicator = db.switch_indic_to_numerator(indicator, popcheck=False)

    df = db.filter_by_indicator(df, indicator)

    title = f'Total number of facilities reporting on their 105:1 form, and reporting a non-zero number for {db.get_indicator_view(indicator)} across the country'

    df = df.rename(columns={indicator: title})

    return df


# CARD 6


def map_reporting_compare_data(
    *,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    report_map_compare_agg,
    **kwargs,
):

    db = Database()

    df = db.rep_data

    indicator = db.switch_indic_to_numerator(indicator, popcheck=False)

    df = db.filter_by_indicator(df, indicator)

    df = get_df_compare(df, indicator,
                        target_year, target_month,
                        reference_year, reference_month, report_map_compare_agg, report=True)

    if report_map_compare_agg == "Compare three months moving average":
        quarter = 'the three months periods ending in '
    else:
        quarter = ''

    title = f'''Percentage change in proportion of reporting facilities that reported a non-zero number for 
            {db.get_indicator_view(indicator)} by district between 
            {quarter}{reference_month}-{reference_year} and {target_month}-{target_year}'''

    df = df.rename(columns={indicator: title})

    return df


def map_reporting_period_data(
    *,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    report_map_period_agg,
    **kwargs,
):

    db = Database()

    df = db.rep_data

    indicator = db.switch_indic_to_numerator(indicator, popcheck=False)

    df = db.filter_by_indicator(df, indicator)

    df = get_df_period(df, indicator,
                       target_year, target_month,
                       reference_year, reference_month, report_map_period_agg, report=True)

    if report_map_period_agg == "Show only month of interest":
        title = f'''Proportion of reporting facilities that reported a non-zero number for 
            {db.get_indicator_view(indicator)} on {reference_month}-{reference_year}'''

    else:
        title = f'''Average proportion of reporting facilities that reported a non-zero number for 
            {db.get_indicator_view(indicator)} between {reference_month}-{reference_year} and {target_month}-{target_year}'''

    df = df.rename(columns={indicator: title})

    return df


# CARD 7


def scatter_reporting_district_data(*, indicator, district, **kwargs):

    db = Database()

    df = db.rep_data

    indicator = db.switch_indic_to_numerator(indicator, popcheck=False)

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    title = f'Total number of facilities reporting on their 105:1 form, and reporting a non-zero number for {db.get_indicator_view(indicator)} in {district} district'

    df = df.rename(columns={indicator: title})

    return df
