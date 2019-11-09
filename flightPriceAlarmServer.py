from flask import Flask
from flask import request
from dbUserService import create_user
import uuid
import mysql.connector

#Initiating a flask object
app = Flask(import_name=__name__)

#Setting up the content of the root path
@app.route('/')
def welcome_msg():
    return 'Hello and welcome to Flight price alarm!'

#Setting up the content of the signup path
#example: @app.route(rule ='/calc',methods= ['post'])
@app.route(rule ='/signup')
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

#Initiating a server
if __name__ == '__main__':
    app.run(host= '0.0.0.0')
