#!/usr/bin/env python3
# -*- coding: utf-8 -*-

loglevel = "info"
workers = 4
bind = "0.0.0.0:8843"
insecure_bind = "0.0.0.0:8880"
graceful_timeout = 120
worker_class = "uvloop"
keepalive = 5
errorlog = "/opt/Capricornus/log/hypercorn_error.log"
accesslog = "/opt/Capricornus/log/hypercorn_access.log"
keyfile = "/opt/Capricornus/cert/key.pem"
certfile = "/opt/Capricornus/cert/cert.pem"