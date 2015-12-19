#
# Title:sqltable.py
# Description:
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime

from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Observation(Base):
    __tablename__ = 'observation'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    station = Column(String)
    location = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    rfc822 = Column(String)
    temp_c = Column(String)
    temp_f = Column(String)
    dewpoint_c = Column(String)
    dewpoint_f = Column(String)
    relative_humidity = Column(String)
    visibility_mi = Column(String)
    weather = Column(String)
    wind_degrees = Column(String)
    wind_kt = Column(String)
    wind_mph = Column(String)
    pressure_in = Column(String)
    pressure_mb = Column(String)
    heat_index_c = Column(String)
    heat_index_f = Column(String)
    windchill_c = Column(String)
    windchill_f = Column(String)
    wind_gust_kt = Column(String)
    wind_gust_mph = Column(String)

    def __init__(self, station, time_stamp):
        self.station = station
        self.time_stamp = time_stamp
        self.location = ''
        self.latitude = ''
        self.longitude = ''
        self.rfc822 = ''
        self.temp_c = ''
        self.temp_f = ''
        self.dewpoint_c = ''
        self.dewpoint_f = ''
        self.relative_humidity = ''
        self.visibility_mi = ''
        self.weather = ''
        self.wind_degrees = ''
        self.wind_kt = ''
        self.wind_mph = ''
        self.pressure_in = ''
        self.pressure_mb = ''
        self.heat_index_c = ''
        self.heat_index_f = ''
        self.windchill_c = ''
        self.windchill_f = ''
        self.wind_gust_kt = ''
        self.wind_gust_mph = ''

    def __repr__(self):
        return "<observation(%d, %s)>" % (self.id, self.station)