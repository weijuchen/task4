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


# List of countries_id and country name

# [(1, 'Indonesia'), (2, 'Malaysia'), (3, 'Chile'), (5, 'Peru'), (6, 'Argentina'), (7, 'Dhekelia'), 
# (8, 'Cyprus'), (9, 'India'), (10, 'China'), (11, 'Israel'), (12, 'Palestine'), (14, 'Ethiopia'), (15, 'South Sudan'), (17, 'Kenya'), (22, 'France'), (24, 'Guyana'), (25, 'Republic of Korea'), (27, 'Morocco'), (29, 'Costa Rica'), (32, 'Democratic Republic of the Congo'), (34, 'Ukraine'), (37, 'South Africa'), (38, 'Saint-Martin'), (40, 'Oman'), (41, 'Uzbekistan'), (42, 'Kazakhstan'), (43, 'Tajikistan'), (44, 'Lithuania'), (45, 'Brazil'), (46, 'Uruguay'), (47, 'Mongolia'), (48, 'Russian 
# Federation'), (49, 'Czech Republic'), (50, 'Germany'), (51, 'Estonia'), (52, 'Latvia'), (53, 'Norway'), (54, 'Sweden'), (55, 'Finland'), (56, 'Vietnam'), (58, 'Luxembourg'), (59, 'United Arab Emirates'), (60, 'Belgium'), (62, 'North Macedonia'), (64, 'Azerbaijan'), (65, 'Kosovo'), (66, 'Turkey'), (67, 'Spain'), (68, 'Lao PDR'), (69, 'Kyrgyzstan'), (121, 'Monaco'), (122, 'Algeria'), (123, 'Mozambique'), (70, 'Armenia'), (71, 'Denmark'), (74, 'Romania'), (75, 'Hungary'), (76, 'Slovakia'), (77, 'Poland'), (78, 'Ireland'), (79, 'United Kingdom'), (80, 'Greece'), (81, 'Zambia'), (83, 'Guinea'), (86, 'Sudan'), (89, 'Austria'), (90, 'Iraq'), (91, 'Italy'), (92, 'Switzerland'), (94, 'Netherlands'), (96, "Côte d'Ivoire"), (97, 'Serbia'), (98, 'Mali'), (99, 'Senegal'), (100, 'Nigeria'), (103, 'Croatia'), (104, 'Slovenia'), (105, 'Qatar'), (106, 'Saudi Arabia'), (109, 'Pakistan'), (110, 'Bulgaria'), (111, 'Thailand'), (112, 'San Marino'), (115, 'Chad'), (116, 'Kuwait'), (199, 
# 'Trinidad and Tobago'), (118, 'Guatemala'), (126, 'Rwanda'), (127, 'Myanmar'), (128, 'Bangladesh'), (129, 'Andorra'), (130, 'Afghanistan'), (131, 'Montenegro'), (132, 'Bosnia and Herzegovina'), (133, 'Uganda'), (136, 'Honduras'), (137, 'Ecuador'), (138, 'Colombia'), (139, 'Paraguay'), (141, 'Portugal'), (142, 'Moldova'), (143, 'Turkmenistan'), (144, 'Jordan'), (145, 'Nepal'), (147, 'Cameroon'), (152, 'Ghana'), (154, 'Gibraltar'), (155, 'United States'), (156, 'Canada'), (157, 'Mexico'), (158, 'Belize'), (162, 'Egypt'), (166, 'The Gambia'), (167, 'Hong Kong'), (176, 'Antarctica'), (177, 'Australia'), (180, 'New Zealand'), (182, 'Madagascar'), (183, 'Philippines'), (184, 'Sri Lanka'), (185, 'Curaçao'), (189, 'Taiwan'), (190, 'Japan'), (192, 'Iceland'), (211, 'Puerto Rico'), (219, 'Mauritius'), (222, 'Republic of Cabo Verde'), (223, 'Malta'), (224, 'Jersey'), (231, 'Singapore'), (239, 'Maldives'), (250, 'Bahrain')]


# Retrieve locations(monitoring stations) based on the provided countries_id
# The countries_id for Malaysia is 2


url=f"https://api.openaq.org/v3/locations?countries_id=2"


headers = {
    "X-API-Key": api_key
}

r = requests.get(url, headers=headers)

# get location names and their corresponding sensors_id 
data=[]
for location in r.json()["results"]:
    data.append((location["name"],location["sensors"][0]["id"]))
        
print(data) 
