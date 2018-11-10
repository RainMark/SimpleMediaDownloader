#!/bin/bash

# entry.sh --server 127.0.0.1

if [ "2" = "$#" ]; then
    m4 -DSVR_NAME="$2" /config/nginx.conf > /etc/nginx/sites-available/default
    service nginx start
    exec /bin/bash
fi
