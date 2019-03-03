#
# Title:wx_db_insert.py
# Description: load an observation into database
# Development Environment:OS X 10.8.5/Python 3
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import email.utils

from sql_table import RawObservation

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WxDbInsert:

    def converter(self, observation, key):
        try :
            return observation[key].strip()
        except:
            return ''

    def execute(self, observation, session):
        station_id = observation['station_id']
        if len(station_id) < 1:
            return False

        raw_time = observation['observation_time_rfc822']
        parsed_time = email.utils.parsedate_to_datetime(raw_time)

        selected_set = session.query(RawObservation).filter_by(station = station_id, date = parsed_time).all()
        for selected in selected_set:
            return False

        obs = RawObservation(station_id, parsed_time)
        obs.location = self.converter(observation, 'location')
        obs.latitude = self.converter(observation, 'latitude')
        obs.longitude = self.converter(observation, 'longitude')
        obs.rfc822 = self.converter(observation, 'observation_time_rfc822')
        obs.temp_c = self.converter(observation, 'temp_c')
        obs.temp_f = self.converter(observation, 'temp_f')
        obs.dewpoint_c = self.converter(observation, 'dewpoint_c')
        obs.dewpoint_f = self.converter(observation, 'dewpoint_f')
        obs.relative_humidity = self.converter(observation, 'relative_humidity')
        obs.visibility_mi = self.converter(observation, 'visibility_mi')
        obs.weather = self.converter(observation, 'weather')
        obs.wind_degrees = self.converter(observation, 'wind_degrees')
        obs.wind_kt = self.converter(observation, 'wind_kt')
        obs.wind_mph = self.converter(observation, 'wind_mph')
        obs.pressure_in = self.converter(observation, 'pressure_in')
        obs.pressure_mb = self.converter(observation, 'pressure_mb')
        obs.heat_index_c = self.converter(observation, 'heat_index_c')
        obs.heat_index_f = self.converter(observation, 'heat_index_f')
        obs.wind_chill_c = self.converter(observation, 'windchill_c')
        obs.wind_chill_f = self.converter(observation, 'windchill_f')
        obs.wind_gust_kt = self.converter(observation, 'wind_gust_kt')
        obs.wind_gust_mph = self.converter(observation, 'wind_gust_mph')

        session.add(obs)
        session.commit()

        return True

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
