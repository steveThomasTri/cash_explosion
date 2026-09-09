from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut
from database import insert_player, get_endgame, update_endgame_results, verify2, totalwinnings, cities
import json

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


def findnewcities():
    mycursor = mydb.cursor()
    sql = f"SELECT DISTINCT playerCity from players UNION SELECT DISTINCT ticketPurchasedCity from players"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)

    sql = "SELECT city from cities"
    mycursor.execute(sql)
    donotduplicatecity = mycursor.fetchall()
    donotdulpicatecitylist = []

    for x in donotduplicatecity:
        donotdulpicatecitylist.append(x[0])

    candidates = [c[0] for c in myresult if c[0] and c[0] not in donotdulpicatecitylist]
    print(f"[get_new_cities] {len(myresult)} distinct city name(s) referenced in players table.")
    print(f"[get_new_cities] {len(donotdulpicatecitylist)} already exist in cities table.")
    print(f"[get_new_cities] {len(candidates)} new city name(s) to geocode: {candidates}")

    if not candidates:
        print("[get_new_cities] Nothing to do — all cities already geocoded.")
        return

    geolocator = Nominatim(user_agent="city_locator")

    inserted = 0
    failed = []

    for city_name in candidates:
        try:
            location = geolocator.geocode(f"{city_name}, Ohio", timeout=10)
            if not location:
                location = geolocator.geocode(city_name, timeout=10)

            if not location:
                print(f"[get_new_cities] FAILED to geocode '{city_name}' — no match found, skipping.")
                failed.append(city_name)
                continue

            county = location.raw["display_name"].split(", ")
            county_match = next((c for c in county if "County" in c), None)

            if not county_match:
                print(f"[get_new_cities] FAILED for '{city_name}' — geocoded, but no county found in "
                      f"result: {location.raw['display_name']}")
                failed.append(city_name)
                continue

            sql = "INSERT INTO cities (city, lon, lat, county) VALUES (%s, %s, %s, %s)"
            data = (city_name, location.longitude, location.latitude, county_match)
            mycursor.execute(sql, data)
            mydb.commit()
            inserted += 1
            print(f"[get_new_cities] Added '{city_name}' -> {county_match} "
                  f"({location.latitude:.4f}, {location.longitude:.4f})")

        except GeocoderTimedOut:
            print(f"[get_new_cities] Timeout for '{city_name}', retrying once...")
            time.sleep(2)
            try:
                location = geolocator.geocode(f"{city_name}, Ohio", timeout=10)
                if location:
                    county = location.raw["display_name"].split(", ")
                    county_match = next((c for c in county if "County" in c), None)
                    if county_match:
                        sql = "INSERT INTO cities (city, lon, lat, county) VALUES (%s, %s, %s, %s)"
                        data = (city_name, location.longitude, location.latitude, county_match)
                        mycursor.execute(sql, data)
                        mydb.commit()
                        inserted += 1
                        print(f"[get_new_cities] Added '{city_name}' on retry -> {county_match}")
                    else:
                        failed.append(city_name)
                else:
                    failed.append(city_name)
            except GeocoderTimedOut:
                print(f"[get_new_cities] FAILED '{city_name}' — timed out twice, skipping.")
                failed.append(city_name)

        time.sleep(1)  # Nominatim's usage policy requires max 1 request/sec

    print(f"[get_new_cities] Done. Inserted {inserted}/{len(candidates)}.")
    if failed:
        print(f"[get_new_cities] {len(failed)} city name(s) could NOT be geocoded and were skipped: {failed}")
        print("[get_new_cities] These will be missing from the dashboard map until fixed manually "
              "(e.g. bad spelling, out-of-state, or too ambiguous for Nominatim).")


def insertcity():
    mycursor = mydb.cursor()
    sql = f"SELECT county from cities where code is null"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if not myresult:
        print("[get_new_cities] insertcity(): no cities missing a county code.")
        return

    print(f"[get_new_cities] insertcity(): {len(myresult)} cities need a county code assigned.")

    if not os.path.exists("county.json"):
        print("[get_new_cities] FAILED: county.json not found in the current directory — "
              "cannot assign county codes.")
        return

    with open('county.json', 'r') as file:
        data = json.load(file)

        matched = 0
        for result in myresult:
            county = result[0].split(" ")
            firstname = county[0]

            found = False
            for feature in data["features"]:
                if (feature["properties"]["STATEFP"] == "39") and (feature["properties"]["NAME"] == firstname):
                    mycursor = mydb.cursor()
                    sql = f"UPDATE cities SET code=%s where county=%s"
                    addr = (feature["properties"]["GEOID"], result[0])
                    mycursor.execute(sql, addr)
                    mydb.commit()
                    matched += 1
                    found = True
                    break

            if not found:
                print(f"[get_new_cities] insertcity(): no GEOID match found for county '{result[0]}'")

        print(f"[get_new_cities] insertcity(): assigned codes to {matched}/{len(myresult)} counties.")


if __name__ == "__main__":
    findnewcities()
    insertcity()