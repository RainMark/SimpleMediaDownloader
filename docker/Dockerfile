FROM debian:stable

RUN set -ex; \
apt-get update; \
apt-get install apt-utils -y; \
apt-get install nginx nginx-common -y; \
apt-get install vim -y; \
apt-get install python3 python3-pip -y; \
apt-get install git m4 -y; \
git clone https://github.com/RainMark/SimpleMediaDownloader.git; \
pip3 install -r /SimpleMediaDownloader/requirements.txt; \
ln -sf /SimpleMediaDownloader/config /config

COPY entry.sh /usr/local/bin/entry.sh
RUN chmod +x /usr/local/bin/entry.sh
CMD ["entry.sh"]