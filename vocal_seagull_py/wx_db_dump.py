#! /usr/bin/python
#
# Title:wx_db_dump.py
# Description:dump mythic scorer and write to AWS S3
# Development Environment:OS X 10.9.3/Python 2.7.7
# Legalise:Copyright (C) 2014 Digital Burro, INC.
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import os
import sys
import time
import yaml

from mythic_scorer_core import mythic_scorer_sql

from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from boto.s3.key import Key


class DumpDriver:

    def writeToS3(self, outFileName, outFilePath):
        bucketName = "mythic-scorer-%d-%2.2d" % (datetime.datetime.today().year, datetime.datetime.today().month)

        bucketTest = s3connection.lookup(bucketName)
        if bucketTest is None:
            print "must create bucket:%s" % bucketName
            s3connection.create_bucket(bucketName)

        s3bucket = s3connection.get_bucket(bucketName)
        s3key = Key(s3bucket)
        s3key.key = outFileName
        s3key.set_contents_from_filename(outFilePath)

    def execute(self, snapShotDirectory, dumpCommand, gzipCommand, s3connection):
        startTime = time.time()

        outFileName = "sqldump%2.2d" % datetime.datetime.today().day
        outFilePath = "%s/%s" % (snapShotDirectory, outFileName)
        command = "%s -u gsc mythic_scorer > %s" % (dumpCommand, outFilePath)
        os.system(command)

        os.chdir(snapShotDirectory)

        command = "%s %s" % (gzipCommand, outFilePath)
        os.system(command)

        outFileName = "%s.gz" % outFileName
        outFilePath = "%s/%s" % (snapShotDirectory, outFileName)

        self.writeToS3(outFileName, outFilePath)

        stopTime = time.time()
        duration = stopTime - startTime

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

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_hostname = configuration['mySqlHostName']
    mysql_database = configuration['mySqlDataBase']

    driver = DumpDriver()
    duration = driver.execute(uuid.uuid4)

    logMessage = "DumpDriver end w/duration:%d" % duration
    print logMessage

print 'stop'
