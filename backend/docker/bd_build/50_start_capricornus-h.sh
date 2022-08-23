#!/bin/bash
FIND_FILE="/opt/Capricornus/config/hypercorn.py"
FIND_STR="workers"
if [ `grep -c "$FIND_STR" $FIND_FILE` -ne '0' ];then
    echo "hypercorn config exist"
else
    cp /opt/Capricornus/config/hypercorn_default.py /opt/Capricornus/config/hypercorn.py
fi
cd /opt/Capricornus && \
nohup /opt/Capricornus/venv/bin/hypercorn -c /opt/Capricornus/config/hypercorn.py main:app >> /tmp/Capricornus.log 2>&1 &