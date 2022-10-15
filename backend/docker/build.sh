#!/bin/bash
IMGNAME=jointhero/capricornusng
IMGVERSION=v2.1.6
docker build --no-cache -t $IMGNAME:$IMGVERSION .
