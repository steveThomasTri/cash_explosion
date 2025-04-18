from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut
from database import insert_player, get_endgame, update_endgame_results, verify2, totalwinnings, cities


import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
password = os.getenv("PASSWORD")
user = os.getenv("USER")

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  auth_plugin='caching_sha2_password',
  database='cedb'
  )

"""
mycursor = mydb.cursor()
sql = f"SELECT DISTINCT playerCity from players UNION SELECT DISTINCT ticketPurchasedCity from players"
mycursor.execute(sql)
myresult = mycursor.fetchall()

sql = "SELECT city from cities"
mycursor.execute(sql)
donotduplicatecity = mycursor.fetchall()
donotdulpicatecitylist = []

for x in donotduplicatecity:
    donotdulpicatecitylist.append(x[0])

geolocator = Nominatim(user_agent="city_locator")

for city in myresult:
    if city[0] not in donotdulpicatecitylist:
        try:
            location = geolocator.geocode(f"{city[0]}, Ohio", timeout=10)
            if location:
                print(f"{city[0]} → {location.latitude}, {location.longitude}")
                print(f"{location.raw}")
                county = location.raw["display_name"].split(", ")
                for c in county:
                    if (c.find("County") != -1):
                        print(c)
                        sql = "INSERT INTO cities (city, lon, lat, county) VALUES (%s, %s, %s, %s)"
                        data = (city[0],location.longitude, location.latitude, c,)
                        mycursor.execute(sql, data)
                        mydb.commit()
                        break
            else:
                print(f"{city[0]} not found. trying alternate approach")
                location = geolocator.geocode(city[0], timeout=10)
                if location:
                    print(f"{city[0]} → {location.latitude}, {location.longitude}")
                    print(f"{location.raw}")
                    county = location.raw["display_name"].split(", ")
                    for c in county:
                        if (c.find("County") != -1):
                            print(c)
                            sql = "INSERT INTO cities (city, lon, lat, county) VALUES (%s, %s, %s, %s)"
                            data = (city[0],location.longitude, location.latitude, c,)
                            mycursor.execute(sql, data)
                            mydb.commit()
                            break
        except GeocoderTimedOut:
            print(f"Timeout for {city[0]}, retrying...")
            time.sleep(2)
            continue
        time.sleep(1)

# Create a geolocator object
#geolocator = Nominatim(user_agent="city_locator")

# Look up the city
#location = geolocator.geocode("Columbus, Ohio")

# Print results
#print(f"Address: {location.address}")
#print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
"""
"""
import json

mycursor = mydb.cursor()
sql = f"SELECT county from cities"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(myresult)




# Open and read the JSON file
with open('county.json', 'r') as file:
    data = json.load(file)

    for result in myresult:
        #print(result[0])
        county = result[0].split(" ")
        firstname = county[0]

        for feature in data["features"]:
            if (feature["properties"]["STATEFP"] == "39") and (feature["properties"]["NAME"] == firstname):
                #print(feature["properties"]["GEOID"], firstname)
                mycursor = mydb.cursor()
                sql = f"UPDATE cities SET code=%s where county=%s"
                addr = (feature["properties"]["GEOID"],result[0],)
                mycursor.execute(sql, addr)
                mydb.commit()
                break
"""
'''
mycursor = mydb.cursor()
sql = f"UPDATE cities SET code=26115 where city='TEMPERANCE, MI'"
mycursor.execute(sql)
mydb.commit()
'''