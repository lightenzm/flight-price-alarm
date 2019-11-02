from flask import Flask
from flask import request
from dbUserService import create_user
import uuid
import mysql.connector

app = Flask(import_name=__name__)

@app.route('/')
def welcome_msg():
    return 'Hello and welcome to Flight price alarm!'

#@app.route(rule ='/calc',methods= ['post'])
@app.route(rule ='/signup')
def sign_up():
    username = request.args.get('username')
    email = request.args.get('email')
    apikey = str(uuid.uuid4().fields[-1])[:15]
    try:
        create_user(username, email, apikey)
    except mysql.connector.errors.IntegrityError as e:
        return "user already exists"
    return str(apikey)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
