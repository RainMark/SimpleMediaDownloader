# Simple Media Downloader

### Deploy

#### Stage1

Setup python environment.

```bash
$ git clone https://git.0491401.org/i233/SimpleMediaDownloader.git
$ cd SimpleMediaDownloader/src
$ sudo -H pip3 install -r requirements.txt
$ python3 SimpleMediaDownloader.py -p 8000
```

#### Stage2

Setup nginx environment.

```bash
$ sudo cp -r /var/www/html /var/www/html.bak
$ sudo mkdir -p /var/www/html
$ sudo cp -r SimpleMediaDownloader/src/web/* /var/www/html
$ sudo vim /var/www/html/js/function.js # Set SITE = ''
$ sudo chown www /var/www/html -R
```

```nginx
server {
    listen 80;
    server_name example.org;
    client_max_body_size 256M;
    resolver 8.8.8.8;

    location /qq {
        proxy_pass https://dl.stream.qqmusic.qq.com/$1$is_args$args;
        rewrite ^/qq/(.*) /$1 break;
    }

    location /api/v1 {
        proxy_pass http://localhost:8000;
    }

    location / {
        root /var/www/html;
    }
}
```

### Test

+ Mozilla Firefox 55.0.3 (Linux)
+ Chromium 61.0.3163.100 (Linux)
