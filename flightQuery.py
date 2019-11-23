import requests
import time
import boto3
from dbUserService import *


MAX_PRICE = 1000000
# read Rapid-API configurations from the configuration file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)
rapid = data["Rapid-API"]
host = rapid["X-RapidAPI-Host"]
key = rapid["X-RapidAPI-Key"]


# Browse flights
def find_flights(originplace, destinationplace, outboundpartialdate, inboundpartialdate):
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsedates/v1.0/US/usd/en-us/{}/{}/{}?inboundpartialdate={}".format(
        originplace, destinationplace, outboundpartialdate, inboundpartialdate)

    response = requests.get(
        url,
        headers={'X-RapidAPI-Host': host,
                 'X-RapidAPI-Key': key,
                 }
    )
    #print(find_flights().content)
    return response.json()

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

# List airports ('Place Id') by Country name
def listPlaces(city):
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/US/USD/en-us/?query={}".format(city)
    response = requests.get(
        url,
        headers={'X-RapidAPI-Host': host,
                 'X-RapidAPI-Key': key,
                 }
    )
    return response.json()

#browse flights for user alerts
def find_flights_and_Alert():
    print("in find_flights_and_Alert")

    #start time for the latency metric
    millis = int(round(time.time() * 1000))

    alarms = getAlarms()
    for alarm in alarms:
        id = alarm[0]
        maxPrice= alarm[1]
        apikey = alarm[2]
        originplace = alarm[3]
        destinationplace = alarm[4]
        outboundpartialdate = alarm[5]
        inboundpartialdate = alarm[6]

        # use the first airport ID. In the future will loop on all airports

        minPriceFound = MAX_PRICE
        carrier = ""
        originAirports = listPlaces(originplace)['Places']
        destinationAirports = listPlaces(destinationplace)['Places']
        print("Looping over all possible routes. Looking for price under {} USD".format(maxPrice))
        for originAirport in originAirports:
            for destinationAirport in destinationAirports:
                response = find_flights(originAirport['PlaceId'], destinationAirport['PlaceId'], outboundpartialdate, inboundpartialdate)
                # Waits for the response to be ready...
                #time.sleep(2)
                try:
                    if (len(response['Quotes']) > 0):
                        minPriceForRoute = int(response['Quotes'][0]['MinPrice'])
                        print("minPrice for route {} => {}, for alarm ID {} is: {} ".format(originAirport['PlaceId'], destinationAirport['PlaceId'], id, str(minPriceForRoute)))
                        if (minPriceForRoute < minPriceFound):
                            minPriceFound = minPriceForRoute
                            carrier = response['Carriers'][0]['Name']
                except:
                    print("error parsing data from skyscanner")
        if (minPriceFound < maxPrice):
            print("found flight for alarm ID {} for {} USD with carrier {}".format(id, minPriceFound, carrier))
            print("deleteting alarm {}".format(id))
            deleteAlarm(id)
        else:
            print("no flights under {} USD for alarm ID {}. min price is: {}".format(maxPrice, id, minPriceFound))

    latency = (int(round(time.time() * 1000)) - millis)
    #Sends latency metric to cloudwatch
    send_latency_cloudwatch(latency)

find_flights_and_Alert()