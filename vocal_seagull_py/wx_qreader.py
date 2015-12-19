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

from aws_utility import AwsUtility

from wx_loader import WxLoader
from wx_xml_parser import WxXmlParser

import boto.sqs

from boto.s3.connection import S3Connection

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class WxSqsReader:

    def s3read(self, s3_filename, s3bucket):
        os.chdir(loader_dir)

        temp = s3_filename.split('/')
        fresh_filename = temp[len(temp)-1]

        try:
            s3key = s3bucket.get_key(s3_filename)
            s3key.get_contents_to_filename(fresh_filename)
            print "S3 read success %s" % (s3_filename)

            command = "%s -xzf %s" % (tar_command, fresh_filename)
            print command
            os.system(command)

            command = "%s -rf %s" % (rm_command, fresh_filename)
            print command
            os.system(command)

            return True
        except:
            print "S3 read failure %s" % (s3_filename)

        return False

    def queue_poller(self, bucket_name, queue_name):
        s3connection = S3Connection(aws_accesskey, aws_secretkey)
        s3bucket = s3connection.get_bucket(bucket_name)

        sqs_connection = boto.sqs.connect_to_region(aws_region, aws_access_key_id=aws_accesskey, aws_secret_access_key=aws_secretkey)
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
                    flag = self.s3read(key, s3bucket)
                    if flag is True:
                        queue.delete_message(message)
                        counter = counter + 1

            results = queue.get_messages(10)

        return counter

    def loader(self, session):
        os.chdir("%s/noaa" % (loader_dir))
        targets = os.listdir('.')

        success = 0
        failure = 0

        for target in targets:
            print target
            parser = WxXmlParser()
            parser.execute(target)

            loader = WxLoader()
            if loader.execute(parser.key_value, session):
                success = success+1
            else:
                failure = failure+1

        message = "load complete success:%d failure:%d" % (success, failure)
        print message

    def execute(self, task_id):
        start_time = time.time()

        aws = AwsUtility(aws_region, aws_accesskey, aws_secretkey)
        aws.log_writer(task_id, 'info', 'vocal.seagull', 'qreader start')

        population = self.queue_poller('vocal-digiburo-com', 'vocal-fresh-file')

        mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)

        engine = create_engine(mysql_url, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        self.loader(session)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "qreader stop w/population %d and duration %d" % (population, duration)
        aws.log_writer(task_id, 'info', 'vocal.seagull', log_message)

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

    aws_region = configuration['awsRegion']
    aws_accesskey = configuration['awsAccessKey']
    aws_secretkey = configuration['awsSecretKey']

    rm_command = configuration['rmCommand']
    tar_command = configuration['tarCommand']

    loader_dir = configuration['loaderDir']

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_hostname = configuration['mySqlHostName']
    mysql_database = configuration['mySqlDataBase']

    duration = 0

    driver = WxSqsReader()
    driver.execute(uuid.uuid4())

print 'stop'
