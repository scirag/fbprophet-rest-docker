# fbprophet-rest-docker

Alpine based Docker Image for Facebook Prophet

Registry : https://hub.docker.com/r/safakcirag/fbprophet-rest

* python : 3.6 
* fbprophet : 0.3.post2 
* Jupyter Notebook

```
curl '-d {"periods":1, \
          "ds": ["2007-12-10", "2007-12-11", "2007-12-12", "2007-12-13", "2007-12-14"], \
          "y": [9.59076113897809, 9.51959031601596, 9.18367658262066, 9.07246736935477, 9.0935720735049]}' \
          -H "Content-Type: application/json" -X POST http://localhost/
```

![](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?style=popout)
