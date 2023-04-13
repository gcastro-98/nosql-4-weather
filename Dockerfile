FROM python:3
COPY weather.py .
COPY cities_metada.csv .
COPY .api_key .
COPY .api_host .
RUN pip install pymongo pandas requests
CMD [ "python", "weather.py", "-mdb"]
