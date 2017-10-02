# Simple Media Downloader

### Deploy

#### Stage1

Setup python environment.

```bash
$ git clone https://git.0491401.org/i233/SimpleMediaDownloader.git
$ cd SimpleMediaDownloader/src
$ sudo -H pip3 install -r requirements.txt
$ python3 SimpleMediaDownloader.py -s yes -p 8000
```

#### Stage2

Setup nginx environment.

```bash
$ sudo cp -r /var/www/html /var/www/html.bak
$ sudo cp -r SimpleMediaDownloader/src/web/* /var/www/html
```

```nginx
server {
	listen 80;
	server_name example.com;
	client_max_body_size 256M;

	location /api {
		proxy_pass http://localhost:8000;
	}

	location / {
		root /var/www/html;
	}
}
```

### TODO

+ Make search process fast.

