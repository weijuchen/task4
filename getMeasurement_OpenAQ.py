import requests
import time
import pandas as pd
from pathlib import Path
from configparser import ConfigParser
import csv

# Config Parse
config = ConfigParser()
config.read("config.ini")
from configparser import ConfigParser
api_key  = config["OpenAQ"]["OPENAQ_API_KEY"]

# List of location name and sensors_id
# [('Kuala Lumpur', 2085316), ('Ban Padang Community School', 6458077), ('CEASTech, UniMAP', 7240645), ('Setia Alam', 7979937)]


url=f"https://api.openaq.org/v3/sensors/2085316/measurements?datetime_to=2024-05-13T14%3A00%3A00%2B00%3A00&datetime_from=2024-05-13T00%3A00%3A00%2B00%3A00"


headers = {
    "X-API-Key": api_key
}



r = requests.get(url, headers=headers)


data={}
if r.status_code == 200:
    if r.json()["results"][0]["parameter"]["id"]==2:
        for measurement in r.json()['results']:
            data[measurement["period"]['datetimeFrom']["utc"]]=measurement["value"]
        pm25 = data
        with open("pm25.csv", "w") as f:
            writer = csv.writer(f)
            for time, value in pm25.items():
                writer.writerow([time, value])
    else:
        print("Sensors do not provide PM2.5 data.")            


