import os
from .helpers import *
from .dropdown import initiate_dropdowns, DEFAULTS
from .database import Database


YEARS = [2018, 2019, 2020, 2021]


# READ FROM DATABASE

DATABASE_URI = os.environ["HEROKU_POSTGRESQL_CYAN_URL"]
db = Database(DATABASE_URI)

# STATIC DATA

from .geopopulation import shapefile  # NOQA: E402


# NAVIGATION

(
    side_nav,
    outlier_policy_dropdown_group,
    indicator_dropdown_group,
    date_dropdowns,
    district_control_group,
    info_pane,
) = initiate_dropdowns()


CONTROLS = dict(
    outlier=outlier_policy_dropdown_group.dropdown_objects[0].value,
    indicator=indicator_dropdown_group.dropdown_objects[-1].value,
    district=district_control_group.dropdown_objects[0].value,
    target_year=date_dropdowns.to_date.value.split(" ")[1],
    target_month=date_dropdowns.to_date.value.split(" ")[0],
    reference_year=date_dropdowns.from_date.value.split(" ")[1],
    reference_month=date_dropdowns.from_date.value.split(" ")[0],
    facility=None,
    indicator_group=indicator_dropdown_group.dropdown_objects[0].value,
    trends_map_compare_agg=DEFAULTS.get("trends_map_compare_agg"),
    trends_map_period_agg=DEFAULTS.get("trends_map_period_agg"),
    trends_treemap_agg=DEFAULTS.get("trends_treemap_agg"),
    report_map_compare_agg=DEFAULTS.get("report_map_compare_agg"),
    report_map_period_agg=DEFAULTS.get("report_map_period_agg"),
)

print("Init control dict")
print(CONTROLS)

LAST_CONTROLS = {}

# CREDENTIALS

credentials = {}

for x in os.environ:
    if "DASH_AUTH" in x:
        login = x.split("DASH_AUTH_")[1]
        password = os.environ.get(x, os.environ.get("SECRET"))
        credentials[login] = password

# GLOBAL DATASET

from .define_datasets import define_datasets  # NOQA: E402

init_data_set = define_datasets(controls=CONTROLS)
