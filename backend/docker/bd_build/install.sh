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
cd backend && \
chmod 755 mkcert-v1.4.3-linux-amd64 && mv mkcert-v1.4.3-linux-amd64 mkcert && mv mkcert /usr/bin/ && \
mkcert -install && \
mkdir -p /opt/CapricornusNG/backend/log && \
mkdir -p /opt/CapricornusNG/backend/cert && \
rm /opt/CapricornusNG/backend/apps/dmodels/*.py && rm /opt/CapricornusNG/backend/apps/dadmins/*.py && \
mkcert -cert-file /opt/CapricornusNG/backend/cert/cert.pem -key-file /opt/CapricornusNG/backend/cert/key.pem zinohome.com CapricornusNG.zinohome.com localhost 127.0.0.1 ::1 && \
virtualenv venv && \
. venv/bin/activate && \
pip3 install -r requirements.txt && \
pip3 uninstall -y fastapi_amis_admin && \
pip3 uninstall -y fastapi_user_auth && \
pip3 uninstall -y sqlalchemy_database && \
cd /opt/CapricornusNG/backend && cp /bd_build/default_env /opt/CapricornusNG/backend/.env && \
cp /bd_build/wait-for /usr/bin/wait-for && chmod 755 /usr/bin/wait-for && \
ls -l /opt/CapricornusNG/backend/.env && cat /opt/CapricornusNG/backend/.env && \
ls -l /opt/CapricornusNG/backend/docker/bd_build/ && \
cp /opt/CapricornusNG/backend/docker/bd_build/50_start_h.sh /etc/my_init.d/50_start_CapricornusNG.sh && \
rm /opt/CapricornusNG/backend/data/capricornus.db && rm -r /opt/CapricornusNG/backend/fastapi_amis_admin_update && \
rm -r /opt/CapricornusNG/docker && rm -r /opt/CapricornusNG/scripts && \
mv /opt/CapricornusNG/backend/docker /opt/CapricornusNG/ &&
chmod 755 /etc/my_init.d/50_start_CapricornusNG.sh