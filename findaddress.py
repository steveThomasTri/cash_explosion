import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

op_apikey = os.getenv("OPENCAGEAPIKEY")

file_to_load = "players2.csv"


api_key = op_apikey

def get_latlng(business, city, road):
    query = f"{business}, {city}, oh"

    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': query,
        'key': api_key,
        #'limit': 1
    }

    response = requests.get(url, params=params).json()

    if response['results']:
        result = response['results'][0]
        #print("Formatted:", result['formatted'])
        #print("Lat:", result['geometry']['lat'])
        #print("Lng:", result['geometry']['lng'])

        return getaddress(result['geometry']['lat'], result['geometry']['lng'], road)
    else:
        print("Not found")

def getaddress(lat, lng, road):
    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': f'{lat},{lng}',
        'key': api_key,
        'pretty': 1,
        'no_annotations': 1
    }

    response = requests.get(url, params=params).json()

    if response['results']:
        result = response['results'][0]
        #print("Formatted address:", result['formatted'])
        #print(road)
        #print("Components:", result['components'])  # Optional: access street, city, etc.
        return([result['formatted'], road, result["components"],lat,lng])
    else:
        print("No results found")


with open(file_to_load) as file:
    reader = csv.reader(file)
    header = next(reader)
    with open("businesses.txt", "a+") as f:
        for row in reader:
            info = get_latlng(row[4], row[6], row[5])
            #print(info)
            f.write(f"{info[0]}\n{info[1]}\n{info[2]}\n{info[3]}\n{info[4]}\n---------------------------------------------------------------------------------------\n")