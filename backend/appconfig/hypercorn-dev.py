#!/usr/bin/env python3
# -*- coding: utf-8 -*-

loglevel = "debug"
workers = 4
bind = "0.0.0.0:8943"
insecure_bind = "0.0.0.0:8980"
graceful_timeout = 120
worker_class = "uvloop"
keepalive = 5
errorlog = "/Users/zhangjun/PycharmProjects/CapricornusNG/backend/log/hypercorn_error.log"
accesslog = "/Users/zhangjun/PycharmProjects/CapricornusNG/backend/log/hypercorn_access.log"
keyfile = "/Users/zhangjun/PycharmProjects/CapricornusNG/backend/cert/key.pem"
certfile = "/Users/zhangjun/PycharmProjects/CapricornusNG/backend/cert/cert.pem"