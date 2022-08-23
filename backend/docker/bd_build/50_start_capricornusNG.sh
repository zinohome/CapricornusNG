#!/bin/bash
FIND_FILE="/opt/CapricornusNG/config/gunicorn.py"
FIND_STR="workers"
if [ `grep -c "$FIND_STR" $FIND_FILE` -ne '0' ];then
    echo "gunicorn config exist"
else
    cp /opt/CapricornusNG/config/gunicorn_default.py /opt/CapricornusNG/config/gunicorn.py
fi
cd /opt/CapricornusNG && \
nohup /opt/CapricornusNG/venv/bin/gunicorn -c /opt/CapricornusNG/config/gunicorn.py main:app >> /tmp/CapricornusNG.log 2>&1 &