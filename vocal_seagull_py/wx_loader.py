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

from wx_db_insert import WxDbInsert
from wx_xml_parser import WxXmlParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class WxLoader:

    def loader(self, session):
        success = 0
        failure = 0

        target_dir = "%s/%s" % (import_path, noaa_dir)

        if os.path.exists(target_dir) is False:
            os.mkdir(target_dir, 0775)

        os.chdir(target_dir)
        targets = os.listdir('.')

        for target in targets:
            print target
            parser = WxXmlParser()
            parser.execute(target)

            inserter = WxDbInsert()
            if inserter.execute(parser.key_value, session):
                success = success+1
            else:
                failure = failure+1

        message = "load complete success:%d failure:%d" % (success, failure)
        print message

        os.chdir(import_path)
        command = "%s -rf %s" % (rm_command, noaa_dir)
        print command
        os.system(command)

        return success

    def execute(self, task_id):
        start_time = time.time()

        mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)
        engine = create_engine(mysql_url, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        population = self.loader(session)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "qreader stop w/population %d and duration %d" % (population, duration)
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

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_hostname = configuration['mySqlHostName']
    mysql_database = configuration['mySqlDataBase']

    driver = WxLoader()
    driver.execute(uuid.uuid4())

print 'stop'
