## Simple Media Downloader

![](https://github.com/RainMark/SimpleMediaDownloader/raw/master/pic/index.png)

---

![](https://github.com/RainMark/SimpleMediaDownloader/raw/master/pic/subpage.png)

---

- build

```bash
$ git clone https://github.com/RainMark/SimpleMediaDownloader.git
$ cd SimpleMediaDownloader/docker/
$ ./build.sh
```

- running

```bash
$ docker run -dt --rm --name dl -p 10086:80 simple-media-dl entry.sh --server localhost
```

- [http://127.0.0.1:10086](http://127.0.0.1:10086)
