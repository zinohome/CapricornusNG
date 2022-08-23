#!/bin/bash
FIND_FILE="/opt/CapricornusNG/config/hypercorn.py"
FIND_STR="workers"
if [ `grep -c "$FIND_STR" $FIND_FILE` -ne '0' ];then
    echo "hypercorn config exist"
else
    cp /opt/CapricornusNG/config/hypercorn_default.py /opt/CapricornusNG/config/hypercorn.py
fi
cd /opt/CapricornusNG && \
nohup /opt/CapricornusNG/venv/bin/hypercorn -c /opt/CapricornusNG/config/hypercorn.py main:app >> /tmp/CapricornusNG.log 2>&1 &