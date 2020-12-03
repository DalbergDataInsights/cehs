import pandas as pd
from model import SideNav, DateDropdownLayout
import calendar
from datetime import datetime

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
    "aggregation_type": os.environ["AGGREGATION_TYPE"],
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
        to_default=DEFAULTS.get("target_month") + " " + DEFAULTS.get("target_year"),
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
        info="""We exclude outliers at facility level - for a given facility and indicator, we look at all data points available since January
        2018 and replace all data points identified as outliers by the sample's median. We give two options for outlier exclusion. \n
        A standard deviation-based approach, where all points more than three standard deviations away from the mean are considered outliers.
        This approach is best suited for 'cleaner', normally distributed data. An interquartile range-based approach, using Tukey's fences method with k=3,
        which fits a broader range of data distributions but is also more stringent, and hence best suited for 'messier' data.""",
        defaults={
            "SELECT AN OUTLIER POLICY": DEFAULTS.get("outlier"),
        },
    )

    indicator_dropdown_group = NestedDropdownGroup(
        db.indicator_dropdowns,
        title="SELECT AN INDICATOR",
        info="We focus on a key set of indicators as advised by experts and described in WHO's list of priority indicators. For simplicity of interpretation and time comparison, we focus on absolute numbers rather than calculated indicators. ",
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
        info=f"""
        The data shown here was last fetched from DHIS2 on {db.fetch_date}.""",
    )

    side_nav.trends_info = """Identify data trends, from the national level to the facility level.
    If you notice any surprising trends, make sure to check the effect of a more stringent outlier exclusion policy on that trend,
    and explore the reporting tool to better understand whether a reporting issue could explain that trend."""

    side_nav.datarep_info = """We provide two layers of information on reporting rate: \n A form-specific indicator -
        the percentage of facilities that reported on their 105:1 form out of those expected to report.
        This is similar to the reporting rates displayed on the DHIS2 system. An indicator-specific
        indicator - the percentage of facilities that reported a positive number for the selected
        indicator out of all facilities that have submitted their 105:1 form. This provides added
        information on how otherwise reporting facilities report on this specific indicator."""

    side_nav.overview_info = """Here we offer a quick overview of the WHO's 20 CEHS indicators. We provide both absolute value and the percentage change compared to the first date in the chosen time frame."""

    return (
        side_nav,
        outlier_policy_dropdown_group,
        indicator_dropdown_group,
        date_dropdowns,
        district_control_group,
    )
