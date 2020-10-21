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


def get_year_and_month_cols(df):

    df = df.reset_index()

    df["year"] = pd.DatetimeIndex(df["date"]).year
    df["month"] = pd.DatetimeIndex(df["date"]).strftime("%b")

    df = df.set_index(["date", "year", "month"])

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


rng = pd.date_range(start="2019-04-01", end="2020-04-01", periods=12)
df = pd.DataFrame({"date": rng, "val": np.random.randn(len(rng))})

df1 = get_year_and_month_cols(df)

df2 = get_sub_dfs(df1, "year", [2018, 2019, 2020], "month", month_order)
