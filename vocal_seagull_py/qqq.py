#
# Title:qreader.py
# Description: poll SQS for a fresh file, read and untar
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import json
import os

import boto.sqs

from boto.s3.connection import S3Connection

class WxSqsReader:

    def __init__(self, aws_region, aws_accesskey, aws_secretkey, tar_command, rm_command):
        self.region = aws_region
        self.accesskey = aws_accesskey
        self.secretkey = aws_secretkey
        self.tar_command = tar_command
        self.rm_command = rm_command

    def s3read(self, s3_filename, s3bucket, loader_dir):
        os.chdir(loader_dir)

        temp = s3_filename.split('/')
        fresh_filename = temp[len(temp)-1]

        try:
            s3key = s3bucket.get_key(s3_filename)
            s3key.get_contents_to_filename(fresh_filename)
            print "S3 read success %s" % (s3_filename)

            command = "%s -xzf %s" % (self.tar_command, fresh_filename)
            print command
            os.system(command)

            command = "%s -rf %s" % (self.rm_command, fresh_filename)
            print command
            os.system(command)

            return True
        except:
            print "S3 read failure %s" % (s3_filename)

        return False

    def queue_poller(self, bucket_name, queue_name, loader_dir):
        s3connection = S3Connection(self.accesskey, self.secretkey)
        s3bucket = s3connection.get_bucket(bucket_name)

        sqs_connection = boto.sqs.connect_to_region(self.region, aws_access_key_id=self.accesskey, aws_secret_access_key=self.secretkey)
        queue = sqs_connection.create_queue(queue_name)

        counter = 0
        results = queue.get_messages(10)
        while (len(results) > 0):
            for message in results:
                parsed_json = json.loads(message.get_body())
                event_name = parsed_json['Records'][0]['eventName']
                if event_name == 'ObjectCreated:Put':
                    s3_file_object = parsed_json['Records'][0]['s3']['object']
                    key = s3_file_object['key']
                    flag = self.s3read(key, s3bucket, loader_dir)
                    if flag is True:
                        queue.delete_message(message)
                        counter = counter + 1

            results = queue.get_messages(10)

        return counter