#! /usr/bin/python3
#
# Title:wx_loader.py
# Description:poll SQS for fresh file alerts and process file when available
# Development Environment:OS X 10.10.5/Python 3
# Author:G.S. Cole (guycole at gmail dot com)
#
import os
import sys
import time
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class WxLoader:

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
                os.system(command)

    def execute(self):
        start_time = time.time()

        db_url = 'postgresql://seagull:bogus@localhost/vocal_seagull'

        db_url = "postgresql://%s:%s@%s/%s" % (db_user_name, db_pass_word, db_host_name, db_data_base)

        engine = create_engine(db_url, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        self.discover_tar(session)

        stop_time = time.time()
        duration = stop_time - start_time
        log_message = "WxLoader stop w/duration %d" % duration
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

    db_data_base = configuration['dbDataBase']
    db_host_name = configuration['dbHostName']
    db_pass_word = configuration['dbPassWord']
    db_user_name = configuration['dbUserName']

    driver = WxLoader()
    driver.execute()

print('stop WxLoader')

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
