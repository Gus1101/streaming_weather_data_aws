import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]
LATITUDE = 23.5508
LONGITUDE = 46.9388

url = f"https://api.tomorrow.io/v4/weather/forecast?location={LATITUDE},{LONGITUDE}&apikey={API_KEY}"

headers = {"accept":"application/json"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))
else:
    print(f"Status code error:{response.status_code}")