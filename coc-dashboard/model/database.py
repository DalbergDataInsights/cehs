from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
import json

Base = declarative_base()


class Population(Base):

    __tablename__ = "population"

    id = Column(Integer, primary_key=True, autoincrement=True)
    district_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    male = Column(Integer)
    female = Column(Integer)
    total = Column(Integer)
    childbearing_age = Column(Integer)
    pregnant = Column(Integer)
    not_pregnant = Column(Integer)
    births = Column(Integer)
    u1 = Column(Integer)
    u5 = Column(Integer)
    u15 = Column(Integer)
    suspect_tb = Column(Integer)

    def serialize(self):
        return {
            "id": self.district_name,
            "year": self.year,
            "female": self.female,
            "total": self.total,
            "childbearing_age": self.childbearing_age,
            "pregnant": self.pregnant,
            "not_pregnant": self.not_pregnant,
            "births": self.births,
            "u1": self.u1,
            "u5": self.u5,
            "u15": self.u15,
            "suspect_tb": self.suspect_tb,
        }


class IndicatorGroup(Base):

    __tablename__ = "indicator_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_group = Column(String, nullable=False)
    indicator_name = Column(String, nullable=False)
    indicator_view = Column(String, nullable=False)

    def serialize(self):
        return {
            "indicator_id": self.id,
            "indicator_group": self.indicator_group,
            "indicator_name": self.indicator_name,
            "indicator_view": self.indicator_view,
        }


class FetchDate(Base):

    __tablename__ = "fetch_date"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    def serialize(self):
        return self.date


class PopulationTarget(Base):

    __tablename__ = "population_target"
    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_name = Column(String)
    cat = Column(String)

    def serialize(self):
        return {"indicator": self.indicator_name, "cat": self.cat}
