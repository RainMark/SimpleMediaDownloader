# Simple Media Downloader

### Install

Please install nginx firstly.

+ please change server_name in *.nginx.conf
+ if you use https please check [https://github.com/XieXianbin/baidu-share-https](https://github.com/XieXianbin/baidu-share-https)

```bash
$ git clone https://git.0491401.org/i233/SimpleMediaDownloader.git
$ cd SimpleMediaDownloader
$ sudo -H pip3 install -r requirements.txt
$ cd src/core && python3 SimpleMediaDownloader.py -p 8000 &
$
$ sudo mkdir -p /var/www/site
$ sudo cp -r ../site/* /var/www/site/
$ cd ../../conf
$ sudo cp SimpleMediaDownloader.nginx.conf /etc/nginx/sites-available/
$ sudo ln -s /etc/nginx/sites-available/SimpleMediaDownloader.nginx.conf /etc/nginx/sites-enabled/SimpleMediaDownloader.nginx.conf
$ sudo nginx -s reload
```

### Tested

+ Mozilla Firefox 55.0.3 (Linux)
+ Chromium 61.0.3163.100 (Linux)
