#! /usr/bin/python
#
# Title:wx_qreader.py
# Description:poll SQS for fresh file alerts and process file when available
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import json
import os
import sys
import time
import uuid
import yaml

from boto.s3.connection import S3Connection

from boto.sqs.connection import SQSConnection

class WxSqsReader:

    def s3read(self, s3filename, s3bucket):
        print s3filename
        os.chdir(import_path)

        temp = s3filename.split('/')
        fresh_filename = temp[len(temp)-1]

        try:
            s3key = s3bucket.get_key(s3filename)
            s3key.get_contents_to_filename(fresh_filename)
            print "S3 read success %s" % (s3filename)

            command = "%s -xzf %s" % (tar_command, fresh_filename)
            print command
            os.system(command)

            command = "%s -rf %s" % (rm_command, fresh_filename)
            print command
            os.system(command)

            return True
        except:
            print "S3 read failure %s" % (s3filename)

        return False

    def parser(self, message, s3bucket):
        flag = False
#        print message.get_body()
        parsed_json = json.loads(message.get_body())
        event_name = parsed_json['Records'][0]['eventName']
        if event_name == 'ObjectCreated:Put':
            s3_file_object = parsed_json['Records'][0]['s3']['object']
            key = s3_file_object['key']
            if (key.startswith('noaa') is True):
                flag = self.s3read(key, s3bucket)

        return flag

    def queue_poller(self):
        counter = 0

        s3connection = S3Connection()
        s3bucket = s3connection.get_bucket('vocal-digiburo-com')

        qconnection = SQSConnection()
        queue = qconnection.create_queue('vocal-fresh-file')
        results = queue.get_messages(3)
        while (len(results) > 0):
            print "length:%d" % len(results)
            for message in results:
                flag = self.parser(message, s3bucket)
                if flag is True:
                    counter = counter + 1
                    queue.delete_message(message)

            results = queue.get_messages(10)

        return counter

    def execute(self, task_id):
        start_time = time.time()

        counter = self.queue_poller()

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "qreader stop w/population %d and duration %d" % (counter, duration)
        print log_message

print 'start'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        yaml_filename = sys.argv[1]
    else:
        yaml_filename = 'config.yaml'

    configuration = yaml.load(file(yaml_filename))

    rm_command = configuration['rmCommand']
    tar_command = configuration['tarCommand']

    import_path = configuration['importPath']
    root_path = configuration['rootPath']
    noaa_dir = configuration['noaaDir']

    driver = WxSqsReader()
    driver.execute(uuid.uuid4())

print 'stop'
