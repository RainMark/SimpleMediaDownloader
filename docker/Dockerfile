FROM debian:stable

RUN apt-get update
RUN apt-get install apt-utils procps vim git m4 -y
RUN apt-get install nginx nginx-common -y
RUN apt-get install python3 python3-pip -y
RUN git clone https://github.com/RainMark/SimpleMediaDownloader.git
RUN pip3 install -r /SimpleMediaDownloader/requirements.txt
RUN ln -sf /SimpleMediaDownloader/config /config

COPY entry.sh /usr/local/bin/entry.sh
RUN chmod +x /usr/local/bin/entry.sh
CMD ["entry.sh"]