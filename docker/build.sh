#!/bin/bash
IMGNAME=jointhero/capricornusng
IMGVERSION=v2.1.5
docker build --no-cache -t $IMGNAME:$IMGVERSION .
