from model import Overview
from store import init_data_set, timeit, Database
import pandas as pd


# Total number of outpatient attendances
# opd_attendance,OPD attendance, GENERAL

# Number of pregnant women with at least one ANC visit
# 1st_anc_visits,1st ANC Visits, MNCH

# Number of facility births
# births,Deliveries in unit, MNCH

# Number of perinatal deaths
# newborn_deaths,Newborn deaths, MNCH

# Number of maternal deaths
# maternal_deaths__mnch_all,Maternal deaths (all), MNCH

# Number of children younger than 1 year receiving their third dose of diphtheria-tetanus–pertussis (DPT3)
# dpt3__u1_all,DPT3 doses (all), EPI

# Number of children younger than 1 year receiving their first dose of measles vaccine (MR1)
# mr1__u1_all,MR1 doses (all), EPI

# Number of children 0-59 months diagnosed with severe wasting and bilateral pitting oedema (SAM)
# sam_identified,SAM cases identified, NUT

# Number of children 0–59 months of age who received an age-appropriate dose of vitamin A in each semester (Vit A second doses)
# vitamin_a,Doses of vitamin A (1st & 2nd), NUT

# Number of confirmed TB cases
# tb_cases_registered,TB cases registered, TB

# Number of injuries due to GBV
# injuries_gbv,Injuries related to GBV, FP


@timeit
def overview_plot(data):

    data = data.get("date_filter")

    # get only two dates
    min_date = data.date.min()
    max_date = data.date.max()

    mask = (data.date == min_date) | (data.date == max_date)
    data = data[mask]

    # filter indicators
    index = ["date"]
    indicators = {
        "OPD attendance": "rgb(39, 190, 182)",
        "1st ANC Visits": "rgb(244, 174, 26)",
        "Deliveries in unit": "rgb(244, 174, 26)",
        "Newborn deaths": "rgb(244, 174, 26)",
        "Maternal deaths": "rgb(244, 174, 26)",
        "DPT3 doses to U1": "rgb(81, 139, 201)",
        "MR1 doses to U1": "rgb(81, 139, 201)",
        "SAM cases identified": "rgb(238, 47, 68)",
        "1st & 2nd doses of vitamin A to U5": "rgb(103, 191, 107)",
        "TB cases registered": "rgb(236, 70, 139)",
        "Injuries related to GBV": "rgb(145, 91, 166)",
    }

    data = data[index + list(indicators.keys())]

    data = data.groupby(by="date").sum().reset_index()

    data = pd.melt(data, id_vars=["date"])

    data = pd.pivot_table(
        data, values="value", index="variable", columns="date"
    ).reset_index()

    data["percentage"] = (data[max_date] - data[min_date]
                          ) / data[min_date] * 100

    data["percentage"] = data["percentage"].apply(lambda x: round(x, 1))

    data.rename(
        columns={max_date: "absolute", "variable": "indicator_name"}, inplace=True
    )

    data["color"] = data["indicator_name"].apply(lambda x: indicators.get(x))

    data.drop(columns=[min_date], inplace=True)

    for col in data.columns:
        data[col] = data[col].astype(str)

    data["percentage"] = data["percentage"].apply(
        lambda x: f"{x}%" if x[0] == "-" else f"+{x}%"
    )

    sort_dict = dict(
        zip(list(indicators.keys()), range(0, len(list(indicators.keys()))))
    )

    data.sort_values(
        by=["indicator_name"],
        inplace=True,
        key=lambda x: x.map(sort_dict),
    )

    data.set_index(["indicator_name", "color", "percentage"], inplace=True)

    return {"overview": data}


overview = Overview(data=init_data_set, data_transform=overview_plot)
