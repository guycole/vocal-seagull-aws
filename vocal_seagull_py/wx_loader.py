#! /usr/bin/python
#
# Title:wx_loader.py
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

from wx_qreader import WxSqsReader
from wx_db_insert import WxDbInsert
from wx_xml_parser import WxXmlParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class WxLoader:

    def loader(self, session):
        success = 0
        failure = 0

        os.chdir("%s/noaa" % (loader_dir))
        targets = os.listdir('.')

        for target in targets:
            print target
            parser = WxXmlParser()
            parser.execute(target)

            loader = WxDbInsert()
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

        sqsReader = WxSqsReader(aws_region, aws_accesskey, aws_secretkey, tar_command, rm_command)
        population = sqsReader.queue_poller('vocal-digiburo-com', 'vocal-fresh-file', loader_dir)

        print "population:%d" % (population)
        population = 1
        if (population > 0):
            mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)

            engine = create_engine(mysql_url, echo=False)
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

    driver = WxLoader()
    driver.execute(uuid.uuid4())

print 'stop'