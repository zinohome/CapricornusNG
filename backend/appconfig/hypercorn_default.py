#!/usr/bin/env python3
# -*- coding: utf-8 -*-

loglevel = "info"
workers = 4
bind = "0.0.0.0:8843"
insecure_bind = "0.0.0.0:8880"
graceful_timeout = 120
worker_class = "uvloop"
keepalive = 5
errorlog = "/opt/CapricornusNG/backend/log/hypercorn_error.log"
accesslog = "/opt/CapricornusNG/backend/log/hypercorn_access.log"
keyfile = "/opt/CapricornusNG/backend/cert/key.pem"
certfile = "/opt/CapricornusNG/backend/cert/cert.pem"