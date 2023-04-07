import pandas as pd
import requests
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime
import requests

############################################
# We receive the data from the weather API #
############################################

url = "https://weatherapi-com.p.rapidapi.com/current.json"
querystring = {"q":"53.1,-0.13"}

headers = {
	"X-RapidAPI-Key": "4c347c4bdamsh920072072156112p12850ajsnf6a61e22808e",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)

##############################################
# Parse Top100-US.csv and store into MongoDB #
##############################################

# MongoDB connection
client = MongoClient()
db = client['mydb']
collection = db['city_weather']

# Weather API credentials and endpoint
api_key = "4c347c4bdamsh920072072156112p12850ajsnf6a61e22808e"
endpoint = "http://api.weatherapi.com/v1/current.json?key={api_key}&q={city},{zip_code}"

# Read CSV into pandas dataframe
df = pd.read_csv('Top100-US.csv', sep=';')

# Iterate over dataframe and call API for each city/zip
for index, row in df.iterrows():
    city = row['City']
    zip_code = row['Zip']
    url = endpoint.format(api_key=api_key, city=city, zip_code=zip_code)
    response = requests.get(url).json()
    
    # Construct document to store in MongoDB
    document = {
        'zip': zip_code,
        'city': city,
        'created_at': datetime.now(),
        'weather': response
    }
    
    # Insert document into MongoDB collection
    collection.insert_one(document)
