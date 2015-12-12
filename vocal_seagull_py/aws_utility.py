#
# Title:aws_utility.py
# Description:
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import json
import time

from email import utils

import boto.sqs

from boto import connect_sqs
from boto.sqs.message import RawMessage

from boto.exception import S3ResponseError

from boto.s3.connection import S3Connection
from boto.s3.key import Key


class AwsUtility:

    def __init__(self, aws_region, aws_accesskey, aws_secretkey):
        self.region = aws_region
        self.accesskey = aws_accesskey
        self.secretkey = aws_secretkey

    def rfc822_now(self):
        now_tuple = datetime.datetime.now().timetuple()
        now_time = time.mktime(now_tuple)
        return utils.formatdate(now_time)

    def log_payload(self, task_id, priority, facility, message):
        data = {
            'time_stamp_rfc822': self.rfc822_now(),
            'task_id': str(task_id),
            'priority': str(priority),
            'facility': str(facility),
            'message': str(message)
        }

        message = RawMessage()
        message.set_body(json.dumps(data))
        return message

    def log_writer(self, task_id, priority, facility, message):
        payload = self.log_payload(task_id, priority, facility, message)
        connection = boto.sqs.connect_to_region(self.region, aws_access_key_id=self.accesskey, aws_secret_access_key=self.secretkey)
        qqq = connection.create_queue('greasy-tool')
        status = qqq.write(payload)

    def s3writer(self, bucket_name, remote_filename, local_filename):
        s3connection = S3Connection(self.accesskey, self.secretkey)
        s3bucket = s3connection.get_bucket(bucket_name)

        s3key = Key(s3bucket)
        s3key.key = remote_filename
        s3key.set_contents_from_filename(local_filename)