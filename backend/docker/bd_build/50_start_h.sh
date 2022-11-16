#!/bin/bash
FIND_FILE="/opt/CapricornusNG/backend/appconfig/hypercorn.py"
FIND_STR="workers"
if [ `grep -c "$FIND_STR" $FIND_FILE` -ne '0' ];then
    echo "hypercorn config exist"
else
    cp /opt/CapricornusNG/backend/appconfig/hypercorn_default.py /opt/CapricornusNG/backend/appconfig/hypercorn.py
fi

FIND_DB_FILE="/opt/CapricornusNG/backend/utils/crud/sample.db"
if [ ! -f "$FIND_DB_FILE" ]; then
    echo "sample database exist"
else
    cp /opt/CapricornusNG/backend/utils/crud/sample.db /opt/CapricornusNG/backend/data/
fi
cd /opt/CapricornusNG/backend && \
nohup /opt/CapricornusNG/backend/venv/bin/hypercorn -c /opt/CapricornusNG/backend/appconfig/hypercorn.py main:app >> /tmp/CapricornusNG.log 2>&1 &