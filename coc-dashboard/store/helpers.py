from rich import print
from time import time
from datetime import datetime
import pandas as pd
import numpy as np

month_order = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


# Filtering methods for data transform functions


def filter_df_by_dates(df, target_year, target_month, reference_year, reference_month):
    min_date = None
    max_date = None
    reverse = False

    # TODO See if I can just have this return only the two dates, not everything in between

    df = df.sort_values(["date"])

    if target_year and target_month:
        target_date = datetime(
            int(target_year), int(month_order.index(target_month) + 1), 1
        )
    if reference_year and reference_month:
        reference_date = datetime(
            int(reference_year), int(month_order.index(reference_month) + 1), 1
        )
    if reference_date <= target_date:
        max_date = target_date
        min_date = reference_date
    elif target_date < reference_date:
        max_date = reference_date
        min_date = target_date
        reverse = True
    if min_date:
        min_mask = df.date >= min_date
        df = df.loc[min_mask].reset_index(drop=True)
    if max_date:
        max_mask = df.date <= max_date
        df = df.loc[max_mask].reset_index(drop=True)
    if reverse:
        df = df.reindex(index=df.index[::-1])
    return df


def filter_by_district(df, district):
    mask = df.id == district
    df = df.loc[mask].reset_index(drop=True)
    return df


def get_sub_dfs(df, select_index, values, new_index, order=None):
    """
    Extract and return a dictionary of dictionaries splitting each original dictionary df entry into traces based on values
    """

    traces = {}
    for value in values:
        sub_df = df[df.index.get_level_values(select_index) == value]
        sub_df = sub_df.groupby(new_index).sum()
        if order:
            sub_df = sub_df.reindex(order)
        traces[value] = sub_df

    return traces


def get_num(df, value=3):
    """
    Gets a dataframe of the count of the specified value for each column; expects index formatting including date and id
    """
    df_count_all = []
    for date in list((df.index.get_level_values("date")).unique()):
        count_for_date = (df.loc[date] == value).sum()
        df_count_for_date = (pd.DataFrame(count_for_date)).transpose()
        df_count_for_date.index = [date]
        df_count_all.append(df_count_for_date)
    new_df = pd.concat(df_count_all)
    return new_df


def reporting_count_transform(data):
    """
    Counts occurrence of type of reporting label for each date, returning dictionary
    """
    # Set index
    data = check_index(data)
    # Remove unnecessary index values
    data = data.droplevel(["id"])
    # Count number of positive_indic
    df_positive = get_num(data, 3)
    # Count number of no_positive_indic
    df_no_positive = get_num(data, 2)
    # Count number of no_form_report
    df_no_form_report = get_num(data, 1)

    data = {
        "Reported a positive number": df_positive,
        "Did not report a positive number": df_no_positive,
        "Did not report on their 105:1 form": df_no_form_report,
    }
    return data


def get_year_and_month_cols(df):

    df = df.reset_index()

    df["year"] = pd.DatetimeIndex(df["date"]).year
    df["month"] = pd.DatetimeIndex(df["date"]).strftime("%b")

    df = df.set_index(["date", "year", "month"])

    return df


# Data cleaning methods for dataset selection and callbacks


def get_ratio(df, indicator, agg_level):
    """
    Aggregates the ratio properly using weights

    """
    # TODO Link to the index_columns defined in the database object
    # TODO find a way to delete the hardcoded name mapping step

    index = ["date", "id", "facility_name"]

    if agg_level == 'country':
        index = [index[0]]

    if agg_level == 'district':
        index = index[:2]

    df = df.groupby(index, as_index=False).sum()

    col_count = len(set(df.columns).difference(set(index)))

    if col_count == 2:

        weighted_ratio = [
            x for x in df.columns if x.endswith('__weighted_ratio')][0]
        weight = [x for x in df.columns if x.endswith('__weight')][0]

        df[indicator] = (df[weighted_ratio]*1000) / df[weight]

        df = df.drop(
            columns=[weighted_ratio, weight])

    return df, index


def check_index(df, index=["id", "date", "facility_name"]):
    """
    Check that the dataframe is formatted in the expected way, with expected indexes. Restructure the dataframe (set the indices) if this is not the case.
    """
    if df.index.values != index:

        df = df.reset_index(drop=True).set_index(index)
    return df


# Decorators


def timeit(f):
    def timed(*args, **kw):

        ts = time()
        result = f(*args, **kw)
        te = time()
        run = round(te - ts, 3)

        print(
            f"[cyan]{f.__name__}()[/cyan] took: [bold blue]{run}[/bold blue] seconds to run."
        )

        return result

    return timed


# Formattimg method


def get_perc_description(perc):
    perc_abs = abs(perc)
    if perc >= 0.1:
        descrip = f"increased by {perc_abs}%"
    elif perc_abs < 0.1:
        descrip = "remained stable"
    elif perc <= 0.1:
        descrip = f"decreased by {perc_abs}%"
    return descrip
