# vocal-seagull-aws
Vocal Seagull collects weather observations from the US NOAA (http://weather.noaa.gov) and stores the results in MySQL (implemented w/python).

* wx_collector.py is invoked from cron(8) periodically to collect the current weather observations and save them to a file.  AWS S3 will store the collected files (written as a tar.gz).  AWS SQS is used to report the job start/stop.
* wx_loader.py reads the tar.gz file from AWS S3, parses each observation and loads into MySQL.  wx_loader.py is also invoked from cron(8) and discovers fresh S3 files by reading from AWS SQS. 
* AWS S3 is configured to write to AWS SQS each time a fresh file is placed within the vocal bucket.
