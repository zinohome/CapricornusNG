#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS")
use_max_workers = None
if max_workers_str:
    use_max_workers = int(max_workers_str)
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
worker_class_str = os.getenv("WORKER_CLASS", "uvloop")

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8843")
insecport = os.getenv("PORT", "8880")
bind_env = os.getenv("BIND", None)
insecbind_env = os.getenv("INSECBIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"
if insecbind_env:
    use_insec_bind = insecbind_env
else:
    use_insec_bind = f"{host}:{insecport}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if use_max_workers:
        web_concurrency = min(web_concurrency, use_max_workers)
accesslog_var = os.getenv("ACCESS_LOG", "/opt/Capricornus/log/hypercorn_access.log")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "/opt/Capricornus/log/hypercorn_error.log")
use_errorlog = errorlog_var or None
keyfile_var = os.getenv("KEYFILE", "/opt/Capricornus/cert/key.pem")
use_keyfile = keyfile_var or None
certfile_var = os.getenv("CERTFILE", "/opt/Capricornus/cert/cert.pem")
use_certfile = certfile_var or None
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

# Hypercorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
insecure_bind = use_insec_bind
errorlog = use_errorlog
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
keep_alive_timeout = int(keepalive_str)
worker_class = worker_class_str
keyfile = use_keyfile
certfile = use_certfile


# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "insecure_bind":insecure_bind,
    "graceful_timeout": graceful_timeout,
    "worker_class": worker_class,
    "keepalive": keep_alive_timeout,
    "errorlog": errorlog,
    "accesslog": accesslog,
    "keyfile": keyfile,
    "certfile": certfile,
    # Additional, non-hypercorn variables
    "workers_per_core": workers_per_core,
    "use_max_workers": use_max_workers,
    "host": host,
    "port": port,
    "insecport": insecport,
}
print(json.dumps(log_data,indent=4))
