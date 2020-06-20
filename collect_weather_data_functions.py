import requests
import json
from datetime import datetime,timedelta,timezone



def getWeatherData(location,unixDate,key):
    
    
    url='https://api.openweathermap.org/data/2.5/onecall/timemachine?lang=fr&units=metric&lat={}&lon={}&dt={}&appid={}'
    url=url.format(location['lat'],location['lon'],unixDate,key)
    response=requests.get(url)
    if response.status_code == 200:
         return response.json()    
    else:
        print("error loading data from openweathermap",response.status_code)

def getUnixTime(previousDay):
    dt=datetime(int(previousDay.split('-')[0]) , int(previousDay.split('-')[1]) , int(previousDay.split('-')[2]))
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)

def getPreviousDay():
    Previous_Date = datetime.today() - timedelta(days=1)
    date=str(Previous_Date).split(' ')
    return date[0]


def convertToUTC(unix):
    return datetime.utcfromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')

def updateDB(cursor,connection,objectJsonData):
    for obj in objectJsonData['hourly'] :
        cursor.execute("insert into public.weather(datetime,weather_station,description,temperature,pressure,humidity,wind_speed,wind_degree) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   (convertToUTC(obj['dt']),'17300001' ,obj['weather'][0]['description'],obj['temp'],obj['pressure'],obj['humidity'],obj['wind_speed'],obj['wind_deg']))
    #print('\n'+convertToUTC(objectJsonData['current']['dt'])+'\n')
    cursor.execute("insert into public.day_context(date,sunrise,sunset,weather_station)values(%s,%s,%s,%s)",(convertToUTC(objectJsonData['current']['dt']),convertToUTC(objectJsonData['current']['sunrise']).split(' ')[1],convertToUTC(objectJsonData['current']['sunset']).split(' ')[1],'17300001'))
    connection.commit()
    cursor.close()
    connection.close()
    print("\n upditing sucssesfuly done ...")