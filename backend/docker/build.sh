#!/bin/bash
IMGNAME=jointhero/capricornusng
IMGVERSION=v0.2.1
docker build --no-cache -t $IMGNAME:$IMGVERSION .
