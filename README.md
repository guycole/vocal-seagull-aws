# vocal-seagull-aws
Vocal Seagull collects weather observations from the US NOAA (http://weather.noaa.gov) and stores the results in MySQL (implemented w/python).

* wx_collector.py is invoked from cron(8) periodically to collect the current weather observations and save them to a file.  
* wx_loader.py parses each observation file and loads into PostGreSQL.  