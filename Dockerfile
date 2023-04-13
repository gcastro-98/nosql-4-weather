FROM python:3
COPY weather.py .
COPY cities_metada.csv .
RUN pip install pymongo
CMD [ "python", "weather.py", "-mdb"]
