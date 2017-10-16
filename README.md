# Simple Media Downloader

### Deploy

#### Stage1

Setup python environment.

```bash
$ git clone https://git.0491401.org/i233/SimpleMediaDownloader.git
$ cd SimpleMediaDownloader/src/core
$ sudo -H pip3 install -r requirements.txt
$ python3 SimpleMediaDownloader.py -p 8000
```

#### Stage2

Setup nginx environment.

```bash
$ sudo cp -r SimpleMediaDownloader/src/site /var/www/
$ sudo chmod 644 -R /var/www/site
```

```nginx
server {
    listen 80;
    server_name example.org;
    client_max_body_size 256M;
    resolver 8.8.8.8;

    location /qqmusic {
        rewrite ^/qqmusic/(.*) /$1 break;
        proxy_pass https://dl.stream.qqmusic.qq.com/$1$is_args$args;
    }

    location /api/v1 {
        proxy_pass http://127.0.0.1:8000;
    }

    location / {
        root /var/www/site;
    }
}
```

### Test

+ Mozilla Firefox 55.0.3 (Linux)
+ Chromium 61.0.3163.100 (Linux)
