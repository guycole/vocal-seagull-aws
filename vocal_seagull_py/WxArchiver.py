#!/usr/bin/python
#
# Title:WxArchiver.py
# Description: tar daily weather collection and write to S3
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import os
import sys
import yaml

from boto.exception import S3ResponseError

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class WxArchiver:

    def tar_directory(self, command):
        os.chdir(seagull_path)
        os.system(command)

        cleanup = "%s -rf %s" % (rm_command, seagull_dir)
        os.system(cleanup)

        os.mkdir(seagull_dir, 0775)

    def s3write(self, out_filename, out_filepath):
        tweaked_key = "noaa-%d-%2.2d/%s" % (datetime.datetime.today().year, datetime.datetime.today().month, out_filename)

        s3key = Key(s3bucket)
        s3key.key = tweaked_key
        s3key.set_contents_from_filename(out_filepath)

    def execute(self):
        """
        discover, parse and load weather files
        """
        out_filename = "noaa-%d-%2.2d-%2.2d.tgz" % (datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day)
        command = "%s -cvzf %s %s" % (tar_command, out_filename, seagull_dir)
        self.tar_directory(command)

        out_filepath = "%s/%s" % (seagull_path, out_filename)
        self.s3write(out_filename, out_filepath)

        os.unlink(out_filepath)

print 'start WxParserLoader'

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
    tar_command = configuration['tarCommand']

    seagull_path = configuration['seagullPath']
    seagull_dir = configuration['seagullDir']

    aws_accesskey = configuration['awsAccessKey']
    aws_secretkey = configuration['awsSecretKey']

    s3connection = S3Connection(aws_accesskey, aws_secretkey)

    try:
        s3bucket = s3connection.get_bucket('vocal-digiburo-com')

        driver = WxArchiver()
        driver.execute()
    except:
        print 'exception'
    finally:
        print 'finally'

print 'stop WxParserLoader'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
