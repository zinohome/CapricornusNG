#!/bin/bash
IMGNAME=jointhero/capricornus
IMGVERSION=v2.1.5
docker build --no-cache -t $IMGNAME:$IMGVERSION .
