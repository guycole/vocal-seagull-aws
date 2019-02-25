#!/bin/bash
#
# Title:runner.sh
#
# Description:
#   drive vocal seagull collection and cycle
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
#PYTHONPATH=/Users/gsc/PycharmProjects/vocal-seagull-aws; export PYTHONPATH
#
#AWS_ACCESS_KEY_ID = "bogus"; export AWS_ACCESS_KEY_ID
#AWS_SECRET_ACCESS_KEY = "bogus"; export AWS_SECRET_ACCESS_KEY
#
#/vocal-seagull-aws/vocal_seagull_py/wx_collector.py /vocal-seagull-aws/seagull/prod.yaml
/vocal-seagull-aws/vocal_seagull_py/wx_loader.py /vocal-seagull-aws/seagull/prod.yaml
#
