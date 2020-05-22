import requests
import json
import psycopg2
from datetime import datetime,timedelta,date
from collect_weather_data_functions import getWeatherData,getUnixTime,getPreviousDay
from collect_weather_data_functions import convertToUTC,updateDB
from dbConnection import DatabaseConnection



key='e02bd93fa40dc48a804040fc963880c7'   
host='localhost'
database='da3t_db'
user='postgres'
password='barca821997'
location={"lat":46.166,"lon":-1.15}

connection=DatabaseConnection(user=user,password=password,host=host,database=database)
if connection:
    con=connection.getCon()
    cursor=con.cursor()
    obj=getWeatherData(location,getUnixTime(getPreviousDay()),key)  #get openweathermap data
    updateDB(cursor,con,obj)                                        #insert data on DB
else:
    print("error conecting ...")






