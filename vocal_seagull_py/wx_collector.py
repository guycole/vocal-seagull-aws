#!/usr/bin/python
#
# Title:WxCollector.py
# Description: collect weather observations
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import os
import sys
import time
import uuid
import yaml

from aws_utility import AwsUtility

class WxCollector:

    def tar_directory(self, time_stamp):
        """
        tar collection directory
        """
        os.chdir(seagull_path)

        out_filename = "noaa%d.tgz" % (time_stamp)
        command = "%s -cvzf /tmp/%s %s" % (tar_command, out_filename, seagull_dir)
        print command
        os.system(command)

        command = "%s -rf %s" % (rm_command, seagull_dir)
        print command
        os.system(command)

        return out_filename

    def archiver(self, time_stamp):
        """
        tar collected files and write to S3
        """
        tar_filename = self.tar_directory(time_stamp)

        s3directory = "noaa/noaa-%d-%2.2d" % (datetime.datetime.today().year, datetime.datetime.today().month)
        s3filename = "%s/%s" % (s3directory, tar_filename)

        os.chdir('/tmp')

        aws = AwsUtility(aws_region, aws_accesskey, aws_secretkey)
        aws.s3writer('vocal-digiburo-com', s3filename, tar_filename)

        os.unlink(tar_filename)

    def collection(self, stations):
        """
        collect weather files
        """
        time_now = int(round(time.time()));

        collection_dir = "%s/%s" % (seagull_path, seagull_dir)

        if os.path.exists(collection_dir) is False:
            os.mkdir(collection_dir, 0775)

        os.chdir(collection_dir)

        for station in stations:
            file_name = "%s.%d" % (station, time_now)
            command = "%s http://w1.weather.gov/xml/current_obs/%s.xml > %s" % (curl_command, station, file_name)
            print command
            os.system(command)

        return time_now

    def execute(self, task_id):
        """
        prepare for collection
        """
        start_time = time.time()

        aws = AwsUtility(aws_region, aws_accesskey, aws_secretkey)
        aws.log_writer(task_id, 'info', 'vocal.seagull', 'collection start')

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
        self.archiver(time_stamp)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "collection stop w/time_stamp %d and duration %d" % (time_stamp, duration)
        aws.log_writer(task_id, 'info', 'vocal.seagull', log_message)

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
    rm_command = configuration['rmCommand']
    tar_command = configuration['tarCommand']

    seagull_path = configuration['seagullPath']
    seagull_dir = configuration['seagullDir']

    driver = WxCollector()
    driver.execute(uuid.uuid4())

print 'stop WxCollector'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
