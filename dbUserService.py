import mysql.connector
import json


def db_connection ():
    # takes information from configuration file
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    print(data)
    mysqldb = data["mysql"]
    host = mysqldb["host"]
    user = mysqldb["user"]
    passwd = mysqldb["passwd"]
    db = mysqldb["db"]

    mydb = mysql.connector.connect(
      host = host,
      user = user,
      passwd=passwd,
      database=db
    )
    return mydb

mydb = db_connection()
mycursor = mydb.cursor()
create_table_statement = "CREATE TABLE IF NOT EXISTS users2 (username varchar(23) NOT NULL,apikey varchar(50) NOT NULL,email varchar(45) NOT NULL,PRIMARY KEY (apikey),UNIQUE KEY email_UNIQUE (email))"
#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

mycursor.execute(create_table_statement)

def create_user(username, email, apikey):
    sql = "insert into flight_requests.users (username, email, apikey) VALUES (%s, %s, %s)"
    val = (username, email, apikey)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

# mycursor = mydb.cursor()
#
# #mycursor.execute("USE cloudschool")
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)
#
# mycursor.execute("SELECT * FROM test")
#
# myresult = mycursor.fetchall()
#
# # for x in mycursor:
# #   print(x)
#
# for x in myresult:
#   print(x)