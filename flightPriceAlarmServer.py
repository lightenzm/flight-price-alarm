import atexit
import uuid

import mysql.connector
# v2.x version - see https://stackoverflow.com/a/38501429/135978
# for the 3.x version
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import abort
from flask import request

from flightQuery import *

# Initiating a flask object
app = Flask(import_name=__name__)


# Setting up the content of the root path
@app.route('/')
def welcome_msg():
    return 'Hello and welcome to Flight price alarm!'


# Setting up the content of the signup path
@app.route(rule='/signup')
def sign_up():
    # Extracts the values from the address, for example username=Lightenzm (query parameters)
    username = request.args.get('username')
    email = request.args.get('email')
    # Creates a random API key
    apikey = str(uuid.uuid4().fields[-1])[:15]
    try:
        create_user(username, email, apikey)
    except mysql.connector.errors.IntegrityError as e:
        return "user already exists"
    return str(apikey)


@app.route(rule='/alarm')
def alarm():
    apikey = request.args.get('apikey')
    maxprice = request.args.get('maxprice')
    originplace = request.args.get('originplace')
    outboundpartialdate = request.args.get('outboundpartialdate')
    inboundpartialdate = request.args.get('inboundpartialdate')
    destinationplace = request.args.get('destinationplace')

    # Extracts the values from the address, for example username=Lightenzm (query parameters)
    # Creates a random API key
    try:
        if not (validatApiKey(apikey)):
            return abort(403)
        create_alarm_info(maxprice, apikey, originplace, destinationplace, outboundpartialdate, inboundpartialdate)
    except mysql.connector.errors.IntegrityError as e:
        return "db Error"
    return "OK"


# schedule 'find_flights_and_Alert'
scheduler = BackgroundScheduler()
scheduler.add_job(func=find_flights_and_Alert, trigger="interval", seconds=20)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Initiating a server

if __name__ == '__main__':
    app.run(host='0.0.0.0')
