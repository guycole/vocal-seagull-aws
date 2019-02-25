#! /usr/bin/python3
#
# Title:wx_loader.py
# Description:poll SQS for fresh file alerts and process file when available
# Development Environment:OS X 10.10.5/Python 3
# Author:G.S. Cole (guycole at gmail dot com)
#
import json
import os
import sys
import time
import uuid
import yaml

from wx_db_insert import WxDbInsert
from wx_xml_parser import WxXmlParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class WxLoader:


    def loader2(self, session):
        success = 0
        failure = 0

        os.chdir(import_dir)
        targets = os.listdir('.')

        for target in targets:
            print(target)
            command = "%s -xf %s" % (tar_command, target)
            print(command)
            os.system(command)

#            parser = WxXmlParser()
#            parser.execute(target)

#            inserter = WxDbInsert()
#            if inserter.execute(parser.key_value, session):
#                success = success+1
#            else:
#                failure = failure+1

        message = "load complete success:%d failure:%d" % (success, failure)
        print(message)

        os.chdir(import_dir)
#        command = "%s -rf %s" % (rm_command, noaa_dir)
#        print(command)
#        os.system(command)

        return success

    def loader(self, target, session):
        print(target)

        parser = WxXmlParser()
        parser.execute(target)
        print(parser.key_value)

        inserter = WxDbInsert()
        inserter.execute(parser.key_value, session)

    def process_tar(self, target, session):
        command = "%s -xf %s" % (tar_command, target)
        print(command)
        os.system(command)

        for root, subdirs, files in os.walk(import_dir):
            if root.endswith('noaa'):
                for target in files:
                    full_name = "%s/%s" % (root, target)
                    self.loader(full_name, session)

                    command = "%s -rf %s" % (rm_command, full_name)
                    print(command)
                    os.system(command)

    def discover_tar(self, session):
        os.chdir(import_dir)
        targets = os.listdir('.')
        for target in targets:
            if target.endswith('.tgz'):
                self.process_tar(target, session)

                command = "%s -rf %s" % (rm_command, target)
                print(command)
#                os.system(command)

    def execute(self):
        start_time = time.time()

#        mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)
#        engine = create_engine(mysql_url, echo=False)
#        Session = sessionmaker(bind=engine)
#        session = Session()
        session = None

        population = 0
#        population = self.loader(session)
        self.discover_tar(session)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "WxLoader stop w/population %d and duration %d" % (population, duration)
        print(log_message)

print('start WxLoader')

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

    rm_command = configuration['rmCommand']
    tar_command = configuration['tarCommand']

    import_dir = configuration['importDir']
    noaa_dir = configuration['noaaDir']

    driver = WxLoader()
    driver.execute()

print('stop WxLoader')

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
