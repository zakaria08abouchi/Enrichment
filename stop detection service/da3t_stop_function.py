
from datetime import datetime , time , date , timezone
from geopy.distance import geodesic
import folium

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

#print( dis() )

def map(A,m,Stop,radius):
    k=1
    for obj in A :
        if k==1:
            folium.Marker([ float(obj['lat']) , float(obj['long']) ] ,
               popup= 'num_traj'+str(obj['num'])+'\n time'+str(obj['time']),
               tooltip='click',
               icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
            k=2
        folium.Marker([ float(obj['lat']) , float(obj['long']) ] ,
               popup= 'num_traj'+str(obj['num'])+'\n time'+str(obj['time']),
               tooltip='click').add_to(m)
    for s in Stop :
        folium.Circle(
                location=[ s['lat'], s['long'] ],
                radius=radius,
                color='#BF0000').add_to(m)
