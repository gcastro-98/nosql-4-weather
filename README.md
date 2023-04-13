# nosql-4-weather
Weather data scraping: a docker-compose setup is leveraged to collect 
data from a Weather web app (using a Python script and its API) and it is 
stored into a MongoDB database. It constitutes the 1st assignment
for the Big Data subject of the Data Science MSc course 
(UB, 2022-23): by G. Castro & P. Riba

## Steps

### Creating keys to collect data

The Weather's API keys were obtained and locally stored in the hidden files: 
``.api_key`` & ``.api_host``. 

### Dockerize the app to collect data

The app to extract weather data is stored in the ``weather.py`` module.
Then, to Dockerize an app it is trivial, since it is needed to:
- Install Python and the dependencies in the container
- Run the Python code

If the Python code is executed as ``python weather.py`` then the tweet 
data is stored locally in a .json; while if the code is executed with 
the ``-mdb`` flag (or ``--mongodb`` tag), it is then stored in a 
MongoDB database: ``python weather.py -mdb``.

The image can be built by typing:

```bash
docker build -t nosql-4-weather .
```

### Publish the docker image of your app in docker hub in your account

The docker image can be found at: 
[DockerHub](https://hub.docker.com/repository/docker/gerardc98/nosql-4-weather)
It was originally pushed, after building the image from the Dockerfile, 
by typing:
```bash
docker tag nosql-4-weather gerardc98/nosql-4-weather
docker push gerardc98/nosql-4-weather
```

This container can be run by single, typing:
```bash
docker run -it --name nosql-4-weather --link mongodb:mongodb nosql-4-weather
```

**Note** it will not work unless a MongoDB container is running 
on localhost at port 27017 with name ``mongodb``! It is needless 
to remind this can 
be done by running:

```bash
docker run -d -p 27017:27017 -v /path/to/local/folder:/data/db --name mongodb mongo
```

### Change the app to store data in mongoDb. Run the app with mongoDB (using images from docker-hub) using docker-compose

To run the multi-containers setup it is enough with typing:

```bash
docker-compose up -d
```
