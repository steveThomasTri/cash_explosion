import requests
import os
from dotenv import load_dotenv

load_dotenv()

op_apikey = os.getenv("OPENCAGEAPIKEY")

api_key = op_apikey
query = "Sunny's Quick-Stop and Deli, lima, oh"

url = "https://api.opencagedata.com/geocode/v1/json"
params = {
    'q': query,
    'key': api_key,
    #'limit': 1
}

response = requests.get(url, params=params).json()

print(response)


if response['results']:
    result = response['results'][0]
    print("Formatted:", result['formatted'])
    print("Lat:", result['geometry']['lat'])
    print("Lng:", result['geometry']['lng'])
else:
    print("Not found")

'''
lat = 40.739306  # Example latitude
lng = -84.138570  # Example longitude

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
    print("Formatted address:", result['formatted'])
    print("Components:", result['components'])  # Optional: access street, city, etc.
else:
    print("No results found")
'''