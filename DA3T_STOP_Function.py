
from datetime import datetime , time , date , timezone
from geopy.distance import geodesic

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

def checkDistance(Points , center , radius):
    
    i=0
    c = (center['lat'] , center['lon'])
    for point in Points:
        p=(point['lat'] , point['long'])
        if(geodesic(c,p).km * 1000 <= radius):
            i=i+1
    if len(Points) == i :
        return True

