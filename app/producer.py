import requests
import os
import json
import boto3

#API configuration 
API_KEY = os.getenv("API_KEY")
LATITUDE = 23.5508
LONGITUDE = 46.9388

url = f"https://api.tomorrow.io/v4/weather/realtime?location={LATITUDE},{LONGITUDE}&apikey={API_KEY}"
headers = {"accept":"application/json"}

#Kinesis Configuration
STREAM_NAME = os.getenv("STREAM_NAME")
REGION = os.getenv("REGION")

#Kinesis Client
kinesis_client = boto3.client("kinesis",region_name=REGION)

#Lambda functions
def lambda_handler(event, context):
    
    response = requests.get(url=url, headers=headers)
    weather_data = response.json()

    kinesis_client.put_record(
        StreamName = STREAM_NAME,
        Data = json.dumps(weather_data),
        PartitionKey = "partition_key",
    )

    return {
        "statusCode":200,
        "body":json.dumps("Daos enviados ao Kinesis com sucesso"),
    }