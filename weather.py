import pandas as pd
import argparse
from typing import List
from datetime import datetime
import requests

#############################################################################
# We prepare the keys to receive data from the weather API #
#############################################################################

with open('.api_key', 'r') as _api_key:
    _xrapid_api_key: str = _api_key.readline().strip()
with open('.api_host', 'r') as _api_host:
    _xrapid_api_host: str = _api_host.readline().strip()

_url: str = "https://weatherapi-com.p.rapidapi.com/current.json"
_headers = {
    "X-RapidAPI-Key": _xrapid_api_key,
    "X-RapidAPI-Host": _xrapid_api_host,
}

##############################################
# Parse cities_metada.csv and store into MongoDB #
##############################################


def get_cities_weather_documents_list() -> List[dict]:
    # Read CSV into pandas dataframe
    df = pd.read_csv('cities_metada.csv', sep=';')
    document_list: List[dict] = []

    # Iterate over dataframe and call API for each city/zip
    for index, row in df.iterrows():
        city = row['City']
        zip_code = row['Zip']
        weather_data: dict = requests.get(
            _url, headers=_headers, params={'q': zip_code}).json()

        # we construct document to store in MongoDB
        document = {
            'zip': zip_code,
            'city': city,
            'created_at': datetime.now(),
            'weather': weather_data
        }
        document_list.append(document)

    return document_list


# ###################################################################
# ARGUMENTS PARSING (we detect whether we want mongo db or not)
# ###################################################################

# we add an argument parser to detect whether we want to save it in
# a MongoDB or a local .json
parser = argparse.ArgumentParser(
    description='Store some Weather data: both locally or in a '
                'MongoDB database if --mongodb or -mdb is flagged')
parser.add_argument(
    '-mdb', '--mongodb', action='store_true',
    help='If activated, the tweet data is stored in a MongoDB '
         'database instead of a local .json')
# now the 'mongodb' state is added as local variable in the
# args namespace (by default, set to False)
args = parser.parse_args()
# the variable can be accessed as vars(args)['mongodb']
use_mongodb = vars(args)['mongodb']

if use_mongodb:
    # connect with the local mongodb and create a database
    # and collection for weather data
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError
    client = MongoClient('mongodb://localhost:27017/')
    db = client["weatherdb"]
    weather_collection = db["city_weather"]

    try:
        # insert documents into MongoDB collection
        weather_collection.insert_many(get_cities_weather_documents_list())
        print("Data succesfully added to the database!")
    except ServerSelectionTimeoutError as error:
        print("There was a problem when adding data to the db! Check whether "
              "there is a local database instance accessible through port "
              "27017. Below the error traceback is presented:", error)
else:
    import json
    _documents: dict = {_i: _doc for _i, _doc in enumerate(
        get_cities_weather_documents_list())}
    with open("city_weather.json", "w") as _json_file:
        json.dump(_documents, _json_file)
