import mysql.connector
import json


def db_connection ():
    # takes information from configuration file
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    print(data)
    #Takes the values from the config file ant puts it into vars
    mysqldb = data["mysql"]
    host = mysqldb["host"]
    user = mysqldb["user"]
    passwd = mysqldb["passwd"]
    db = mysqldb["db"]
    #opens a connection to the DB
    mydb = mysql.connector.connect(
      host = host,
      user = user,
      passwd=passwd,
      database=db
    )
    return mydb

#Connect to the DB with details taken in db_connection
mydb = db_connection()

#Enables the use of multiple environments with the same connection?
mycursor = mydb.cursor()

#Creates a users table if not exists
create_users_table_statement = "CREATE TABLE IF NOT EXISTS users (username varchar(23) NOT NULL,apikey varchar(50) NOT NULL,email varchar(45) NOT NULL,PRIMARY KEY (apikey),UNIQUE KEY email_UNIQUE (email))"

#Creates a alarm_req table if not exists
create_alarms_table_statement = ("CREATE TABLE IF NOT EXISTS flightsAlarm.alarm_req ("+
  "id INT auto_increment NOT NULL,"+
  "maxprice INT NOT NULL,"+
  "apikey VARCHAR(50) NOT NULL,"+
  "originplace VARCHAR(45) NOT NULL,"+
  "destinationplace VARCHAR(45) NOT NULL,"+
  "outboundpartialdate VARCHAR(45) NOT NULL,"+
  "inboundpartialdate VARCHAR(45) NOT NULL,"+
  "PRIMARY KEY (id),"+
  "INDEX apikey_idx (apikey ASC),"+
  "CONSTRAINT apikey"+
   " FOREIGN KEY (apikey)"+
   " REFERENCES flightsAlarm.users (apikey)"+
   " ON DELETE NO ACTION"+
   " ON UPDATE NO ACTION);"
)


mycursor.execute(create_users_table_statement)
mycursor.execute(create_alarms_table_statement)

#takes user details and put them as values in the users table
def create_user(username, email, apikey):
    sql = "insert into flightsAlarm.users (username, email, apikey) VALUES (%s, %s, %s)"
    #replace %s with username, email,apikey?
    val = (username, email, apikey)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

#takes user alarm req parameters and put them as values in the alarm_req table
def create_alarm_info(maxprice, apikey, originplace, destinationplace, outboundpartialdate, inboundpartialdate):
    sql = "insert into flightsAlarm.alarm_req (maxprice, apikey, originplace, destinationplace, outboundpartialdate, inboundpartialdate) VALUES (%s, %s, %s, %s, %s, %s)"
    #replace %s with apikey, originplace, destinationplace, outboundpartialdate, inboundpartialdate?
    val = (int(maxprice), apikey, originplace, destinationplace, outboundpartialdate, inboundpartialdate)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

#create_alarm_info("100", "7546478463120", "SFO-sky", "JFK-sky", "2019-12-01", "2019-12-05")
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