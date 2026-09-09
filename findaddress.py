import requests

query = """
[out:json];
(
  node["name"~"Brownie's Market",i](41.3,-82.3,41.6,-81.9);
  way["name"~"Brownie's Market",i](41.3,-82.3,41.6,-81.9);
);
out center;
"""

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "User-Agent": "python-requests/geocoding-test"
}

response = requests.post(
    "https://overpass.kumi.systems/api/interpreter",
    data={"data": query},
    headers=headers
)

print("Status code:", response.status_code)
print("Response text:", response.text[:500])