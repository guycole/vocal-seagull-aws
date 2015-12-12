#!/usr/bin/python
#
# Title:WxCollector.py
# Description: collect weather observations
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import json
import os
import rfc822
import sys
import time
import uuid
import yaml

from email import utils

from os import system

from boto import connect_sqs
from boto.sqs.message import RawMessage

class WxCollector:
    def rfc822_now(self):
        now_tuple = datetime.datetime.now().timetuple()
        now_time = time.mktime(now_tuple)
        return utils.formatdate(now_time)

    def log_payload(self, task_id, priority, facility, message):
        data = {
            'time_stamp_rfc822': self.rfc822_now(),
            'task_id': str(task_id),
            'priority': str(priority),
            'facility': str(facility),
            'message': str(message)
        }

        message = RawMessage()
        message.set_body(json.dumps(data))
        return message
    
    def q_lookup(self, q_name):
        sqs_connection = connect_sqs(aws_accesskey, aws_secretkey)
        return sqs_connection.lookup(q_name)

    def q_writer(self, qqq, payload):
        status = qqq.write(payload)

    def collection(self, stations):
        """
        collect weather files
        """
        time_now = int(round(time.time()));

        collection_dir = "%s/%s" % (seagull_path, seagull_dir)
        os.chdir(collection_dir)

        for station in stations:
            file_name = "%s.%d" % (station, time_now)
            command = "%s http://w1.weather.gov/xml/current_obs/%s.xml > %s" % (curl_command, station, file_name)
            print command
            system(command)

    def execute(self, task_id):
        start_time = time.time()

        qqq = self.q_lookup('greasy-tool')

        payload = self.log_payload(task_id, 'info', 'vocal.seagull', 'application start')
        self.q_writer(qqq, payload)
        
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

        stop_time = time.time()
        return stop_time - start_time

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

    aws_region = configuration['awsRegion']
    aws_accesskey = configuration['awsAccessKey']
    aws_secretkey = configuration['awsSecretKey']

    curl_command = configuration['curlCommand']

    seagull_path = configuration['seagullPath']
    seagull_dir = configuration['seagullDir']

#    try:
    driver = WxCollector()
    driver.execute(uuid.uuid4())
#    except:
#        print 'exception'
#    finally:
#        print 'finally'

print 'stop WxCollector'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
