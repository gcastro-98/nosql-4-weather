FROM python:3
COPY twitter.py .
RUN pip install twython pymongo
CMD [ "python", "twitter.py"]
