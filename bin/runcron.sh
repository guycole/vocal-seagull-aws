#!/bin/bash
#
# Title:runcron.sh
#
# Description:
#   cron job
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
docker run -d --rm -v /var/vocal/seagull:/var/vocal/seagull vocal-seagull
#
