#!/usr/bin/python
#
# Title:WxCollector.py
# Description: collect weather observations
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import os
import sys
import time
import yaml

class WxCollector:

    def tar_directory(self, time_stamp):
        """
        tar collection directory
        """
        os.chdir(root_dir)

        out_filename = "noaa%d.tgz" % time_stamp
        command = "%s -cvzf %s %s" % (tar_command, out_filename, noaa_dir)
        print(command)
        os.system(command)

        command = "%s -rf %s" % (rm_command, noaa_dir)
        print(command)
        os.system(command)

        return out_filename

    def collection(self, stations):
        """
        collect weather files
        """
        time_now = int(round(time.time()));

        if os.path.exists(noaa_dir) is False:
            os.mkdir(noaa_dir, 0o775)

        os.chdir(noaa_dir)

        for station in stations:
            file_name = "%s.%d" % (station, time_now)
            command = "%s http://w1.weather.gov/xml/current_obs/%s.xml > %s" % (curl_command, station, file_name)
            print(command)
            os.system(command)

        return time_now

    def execute(self):
        """
        prepare for collection
        """
        start_time = time.time()

        stations = [
            'KVBG', 'KNSI', 'KWMC', 'KOTH', 'KPDT', 'KRNO', 'KSBP', 'KPDX', 'KSIY', 'KCIC',
            'KRNM', 'KMUO', 'KGCD', 'KORD', 'KBOK', 'KHAF', 'KCVO', 'KOMA', 'KPIR', 'KONP',
            'KEUG', 'KRDD', 'KSBA', 'KCOE', 'KKLS', 'KACV', 'KCLM', 'KRBL', 'KSLC', 'KUKI',
            'KMSP', 'KSEA', 'KELN', 'KSTS', 'KRKS', 'KUAO', 'KDLS', 'KCCR', 'KEKO', 'KELY',
            'KMHR', 'KOAK', 'KBDN', 'KSQL', 'KDEN', 'KSFO', 'KMAN', 'KMSN', 'KAVX', 'KLMT',
            'KRAP', 'KRHV', 'KBNO', 'KHIF', 'KLAX', 'KSUX', 'KHWD', 'KSLE', 'KOLM', 'KMFR',
            'KBOI', 'KRBG', 'KRCA', 'KONO', 'KBHB', 'KRDM', 'KCLS', 'KPAE', 'KIDA', 'KSCK',
            'KLKV', 'KLAS', 'KNUC', 'KCEC', 'KLWS', 'KPRB', 'KHIO', 'KLOL', 'KSUU', 'KPVU',
            'KSKA', 'KSXT', 'KTWF', 'KSJC', 'KMYF', 'KENV', 'KAPC', 'KMRY', 'KPAO', 'KREO',
            'KSTL', 'KAAT', 'KFOT', 'PAJN', 'PANC'
        ]

        time_stamp = self.collection(stations)
        self.tar_directory(time_stamp)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "collection stop w/time_stamp %d and duration %d" % (time_stamp, duration)
        print(log_message)

print('start WxCollector')

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        fileName = "config.yaml"

    with open(fileName, 'r') as stream:
        try:
            configuration = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    curl_command = configuration['curlCommand']
    rm_command = configuration['rmCommand']
    tar_command = configuration['tarCommand']

#    export_path = configuration['exportPath']
    root_dir = configuration['rootDir']
    noaa_dir = configuration['noaaDir']

    driver = WxCollector()
    driver.execute()

print('stop WxCollector')

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
