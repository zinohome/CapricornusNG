#!/usr/bin/env python3
# -*- coding: utf-8 -*-

bind = '0.0.0.0:8843'
backlog = 512
chdir = '/opt/Capricornus'
timeout = 300
worker_class = 'uvicorn.workers.UvicornWorker'
workers = 2
threads = 5
loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "/opt/Capricornus/log/gunicorn_access.log"
errorlog = "/opt/Capricornus/log/gunicorn_error.log"
keyfile = "/opt/Capricornus/cert/key.pem"
certfile = "/opt/Capricornus/cert/cert.pem"
"""
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
