import requests
import json
import time
import boto3

country = "us"
url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsedates/v1.0/" + country + "/usd/en-us/LHR-sky/SFO-sky/2019-09-09/2019-09-10"

# takes information from configuration file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)
print(data)
rapid = data["Rapid-API"]
host = rapid["X-RapidAPI-Host"]
key = rapid["X-RapidAPI-Key"]


# Browse dates inbound (get req)
def find_flights():
    int(round(time.time() * 1000))
    response = requests.get(
        url,
        headers={'X-RapidAPI-Host': host,
                 'X-RapidAPI-Key': key,
                 }
    )
    print(find_flights().content)
    latency = (int(round(time.time() * 1000)) - millis)
    send_latency_cloudwatch(latency)
    return response

# sends latency metric to aws cloudwatch
def send_latency_cloudwatch(latency):
    client = boto3.client('cloudwatch')
    response = client.put_metric_data(
        Namespace='flight_price_alarm',
        MetricData=[
            {
                'MetricName': 'latency',
                'Value': latency,
                'Unit': 'Milliseconds'
            },
        ]
    )
    return response

