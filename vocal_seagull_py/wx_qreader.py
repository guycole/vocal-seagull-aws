#
# Title:qreader.py
# Description:
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
class WxSqsReader:

    def s3read(self, s3_filename, s3bucket):
        os.chdir(loader_directory)

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