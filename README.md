# twitter-scrapping
Twitter data scraping: a docker-compose setup is leveraged to collect 
data from Twitter (using a Python app and Twitter's API) and it is 
stored into a MongoDB database. It constitutes the 1st assignment
for the Big Data subject of the Data Science MSc course 
(UB, 2022-23): by G. Castro & P. Riba

## Steps

### Creating keys to Collect Data from Twitter

The Twitter's API keys were obtained for our developer accounts
and locally stored in the hidden files: ``.consumer_key`` & 
``.consumer_secret``. The access token & secret were as well 
stored at ``.access_token`` & ``.access_secret``.

### Dockerize the app to collect data from Twitter

The app to extract Twitter data was based in the proposed 
[notebook](https://github.com/rohit-nlp/BigDataCourseUB/blob/master/assisgnment_1/Twitter.ipynb) 
and the corresponding Python source code was stored in the ``twitter.py`` module.
Then, to Dockerize an app it is trivial, since it is needed to:
- Install Python and the dependencies (``twython``) in the container
- Run the Python code

If the Python code is executed as ``python twitter.py`` then the tweet 
data is stored locally in a .json; while if the code is executed with 
the ``-mdb`` flag (or ``--mongodb`` tag), it is then stored in a 
MongoDB database: ``python twitter.py -mdb``.

The image can be built by typing:

```bash
docker build -t twitter-scrapping .
```

### Publish the docker image of your app in docker hub in your account

The docker image can be found at: 
[DockerHub](https://hub.docker.com/repository/docker/gerardc98/twitter-scrapping)

It was pushed by @gcastro-98 simply by doing:
```bash
docker push twitter-scrapping
```

### Change the app to store data in mongoDb. Run the app with mongoDB (using images from docker-hub) using docker-compose

To run the multi-containers setup it is enough with typing:

```bash
docker-compose up -d
```
