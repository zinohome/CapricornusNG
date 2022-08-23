#!/bin/bash
set -e
set -x
apt-get update && DEBIAN_FRONTEND=noninteractive && \
apt -y dist-upgrade && \
apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev python3-dev net-tools libsasl2-dev curl wget procps netcat git libnss3-tools python3-pip && \
pip3 install virtualenv && \
cd /opt && \
git clone https://github.com/zinohome/CapricornusNG.git && \
cd /opt/CapricornusNG && \
git pull && \
chmod 755 mkcert-v1.4.3-linux-amd64 && mv mkcert-v1.4.3-linux-amd64 mkcert && mv mkcert /usr/bin/ && \
mkcert -install && \
mkdir -p /opt/CapricornusNG/log && \
mkdir -p /opt/CapricornusNG/cert && \
rm /opt/CapricornusNG/models/*.py && rm /opt/CapricornusNG/services/*.py && \
mkcert -cert-file /opt/CapricornusNG/cert/cert.pem -key-file /opt/CapricornusNG/cert/key.pem zinohome.com CapricornusNG.zinohome.com localhost 127.0.0.1 ::1 && \
virtualenv venv && \
. venv/bin/activate && \
pip3 install -r requirements.txt && \
cd /opt/CapricornusNG && cp /bd_build/default_env /opt/CapricornusNG/.env && \
cp /bd_build/wait-for /usr/bin/wait-for && chmod 755 /usr/bin/wait-for && \
ls -l /opt/CapricornusNG/.env && cat /opt/CapricornusNG/.env && \
cp /opt/CapricornusNG/docker/bd_build/50_start_CapricornusNG-h.sh /etc/my_init.d/50_start_CapricornusNG.sh && \
chmod 755 /etc/my_init.d/50_start_CapricornusNG.sh