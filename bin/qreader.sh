#!/bin/bash
#
# Title:qreader.sh
#
# Description:
#   read SQS to discover fresh S3 files
#
# Development Environment:
#   OS X 10.10.5
#
# Author:
#   G.S. Cole (guycole at gmail dot com)
#
# Maintenance History:
#   $Id$
#
#   $Log$
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
PYTHONPATH=/Users/gsc/PycharmProjects/vocal-seagull-aws; export PYTHONPATH
#
#AWS_ACCESS_KEY_ID = "bogus"; export AWS_ACCESS_KEY_ID
#AWS_SECRET_ACCESS_KEY = "bogus"; export AWS_SECRET_ACCESS_KEY
#
/Users/gsc/PycharmProjects/vocal-seagull-aws/vocal_seagull_py/wx_qreader.py /var/vocal/config.yaml
#