from datetime import datetime , time , date , timezone
from geopy.distance import geodesic
import folium
import matplotlib.pyplot as plt 
import numpy as np
from dbConnection import DatabaseConnection
from flask import jsonify

host='localhost'
database='da3t_db'
user='postgres'
password='barca821997'


def getUnixTime(dateTime):
    dateTime=str(dateTime)
    date=dateTime.split(' ')[0]
    time=dateTime.split(' ')[1]

    dt=datetime(int(date.split('-')[0]) , int(date.split('-')[1]) , int(date.split('-')[2]) , int(time.split(':')[0]) , int(time.split(':')[1]))
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)

def getCenter(Points):
    lat=0
    lon=0
    for p in Points:
        lat=lat+float(p['lat'])
        lon=lon+float(p['long'])
    center={'lat':float(lat/len(Points)),'lon':float(lon/len(Points))}
    return center

def checkTime(time_point_1 , time_point_2 , time):   # new function
    if ( getUnixTime(time_point_2) - getUnixTime(time_point_1) ) >= ( time * 60 ):
        
        return True
       
    else:
        return False

def existe(obj,Painted):
    for p in Painted:
        if p == obj:
            return True
        else:
            return False


        
def checkDistance(point_1 , point_2 , radius):
    
    p1=( float( point_1['lat'] ) ,  float( point_1['long'] ) )
    p2=( float( point_2['lat'] ) ,  float( point_2['long'] ) )
    if( geodesic(p1,p2).km * 1000 <= radius) :
        return True
    else:
        return False





def dis():
    c=(48.94916729374633 , 2.712422235848561)
    p=(48.961171845281726, 2.6660100518582475)
    return geodesic(c,p).km * 1000

def toHour (A):
    startHour=float(str(A[0]['time']).split(' ')[1].split(':')[0])
    startMinut=float(int(str(A[0]['time']).split(' ')[1].split(':')[1])/60)
    start=startHour+startMinut
    endHour=float(str(A[-1]['time']).split(' ')[1].split(':')[0])
    endMinut=float(int(str(A[-1]['time']).split(' ')[1].split(':')[1])/60)
    end=endHour+endMinut
    time={"start" : start ,  "end" : end}
    return time

def timeToFloat(m):
    startHour=float(str(m["start"]).split(' ')[1].split(':')[0])
    startMinut=float(int(str(m["start"]).split(' ')[1].split(':')[1])/60)
    start=startHour+startMinut
    endHour=float(str(m["end"]).split(' ')[1].split(':')[0])
    endMinut=float(int(str(m["end"]).split(' ')[1].split(':')[1])/60)
    end=endHour+endMinut
    time={"start" : start ,  "end" : end}
    return time

def timeToHour(point):
    date=str(point).split(' ')[0]
    time=str(point).split(' ')[1]
    hour=float(time.split(':')[0])
    minut=float(int(time.split(':')[1])/60)
    timeHour=hour+minut
    return timeHour

