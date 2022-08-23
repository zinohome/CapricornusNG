#!/bin/bash
IMGNAME=jointhero/CapricornusNG
IMGVERSION=v2.1.5
docker build --no-cache -t $IMGNAME:$IMGVERSION .
