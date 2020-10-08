import pandas as pd
from model import SideNav

from store.helpers import month_order
from package.components.nested_dropdown_group import NestedDropdownGroup
from package.components.methodology_section import MethodologySection

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DEFAULTS = {
    "default_outlier": os.environ["OUTLIER"],
    "default_indicator": os.environ["INDICATOR"],
    "default_indicator_type": os.environ["INDICATOR_TYPE"],
    "default_district": os.environ["DISTRICT"],
    "default_target_year": os.environ["TARGET_YEAR"],
    "default_target_month": os.environ["TARGET_MONTH"],
    "default_reference_year": os.environ["REFERENCE_YEAR"],
    "default_reference_month": os.environ["REFERENCE_MONTH"],
}


def initiate_dropdowns(data_outliers, indicator_group):

    years = [2018] * 12 + [2019] * 12 + [2020] * 12

    date_columns = pd.DataFrame({"year": years, "month": month_order * 3})
    date_columns.year = date_columns.year.astype(str)
    date_columns.columns = ["Target Year", "Target Month"]
    target_date = NestedDropdownGroup(
        date_columns.copy(), title="Select target date", vertical=False
    )

    # TODO Have those defined as this month - 1

    outlier_policy_dropdown_group = NestedDropdownGroup(
        pd.DataFrame(
            {
                "Select an outlier correction policy": [
                    "Keep outliers",
                    "Correct outliers - using standard deviation",
                    "Correct outliers - using interquartile range",
                ]
            }
        ),
        title="Select an outlier correction policy",
    )

    indicator_dropdown_group = NestedDropdownGroup(
        indicator_group, title="Select an indicator"
    )


    years = [2018] * 12 + [2019] * 12 + [2020] * 12

    date_columns = pd.DataFrame({"year": years, "month": month_order * 3})

    date_columns.columns = ["Target Year", "Target Month"]
    target_date = NestedDropdownGroup(
        date_columns.copy(), title="Select target date", vertical=False
    )

    # TODO Have those defined as this month - 1

    date_columns.columns = ["Reference Year", "Reference Month"]
    reference_date = NestedDropdownGroup(
        date_columns, title="Select reference date", vertical=False
    )



    district_control_group = NestedDropdownGroup(
        data_outliers[["id"]].rename(
            columns={"id": "Please select a district"}),
        title="Select a district",
    )

    side_nav = SideNav(
        [
            outlier_policy_dropdown_group,
            indicator_dropdown_group,
            reference_date,
            target_date,
            district_control_group,
        ]
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
        "default_indicator_type"
    )
    # TODO Link that to default indic
    indicator_dropdown_group.dropdown_objects[1].value = "EPI"
    indicator_dropdown_group.dropdown_objects[2].value = DEFAULTS.get(
        "default_indicator"
    )

    reference_date.dropdown_objects[0].value = DEFAULTS.get("default_reference_year")
    reference_date.dropdown_objects[1].value = DEFAULTS.get("default_reference_month")

    district_control_group.dropdown_objects[0].value = DEFAULTS.get("default_district")