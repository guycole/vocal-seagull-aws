#!/usr/bin/python
#
# Title:WxCollector.py
# Description: Collect stations contained in stations.dat
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import os
import sys
import time
import yaml

from os import system

class WxCollector:

    def collection(self, stations):
        """
        collect weather files
        """
        time_now = int(round(time.time()));

        os.chdir(collected_dir)

        for station in stations:
            file_name = "%s.%d" % (station, time_now)
            command = "%s %s%s.xml > %s" % (curl, base_url, station, file_name)
            system(command)

    def execute(self):
        """
        prepare for collection
        """
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

        self.collection(stations)

print 'start WxCollector'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        fileName = "config.yaml"

    configuration = yaml.load(file(fileName))

    collected_dir = configuration['collectedDir']
    curl = configuration['curl']
    base_url = configuration['baseUrl']

    collector = WxCollector()
    collector.execute()

print 'stop WxCollector'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
