#! /usr/bin/python
#
# Title:wx_db_dump.py
# Description:dump vocal seagull and write to AWS S3
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import os
import sys
import time
import uuid
import yaml

from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from boto.s3.key import Key


class DumpDriver:

    def execute(self, task_id):
        start_time = time.time()

        dump_name = "seagull-%d-%2.2d-%2.2d.sql.gz" % (datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
        dump_path = "%s/%s" % (snapshot_dir, dump_name)
        command = "%s -u %s -p%s %s | %s > %s" % (dump_command, mysql_username, mysql_password, mysql_database, gzip_command, dump_path)
        print command
        os.system(command)

        s3directory = 'dbdump-digiburo-com'
        s3filename = "%s/%s" % (s3directory, dump_name)

        s3connection = S3Connection()
        s3bucket = s3connection.get_bucket('dbdump-digiburo-com')

        s3key = Key(s3bucket)
        s3key.key = dump_name
        s3key.set_contents_from_filename(dump_path)

        os.unlink(dump_path)

        stop_time = time.time()
        duration = stop_time - start_time

        return duration

print 'start'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        yamlFileName = sys.argv[1]
    else:
        yamlFileName = 'config.yaml'

    configuration = yaml.load(file(yamlFileName))

    dump_command = configuration['dumpCommand']
    gzip_command = configuration['gzipCommand']
    rm_command = configuration['rmCommand']

    snapshot_dir = configuration['snapShotPath']

    mysql_username = configuration['mySqlDumpUserName']
    mysql_password = configuration['mySqlDumpPassWord']
    mysql_hostname = configuration['mySqlDumpHostName']
    mysql_database = configuration['mySqlDumpDataBase']

    driver = DumpDriver()
    duration = driver.execute(uuid.uuid4)

    log_message = "DumpDriver end w/duration:%d" % duration
    print log_message

print 'stop'
