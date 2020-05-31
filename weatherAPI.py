from flask import Flask , request, render_template,jsonify
import psycopg2
from dbConnection import DatabaseConnection
import requests,json
from weatherAPIFunction import getQuery,getPlacePOI,getGeodatatminePOI,getDistance,getAddress,getID,getPointOfInterest,dis
import json

host='localhost'
database='da3t_db'
user='postgres'
password='db_password'

app=Flask('__name__')

connection=DatabaseConnection(user,password,host,database)
con=connection.getCon()
cur=con.cursor()

@app.route('/weather',methods=['POST','GET'])
def weather():
    if request.method =='GET':
        datetime=request.args['datetime']
        stationID=request.args['stationID']
        if datetime and stationID:
            querry="select * from weather where datetime=%s and weather_station=%s"
            try:

               cur.execute(querry,(datetime,stationID,))
               result=cur.fetchall()
            except:
                 return jsonify({'error':'Missing value or error format'})
            
            if result:
                return  jsonify({'date':str(result[0][0]).split(' ')[0],
                             'time':str(result[0][0]).split(' ')[1],
                             'weatherstation':result[0][1],
                             'description':result[0][2],
                             'temperature':int(result[0][3]),
                             'pressure':int(result[0][4]),
                             'humidity':int(result[0][5]),
                             'windspeed':int(result[0][6]),
                             'winddeg':int(result[0][7])
                            })
            else:
                return jsonify({'error':'no value for this date'})

            
        else:
            return jsonify({'error':'empty value'})

    if request.method=='POST':
         datetime=request.args['datetime']
         stationID=request.args['stationID']

         if datetime and stationID:

             querry="select * from weather where datetime=%s and weather_station=%s "

             try:
                 cur.execute(querry,(datetime,stationID,))
                 result=cur.fetchall()
             except:
                 return jsonify({'error':'Missing value or error format'})
             if result:
                 return  jsonify({'date':str(result[0][0]).split(' ')[0],
                             'time':str(result[0][0]).split(' ')[1],
                             'weatherstation':result[0][1],
                             'description':result[0][2],
                             'temperature':int(result[0][3]),
                             'pressure':int(result[0][4]),
                             'humidity':int(result[0][5]),
                             'windspeed':int(result[0][6]),
                             'winddeg':int(result[0][7])
                            })
             else:
                 return jsonify({'error':'no value for this date'})
     
         else:
             return jsonify({'error':'empty value'})

@app.route('/daycontext',methods=['GET','POST'])  
def daycontext():
    if request.method =='GET':
        date=request.args['date']
        stationID=request.args['stationID']
        if date and stationID:
            querry="select * from day_context where date=%s and weather_station=%s"
            try:
                cur.execute(querry,(date,stationID,))
                result=cur.fetchall()
            except:
                return jsonify({'error':'Missing value or error format'})
            
            if result:
                return  jsonify({'date':str(result[0][0]),
                             'sunrise':str(result[0][1]),
                             'sunset':str(result[0][2])
                            })
            else:
                return jsonify({'error':'no value for thid date'})
            
        else:
            return jsonify({'error':'empty value'})
    
    if request.method == 'POST':
        date=request.args['date']
        stationID=request.args['stationID']
        if date and stationID:
            querry="select * from day_context where date=%s and weather_station=%s"
            try:
                cur.execute(querry,(date,stationID,))
                result=cur.fetchall()
            except:
                return jsonify({'error':'Missing value or error format'})
            if result:
                return  jsonify({'date':str(result[0][0]),
                             'sunrise':str(result[0][1]),
                             'sunset':str(result[0][2])
                            })
            else:
                return jsonify({'error':'no value for thid date'})
        else:
            return jsonify({'error':'empty value'})

#service place
key='google_key'
@app.route('/place',methods=['POST','GET'])
def place():
    if request.method == 'GET':
        type=request.args['type']
        lat=request.args['lat']
        lon=request.args['lon']
        radius=request.args['radius']
        return getPlacePOI(lat,lon,radius,type,type,key)
    if request.method == 'POST':
        type=request.args['type']
        lat=request.args['lat']
        lon=request.args['lon']
        radius=request.args['radius']
        return getPlacePOI(lat,lon,radius,type,type,key)

#service datatourisme
@app.route('/datatourisme',methods=['POST','GET'])
def datatourisme():
    if request.method =='GET':
        type=str(request.args['type'])
        lat=request.args['lat']
        lon=request.args['lon']
        radius=float(request.args['radius'])
        radius=float(radius/1000)
        
        url = 'http://localhost:8080/'
        r = requests.post(url, json={'query': getQuery(type=type,lat=lat,lon=lon,radius=radius)})
        return r.json()


    if request.method=='POST':
        type=str(request.args['type'])
        lat=request.args['lat']
        lon=request.args['lon']
        radius=float(request.args['radius'])
        radius=float(radius/1000)
        
        url = 'http://localhost:8080/'
        r = requests.post(url, json={'query': getQuery(type=type,lat=lat,lon=lon,radius=radius)})
        return r.json()
        
#service geodatamine
@app.route('/geodatamine',methods=['GET','POST'])
def geodatamine():
    if request.method == 'GET':
        type=request.args['type']
        lat=request.args['lat']
        lon=request.args['lon']
        radius=float(request.args['radius'])
        radius=float(radius/1000)
        location={'lat':lat,'lon':lon}
        
        poiObject=getPointOfInterest(type,getID(getAddress(location))[0]['id'])
        poi=[]

        for p in poiObject['features']:
            latPoi=p['geometry']['coordinates'][1]
            lonPoi=p['geometry']['coordinates'][0]
            locationPoi={'lat':latPoi,'lon':lonPoi}
            distance=getDistance(location,locationPoi)
            if distance <= int(radius * 1000):
                poi.append(p)
        if poi:
            return jsonify(poi)
        else:
            return jsonify({'error':'no result'})


    if request.method == 'POST':
        type=request.args['type']
        lat=request.args['lat']
        lon=request.args['lon']
        radius=float(request.args['radius'])
        radius=float(radius/1000)
        location={'lat':lat,'lon':lon}

        poiObject=getPointOfInterest(type,getID(getAddress(location))[0]['id'])
        poi=[]

        for p in poiObject['features']:
            latPoi=p['geometry']['coordinates'][1]
            lonPoi=p['geometry']['coordinates'][0]
            locationPoi={'lat':latPoi,'lon':lonPoi}
            distance=getDistance(location,locationPoi)
            if distance <= int(radius * 1000):
                poi.append(p)
        if poi:
            return jsonify(poi)
        else:
            return jsonify({'error':'no result'})
        



if __name__=='__main__':
    app.run(debug=True)

