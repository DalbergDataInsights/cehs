# Data csv download links

import xlsxwriter
import pandas as pd
import base64
import io


def download_file(dict_of_st):

    xlsx_io = io.BytesIO()
    writer = pd.ExcelWriter(xlsx_io, engine="xlsxwriter")

    for df_name, df in dict_of_st.items():
        if len(df_name) > 31:
            df_name = df_name[:30]

        df.to_excel(writer, sheet_name=df_name)
    writer.save()
    xlsx_io.seek(0)

    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    href_data_downloadable = f"data:{media_type};base64,{data}"
    return href_data_downloadable


# Methodology section


def meth_data(date):
    meth_data = [
        {
            "sub_title": "Date of download",
            "body": f"The data shown here was last fetched from DHIS2 on {date}.",
            "list_data": [],
        },
        {
            "sub_title": "Reporting Rates ",
            "body": "We provide two layers of information on reporting rate:",
            "list_data": [
                "A form-specific indicator - the percentage of facilities that reported on their 105:1 form out of those expected to report. This is similar to the reporting rates displayed on the DHIS2 system.",
                "An indicator-specific indicator - the percentage of facilities that reported a positive number for the selected indicator out of all facilities that have submitted their 105:1 form. This provides added information on how otherwise reporting facilities report on this specific indicator. ",
            ],
        },
    ]
    return meth_data
