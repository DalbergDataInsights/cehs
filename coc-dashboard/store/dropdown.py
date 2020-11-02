import pandas as pd
from model import SideNav, DateDropdownLayout
import calendar
from datetime import datetime

from store.helpers import month_order
from .database import Database
from package.components.nested_dropdown_group import NestedDropdownGroup
from package.components.methodology_section import MethodologySection

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DEFAULTS = {
    "default_outlier": os.environ["OUTLIER"],
    "default_indicator": os.environ["INDICATOR"],
    "default_indicator_group": os.environ["INDICATOR_GROUP"],
    "default_district": os.environ["DISTRICT"],
    "default_target_year": os.environ["TARGET_YEAR"],
    "default_target_month": os.environ["TARGET_MONTH"],
    "default_reference_year": os.environ["REFERENCE_YEAR"],
    "default_reference_month": os.environ["REFERENCE_MONTH"],
}


def initiate_dropdowns():

    db = Database()

    # Initiate type of aggregation dropdown

    entries = pd.DataFrame({"aggregation_type": ["Compare two months"]})

    aggregation_type = NestedDropdownGroup(
        entries, title="SELECT AN ANALYSIS TIMEFRAME"
    )

    # Initiate date dropdown layout

    dates = list(pd.to_datetime(db.raw_data.date.unique()))
    dates = [x.strftime("%b %Y") for x in dates]

    date_dropdowns = DateDropdownLayout(options=dates)

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
    )

    indicator_dropdown_group = NestedDropdownGroup(
        db.indicator_dropdowns,
        title="SELECT AN INDICATOR",
        info="We focus on a key set of indicators as advised by experts and described in WHO's list of priority indicators. For simplicity of interpretation and time comparison, we focus on absolute numbers rather than calculated indicators. ",
    )

    district_control_group = NestedDropdownGroup(
        pd.DataFrame({"SELECT A DISTRICT": db.districts}),
        title="SELECT A DISTRICT",
    )

    side_nav = SideNav(
        elements=[
            indicator_dropdown_group,
            district_control_group,
            aggregation_type,
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

    return (
        side_nav,
        outlier_policy_dropdown_group,
        indicator_dropdown_group,
        aggregation_type,
        date_dropdowns,
        district_control_group,
    )


def set_dropdown_defaults(
    outlier_policy_dropdown_group,
    aggregation_type,
    date_dropdowns,
    indicator_dropdown_group,
    district_control_group,
):
    outlier_policy_dropdown_group.dropdown_objects[0].value = DEFAULTS.get(
        "default_outlier"
    )

    date_dropdowns.from_date.value = (
        DEFAULTS.get("default_reference_month")
        + " "
        + DEFAULTS.get("default_reference_year")
    )

    indicator_dropdown_group.dropdown_objects[0].value = DEFAULTS.get(
        "default_indicator_group"
    )
    indicator_dropdown_group.dropdown_objects[1].value = DEFAULTS.get(
        "default_indicator"
    )

    date_dropdowns.from_date.value = (
        DEFAULTS.get("default_target_month") + " " + DEFAULTS.get("default_target_year")
    )

    district_control_group.dropdown_objects[0].value = DEFAULTS.get("default_district")
