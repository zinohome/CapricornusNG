#!/bin/bash
set -e
set -x
apt-get update && DEBIAN_FRONTEND=noninteractive && \
apt -y dist-upgrade && \
apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev python3-dev net-tools libsasl2-dev curl wget procps netcat git libnss3-tools python3-pip && \
pip3 install virtualenv && \
cd /opt && \
git clone https://github.com/zinohome/Capricornus.git && \
cd /opt/Capricornus && \
git pull && \
chmod 755 mkcert-v1.4.3-linux-amd64 && mv mkcert-v1.4.3-linux-amd64 mkcert && mv mkcert /usr/bin/ && \
mkcert -install && \
mkdir -p /opt/Capricornus/log && \
mkdir -p /opt/Capricornus/cert && \
rm /opt/Capricornus/models/*.py && rm /opt/Capricornus/services/*.py && \
mkcert -cert-file /opt/Capricornus/cert/cert.pem -key-file /opt/Capricornus/cert/key.pem zinohome.com Capricornus.zinohome.com localhost 127.0.0.1 ::1 && \
virtualenv venv && \
. venv/bin/activate && \
pip3 install -r requirements.txt && \
pip3 uninstall -y simple_rest_client && \
cd /opt/Capricornus && cp /bd_build/default_env /opt/Capricornus/.env && \
cp /bd_build/wait-for /usr/bin/wait-for && chmod 755 /usr/bin/wait-for && \
ls -l /opt/Capricornus/.env && cat /opt/Capricornus/.env && \
cp /opt/Capricornus/docker/bd_build/50_start_capricornus-h.sh /etc/my_init.d/50_start_capricornus.sh && \
chmod 755 /etc/my_init.d/50_start_capricornus.sh