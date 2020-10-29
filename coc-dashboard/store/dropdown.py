import pandas as pd
from model import SideNav

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

    # Initiate data selection dropdowns

    max_date = db.raw_data.date.max()
    (max_year, max_month_number) = (max_date.year, max_date.month)
    max_month = month_order[max_month_number - 1]

    years = [2018] * 12 + [2019] * 12 + [2020] * max_month_number

    date_columns = pd.DataFrame(
        {"year": years, "month": month_order * 2 + month_order[:max_month_number]}
    )

    date_columns.year = date_columns.year.astype(str)

    date_columns.columns = ["Target Year", "Target Month"]
    target_date = NestedDropdownGroup(
        date_columns.copy(), title="SELECT AN ANALYSIS TIMEFRAME", vertical=False
    )

    date_columns.columns = ["Reference Year", "Reference Month"]
    reference_date = NestedDropdownGroup(
        date_columns, title="SELECT AN ANALYSIS TIMEFRAME", vertical=False
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
            reference_date,
            target_date,
            outlier_policy_dropdown_group,
        ],
        info=f"""
        The data shown here was last fetched from DHIS2 on {db.fetch_date}.

        We provide two layers of information on reporting rate: \n A form-specific indicator -
        the percentage of facilities that reported on their 105:1 form out of those expected to report.
        This is similar to the reporting rates displayed on the DHIS2 system. An indicator-specific
        indicator - the percentage of facilities that reported a positive number for the selected
        indicator out of all facilities that have submitted their 105:1 form. This provides added
        information on how otherwise reporting facilities report on this specific indicator.""",
    )

    return (
        side_nav,
        outlier_policy_dropdown_group,
        indicator_dropdown_group,
        reference_date,
        target_date,
        district_control_group,
    )


def set_dropdown_defaults(
    outlier_policy_dropdown_group,
    target_date,
    reference_date,
    indicator_dropdown_group,
    district_control_group,
):
    outlier_policy_dropdown_group.dropdown_objects[0].value = DEFAULTS.get(
        "default_outlier"
    )

    target_date.dropdown_objects[0].value = DEFAULTS.get("default_target_year")
    target_date.dropdown_objects[1].value = DEFAULTS.get("default_target_month")

    indicator_dropdown_group.dropdown_objects[0].value = DEFAULTS.get(
        "default_indicator_group"
    )
    indicator_dropdown_group.dropdown_objects[1].value = DEFAULTS.get(
        "default_indicator"
    )

    reference_date.dropdown_objects[0].value = DEFAULTS.get("default_reference_year")
    reference_date.dropdown_objects[1].value = DEFAULTS.get("default_reference_month")

    district_control_group.dropdown_objects[0].value = DEFAULTS.get("default_district")