def visualise(trajectorys_stop_move , stops_duration , entering_time , trajectorys_weather , weathers):
    fig, gnt = plt.subplots( )
    gnt.set_ylim(0, 60)
    trajectoryDuration = toHour(trajectorys_stop_move)
   
    x_start = trajectoryDuration["start"] 
    x_end = trajectoryDuration["end"] 

    gnt.set_xlim(x_start, x_end)
    gnt.xticks(np.arange(x_start, x_end, 1))

    gnt.set_xlabel('trajectory duration') 
    gnt.set_ylabel('orchestration') 
    gnt.set_yticks([10, 40])
    gnt.set_yticklabels(['S/M', 'weather'])
    gnt.grid(True)

    # start visualise stop move
    for s in stops_duration:   #visualise stops
        time=timeToFloat(s)
        start_stop=time["start"]
        end_stop=time["end"]
        #gnt.broken_barh([(start, end-start)], (5, 10), facecolors =('tab:red'))
        gnt.broken_barh([(start_stop , end_stop-start_stop )], (5, 10), facecolors =('tab:red'))
        #print(str(start) + " "+ str(end)+'\n')
        #gnt.broken_barh([(trajectoryDuration["start"], trajectoryDuration["end"]-trajectoryDuration["start"])], (10, 30), facecolors =('tab:red'))
        time=None
        start=None
        end=None

    length = len(stops_duration)       #visualise move
    for i in range(length-1):
        stop_1=stops_duration[i]
        time1=timeToFloat(stop_1)
        stop_2=stops_duration[i+1]
        time2=timeToFloat(stop_2)
        if time2["start"]>time1["end"]:
            gnt.broken_barh([(time1["end"], time2["start"]-time1["end"])], (5, 10), facecolors =('tab:orange'))
            #gnt.broken_barh([( time1["start"]+ (entringTime / 60) , time2["start"]-time1["start"]- (entringTime / 60) )], (5, 10), facecolors =('tab:orange'))
    
    trajectory_duration=toHour(trajectorys_stop_move)
    first_stop=stops_duration[0]
    split_first_stop=timeToFloat(first_stop)
    if trajectory_duration["start"] < split_first_stop["start"]:
        gnt.broken_barh([(trajectory_duration["start"], split_first_stop["start"]-trajectory_duration["start"])], (5, 10), facecolors =('tab:orange'))

    #a2=toHour(trajectorys_stop_move)
    last_stop=stops_duration[-1]
    split_last_stop=timeToFloat(last_stop)
    if trajectory_duration['end'] > split_last_stop["end"] :
        gnt.broken_barh([(split_last_stop["end"], trajectory_duration["end"]-split_last_stop["end"])], (5, 10), facecolors =('tab:orange'))
    # end visualise stop move

    #start visualise weather

    connection=DatabaseConnection(user,password,host,database)
    con=connection.getCon()
    cur=con.cursor()

    trajectory_date =str( trajectorys_weather[0]['time'] ).split(' ')[0]
    #trajectory_date_start=trajectory_date + ' 00:00:00'
    #trajectory_date_end=trajectory_date + ' 23:00:00'
    trajectory_date_start='2020-05-04 00:00:00'
    trajectory_date_end='2020-05-04 23:00:00'
    #print(trajectory_date_start +'\n'+trajectory_date_end)

    #querry=" select * from weather where datetime between '2020-05-04 00:00:00' and '2020-05-04 03:00:00' "
    querry=" select datetime , description from weather where datetime between %s and %s "
    
    try:
        cur.execute(querry,(trajectory_date_start , trajectory_date_end ) )
        result=cur.fetchall()
        
    except:
        print("nononononon") 
    
    
    if result :
        weathers_values=[]
        for obj in result:
            weathers_values.append({'datetime' :  obj[0] , 'description':obj[1]})
            
    
    start_end_trajectory=toHour(trajectorys_weather)
    start_trajectory=int( str(start_end_trajectory['start']).split('.')[0] )
    end_trajectory=int( str(start_end_trajectory['end']).split('.')[0] )
    
    #print(str(start_trajectory) +'\n'+str(end_trajectory))
    weathers_values_to_hour=[]
    i=0
    for obj in weathers_values :
        time=timeToHour(obj['datetime'])
        objec={"time":int(time) , "description" : obj["description"]}
        weathers_values_to_hour.append(objec)
        i=i+1
        objec=None
    #print(str(i))
    #color=["tab:blue","tab:orange","tab:red","tab:green","tab:pink","tab:orange","tab:red","tab:green","tab:blue","tab:pink"]
    colors=['tab:blue', 'tab:orange', 'tab:green', 'tab:red','tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    i=start_trajectory
    j=end_trajectory
    k=0
    
    # while i < j:
    #
    #     while str(weathers_values_to_hour[i]['description']) != str(weathers_values_to_hour[i+1]['description']):
    #
    #         gnt.broken_barh([( i, 1  )], (30, 20), facecolors =(color[k])  )
    #
    #         print( str(weathers_values[i]['description']+str(i)+'\n'+weathers_values[i+1]['description']+str(i+1)+'\n') )
    #         i=i+1
    #         #print('inside'+str(i)+'\n')
    #         k=k+1
    #         if k == 9:
    #             k=0
    #     gnt.broken_barh([(i , 2  )], (30, 20), facecolors =(color[k+1])  )
    #     #print( str(weathers_values[i]['description'])+'n' )
    #     #print( 'n'+str(weathers_values[+1]['description']) )
    #     i=i+2
    #     if str(weathers_values_to_hour[i-1]['description']) != str(weathers_values_to_hour[i]['description']):
    #         k=k+1
    #     #print('out'+str(i)+'\n')


    # Karim's implementation

    current_hour = start_trajectory
    end_hour = end_trajectory
    color = 0

    previous_weather = str(weathers_values_to_hour[current_hour]['description'])

    while current_hour < end_hour:
        current_weather = str(weathers_values_to_hour[current_hour]['description'])
        if current_weather != previous_weather:
            color = 0 if (color == 9) else color + 1

        gnt.broken_barh([(current_hour, 1)], (30, 20), facecolors=(colors[color]))
        
        previous_weather = current_weather
        current_hour = current_hour + 1

    plt.tight_layout()
    plt.savefig("D:/etude/stage/Projet/developpement/code_source/application/stop_move/static/images/chart.png")
