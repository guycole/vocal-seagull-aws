#!/usr/bin/python
#
# Title:WxWriter.py
# Description: write weather observations to S3
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import os
import sys
import time
import uuid
import yaml

from boto.exception import S3ResponseError

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class WxWriter:

    def execute(self, task_id):
        """
        write outbound S3 files
        """
        start_time = time.time()
    
        os.chdir(export_path)
        
        files = os.listdir('.')
        for filename in files:
            print filename

            s3directory = "noaa/noaa-%d-%2.2d" % (datetime.datetime.today().year, datetime.datetime.today().month)
            s3filename = "%s/%s" % (s3directory, filename)

            s3connection = S3Connection()
            s3bucket = s3connection.get_bucket('vocal-digiburo-com')

            s3key = Key(s3bucket)
            s3key.key = s3filename
            s3key.set_contents_from_filename(filename)

            os.unlink(filename)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "stop w/duration %d" % (duration)
        print log_message

print 'start WxWriter'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        fileName = "config.yaml"

    configuration = yaml.load(file(fileName))

    rm_command = configuration['rmCommand']

    export_path = configuration['exportPath']
    root_path = configuration['rootPath']

    driver = WxWriter()
    driver.execute(uuid.uuid4())

print 'stop WxWriter'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
