
"""
Geocode ticket-purchase store locations from player.csv using
Google Places API (New) Text Search, then write out an enriched CSV
with name, formatted address, latitude, and longitude for each row.

Usage:
    1. Set your API key below (or via the GOOGLE_PLACES_API_KEY env var).
    2. python geocode_players.py
"""

import csv
import os
import time
import requests

#API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "YOUR_API_KEY")
API_KEY = "AIzaSyD6KuEPBNz90RkwjkuU66sX5rtRDzIBW8M"

INPUT_CSV = "player.csv"
OUTPUT_CSV = "player_with_coordinates2.csv"

SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    # Keep the field mask minimal -> cheapest ("Pro") pricing tier
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
}


def geocode(query: str) -> dict:
    """Send one Text Search (New) request and return the top match, or None."""
    body = {"textQuery": query}
    resp = requests.post(SEARCH_URL, headers=HEADERS, json=body, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    places = data.get("places", [])
    if not places:
        return None
    top = places[0]
    return {
        "name": top["displayName"]["text"],
        "address": top["formattedAddress"],
        "latitude": top["location"]["latitude"],
        "longitude": top["location"]["longitude"],
    }


def main():
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Build the query string for each row (store, street, city + state)
    for row in rows:
        row["_query"] = (
            f"{row['ticketPurchasedStore']}, "
            f"{row['ticketPurchasedStreet']}, "
            f"{row['ticketPurchasedCity']}, OH"
        )

    # Deduplicate: many rows share the same store/street/city combo,
    # no need to pay for (or wait on) the same lookup twice.
    unique_queries = sorted({row["_query"] for row in rows})
    print(f"{len(rows)} rows -> {len(unique_queries)} unique locations to geocode")

    cache = {}
    for i, query in enumerate(unique_queries, 1):
        try:
            result = geocode(query)
        except requests.exceptions.RequestException as e:
            print(f"  [{i}/{len(unique_queries)}] ERROR for '{query}': {e}")
            result = None

        if result is None:
            print(f"  [{i}/{len(unique_queries)}] NO MATCH: {query}")
        else:
            print(f"  [{i}/{len(unique_queries)}] OK: {query} -> {result['address']}")

        cache[query] = result
        time.sleep(0.05)  # small pause to be polite to the API

    # Merge results back into every row
    fieldnames = list(rows[0].keys())
    fieldnames.remove("_query")
    fieldnames += ["placeName", "placeAddress", "latitude", "longitude"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            result = cache.get(row["_query"])
            out_row = {k: v for k, v in row.items() if k != "_query"}
            if result:
                out_row["placeName"] = result["name"]
                out_row["placeAddress"] = result["address"]
                out_row["latitude"] = result["latitude"]
                out_row["longitude"] = result["longitude"]
            else:
                out_row["placeName"] = ""
                out_row["placeAddress"] = ""
                out_row["latitude"] = ""
                out_row["longitude"] = ""
            writer.writerow(out_row)

    print(f"\nSaved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()