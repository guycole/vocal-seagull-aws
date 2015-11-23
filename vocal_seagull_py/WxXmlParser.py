#
# Title:WxXmlParser.py
# Description:read and parse a weather service XML file
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import sys
import xml.parsers.expat

class WxXmlParser:
    buffer = 'xxx'

    def __init__(self):
        self.key_value = {}
        self.key_value['station_id'] = ''

    def start_element(self, name, attrs):
        """
        start of XML tag
        """
#        print 'start:', name, attrs

    def end_element(self, name):
        """
        ending XML tag
        """
        if name == 'credit':
            return

        if name == 'credit_URL':
            return

        if name == 'url':
            return

        if name == 'title':
            return

        if name == 'link':
            return

        if name == 'image':
            return

        if name == 'suggested_pickup':
            return

        if name == 'suggested_pickup_period':
            return

        if name == 'location':
            self.key_value[name] = self.buffer
            return

        if name == 'station_id':
            self.key_value[name] = self.buffer
            return

        if name == 'latitude' or name == 'longitude':
            self.key_value[name] = self.buffer
            return

        if name == 'observation_time':
            return

        if name == 'observation_time_rfc822':
            self.key_value[name] = self.buffer
            return

        if name == 'weather':
            self.key_value[name] = self.buffer
            return

        if name == 'temperature_string':
            return

        if name == 'temp_c' or name == 'temp_f':
            self.key_value[name] = self.buffer
            return

        if name == 'relative_humidity':
            self.key_value[name] = self.buffer
            return

        if name == 'wind_string':
            return

        if name == 'wind_dir':
            return

        if name == 'wind_degrees':
            self.key_value[name] = self.buffer
            return

        if name == 'wind_mph' or name == 'wind_kt':
            self.key_value[name] = self.buffer
            return

        if name == 'wind_gust_mph' or name == 'wind_gust_kt':
            self.key_value[name] = self.buffer
            return

        if name == 'pressure_string':
            return

        if name == 'pressure_mb' or name == 'pressure_in':
            self.key_value[name] = self.buffer
            return

        if name == 'dewpoint_string':
            return

        if name == 'dewpoint_f' or name == 'dewpoint_c':
            self.key_value[name] = self.buffer
            return

        if name == 'windchill_string':
            return

        if name == 'windchill_f' or name == 'windchill_c':
            self.key_value[name] = self.buffer
            return

        if name == 'heat_index_string':
            return

        if name == 'heat_index_f' or name == 'heat_index_c':
            self.key_value[name] = self.buffer
            return

        if name == 'visibility_mi':
            self.key_value[name] = self.buffer
            return

        if name == 'icon_url_base':
            return

        if name == 'two_day_history_url':
            return

        if name == 'icon_url_name':
            return

        if name == 'ob_url':
            return

        if name == 'disclaimer_url':
            return

        if name == 'copyright_url':
            return

        if name == 'privacy_policy_url':
            return

        if name == 'current_observation':
            return

        print "unknown name:%s" % (name)

    def char_data(self, data):
        """
        text between start and end tag
        """
#        self.buffer = repr(data)
        self.buffer = data

    def execute(self, file_name):
        """
        read and parse XML file
        """
        in_file = open(file_name, 'r')
        raw_xml = in_file.read()
        in_file.close()

        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        p.Parse(raw_xml)

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
