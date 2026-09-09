from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="brownies_market_lookup")

query = "Brownie's Market, East Lake Road, Sheffield Lake, OH"
location = geolocator.geocode(query)

if location:
    print(location.address)
    print((location.latitude, location.longitude))
else:
    print("No result found")