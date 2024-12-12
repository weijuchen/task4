import requests
import time
import pandas as pd
from pathlib import Path
from configparser import ConfigParser
# Config Parse

config = ConfigParser()
config.read("config.ini")
from configparser import ConfigParser

api_key  = config["OpenAQ"]["OPENAQ_API_KEY"]

url=f"https://api.openaq.org/v3/countries?limit=1000"

headers = {
    "X-API-Key": api_key
}

r = requests.get(url, headers=headers)


#  Retrieve countries_id  and all country name  
data=[]
for country in r.json()['results']:
    data.append(((country['id'], country['name'])))
print(data)



