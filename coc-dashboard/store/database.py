from datetime import datetime
from os import rename
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from model.database import FetchDate, Population, PopulationTarget, IndicatorGroup
import pandas as pd
from .helpers import timeit


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """
    Singleton database class
    ! This class should be called for the first time with DB bind_string.

    Keyword arguments:
    bind_string -- SQLAlchemy-like DB bind string
    Return: Database
    """

    fetch_data_query = """SELECT * FROM {}"""
    repos = ["value_raw", "value_rep", "value_std", "value_iqr"]

    indicator_group_fetch_query = """SELECT * FROM indicator_group;"""

    data_types = {
        "district_name": str,
        "facility_name": str,
        "date": "datetime64[ns]",
        "indicator_name": str,
        "*": int,
    }

    index_columns = ["id", "facility_name", "date"]

    datasets = {}
    raw_data = {}

    init = False

    def __init__(self, bind_string=None):
        if bind_string:
            self.engine = create_engine(bind_string)
            self.Session = sessionmaker(bind=self.engine)
            self.init = True

            print("Fetching data")
            for repo in self.repos:
                self.raw_data[repo] = self.get_repository(repo)
            self.districts = self.raw_data["value_raw"].id.unique()
            self.districts.sort()

        assert self.init, "You must pass a DB bind string to use Database first!"
        self.set_indicator_groups_and_view()

    @timeit
    def get_repository(self, repo_name):

        __dataframe = pd.read_sql(
            self.fetch_data_query.format(repo_name), con=self.engine
        )

        for col in __dataframe.columns:
            try:
                __dataframe[col] = __dataframe[col].astype(
                    self.data_types.get(col, self.data_types.get("*"))
                )
            except:
                print(f"Was not able to convert {col}")

        __dataframe.rename(columns={"district_name": "id"}, inplace=True)

        return __dataframe

    @property
    def fetch_date(self):
        session = self.Session()
        date = session.query(FetchDate).one()
        session.close()
        return date.serialize()

    def filter_by_indicator(self, df, indicator):
        df = df.reset_index()
        try:
            df = df[self.index_columns + [indicator]]
        except Exception as e:
            print(e)
            print("No such column is present in the dataframe")
        return df

    def include_dataset(self, key, df):
        self.datasets[key] = df

    def fetch_dataset(self, key):
        return self.datasets.get(key)

    def get_serialized_obj(self, sqlalchemy_obj):
        session = self.Session()
        objects = session.query(sqlalchemy_obj).all()
        serialized = [obj.serialize() for obj in objects]
        session.close()
        return serialized

    def get_serialized_into_df(self, sqlalchemy_obj):
        df = pd.DataFrame(self.get_serialized_obj(sqlalchemy_obj))
        return df

    def get_population_data(self):
        return self.get_serialized_into_df(Population)

    def get_population_target(self):
        return self.get_serialized_into_df(PopulationTarget)

    def set_indicator_groups_and_view(self):
        serialized_groups = self.get_serialized_obj(IndicatorGroup)
        self.__indicator_serialized = serialized_groups
        indicator_groups = pd.DataFrame(serialized_groups)
        self.__indicator_dropdowns = (
            indicator_groups[["indicator_group", "indicator_name"]]
            .copy()
            .reset_index(drop=True)
        )

    def filter_by_policy(self, policy):
        dropdown_filters = {
            "Correct outliers - using standard deviation": "value_std",
            "Correct outliers - using interquartile range": "value_iqr",
            "Keep outliers": "value_raw",
            "Reporting": "value_rep",
        }
        return self.raw_data.get(dropdown_filters.get(policy)).copy()

    @property
    def indicator_dropdowns(self):
        return self.__indicator_dropdowns

    def get_renaming_dict(
        self,
        rename_from="indicator_id",
        rename_to="indicator_view",
    ):
        return {
            x.get(rename_from): x.get(rename_to) for x in self.__indicator_serialized
        }

    def rename_df_columns(
        self, df, rename_from="indicator_name", rename_to="indicator_view"
    ):
        rename_dict = self.get_renaming_dict(rename_from, rename_to)
        df.rename(columns=rename_dict)
        return df

    def get_indicator_view(
        self, indicator, rename_from="name", rename_to="view", indicator_group=None
    ):
        if indicator_group:
            for x in self.__indicator_serialized:
                if (
                    x.get("indicator_group") == indicator_group
                    and x.get(f"indicator_{rename_from}") == indicator
                ):
                    return x.get(f"indicator_{rename_to}")
        else:
            return self.get_renaming_dict(
                rename_from=f"indicator_{rename_from}",
                rename_to=f"indicator_{rename_to}",
            ).get(indicator)
