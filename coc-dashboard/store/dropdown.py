import pandas as pd
from model import SideNav, DateDropdownLayout, InfoPane
import calendar
from datetime import datetime
import base64

from .database import Database
from package.components.nested_dropdown_group import NestedDropdownGroup

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DEFAULTS = {
    "outlier": os.environ["OUTLIER"],
    "indicator": os.environ["INDICATOR"],
    "indicator_group": os.environ["INDICATOR_GROUP"],
    "district": os.environ["DISTRICT"],
    "target_year": os.environ["TARGET_YEAR"],
    "target_month": os.environ["TARGET_MONTH"],
    "reference_year": os.environ["REFERENCE_YEAR"],
    "reference_month": os.environ["REFERENCE_MONTH"],
    "trends_map_compare_agg": os.environ["COMPARE_AGG"],
    "trends_map_period_agg": os.environ["PERIOD_AGG"],
    "trends_treemap_agg": os.environ["PERIOD_AGG"],
    "report_map_compare_agg": os.environ["COMPARE_AGG"],
    "report_map_period_agg": os.environ["PERIOD_AGG"],
}


def initiate_dropdowns():

    db = Database()

    # Initiate type of aggregation dropdown

    entries = pd.DataFrame(
        {
            "aggregation_type": [
                "Compare two months",
                "Compare moving averages (last 3 months)",
                "Average over period",
                "Sum over period",
            ]
        }
    )

    dates = list(pd.to_datetime(db.raw_data.date.unique()))
    dates.sort()
    dates = [x.strftime("%b %Y") for x in dates]

    date_dropdowns = DateDropdownLayout(
        options=dates,
        from_default=DEFAULTS.get("reference_month")
        + " "
        + DEFAULTS.get("reference_year"),
        to_default=DEFAULTS.get("target_month") + " " +
        DEFAULTS.get("target_year"),
    )

    # Initiate outlier policy dropdown

    outlier_policy_dropdown_group = NestedDropdownGroup(
        pd.DataFrame(
            {
                "SELECT AN OUTLIER POLICY": [
                    "Keep outliers",
                    "Correct outliers - using standard deviation",
                    "Correct outliers - using interquartile range",
                ]
            }
        ),
        title="SELECT AN OUTLIER POLICY",
        defaults={
            "SELECT AN OUTLIER POLICY": DEFAULTS.get("outlier"),
        },
    )

    indicator_dropdown_group = NestedDropdownGroup(
        db.indicator_dropdowns,
        title="SELECT AN INDICATOR",
        defaults={
            "config_group": DEFAULTS.get("indicator_group"),
            "config_indicator": DEFAULTS.get("indicator"),
        },
    )

    district_control_group = NestedDropdownGroup(
        pd.DataFrame({"SELECT A DISTRICT": db.districts}),
        title="SELECT A DISTRICT",
        defaults={"SELECT A DISTRICT": DEFAULTS.get("district")},
    )

    side_nav = SideNav(
        elements=[
            indicator_dropdown_group,
            district_control_group,
            date_dropdowns,
            outlier_policy_dropdown_group,
        ],
        info="Click for more information",
    )

    info_pane = InfoPane(image="/static/images/info-pane.png",
                         text=f"""The data shown here was last fetched from DHIS2 on {db.fetch_date}.""")

    return (
        side_nav,
        outlier_policy_dropdown_group,
        indicator_dropdown_group,
        date_dropdowns,
        district_control_group,
        info_pane
    )
