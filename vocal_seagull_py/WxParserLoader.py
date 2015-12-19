#!/usr/bin/python
#
# Title:WxParserLoader.py
# Description: parse raw weather files and load into MySQL
# Development Environment:OS X 10.8.5/Python 2.7.2
# Author:G.S. Cole (guycole at gmail dot com)
#
import os
import sys
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wx_loader import WxLoader
from wx_xml_parser import WxXmlParser

class WxParserLoader:

    def execute(self):
        """
        discover, parse and load weather files
        """
        success = 0
        failure = 0

        collection_dir = "%s/%s" % (seagull_path, seagull_dir)

        targets = os.listdir(collection_dir)
        for target in targets:
            file_name = "%s/%s" % (collection_dir, target)

            parser = WxXmlParser()
            parser.execute(file_name)

            loader = WxLoader()
            if loader.execute(parser.key_value, session):
                success = success+1
            else:
                failure = failure+1

        print "end success:%d failure:%d" % (success, failure)

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

    seagull_path = configuration['seagullPath']
    seagull_dir = configuration['seagullDir']

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_database = configuration['mySqlDataBase']
    mysql_hostname = configuration['mySqlHostName']

    mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)

    engine = create_engine(mysql_url, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        wxParserLoader = WxParserLoader()
        wxParserLoader.execute()
    except:
        print 'exception'
    finally:
        print 'finally'

print 'stop WxParserLoader'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***