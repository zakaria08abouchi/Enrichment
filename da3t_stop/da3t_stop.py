from flask import Flask , jsonify , request
import psycopg2
from dbConnection import DatabaseConnection
from datetime import datetime , time , date , timezone
from geopy.distance import geodesic
from da3t_stop_function import getUnixTime , getCenter , checkDistance , checkTime , existe
import folium , json



host='localhost'
database='da3t_db'
user='postgres'
password='your pass word DB'

app=Flask(__name__)

connection=DatabaseConnection(user,password,host,database)
con=connection.getCon()
cur=con.cursor()

@app.route('/DA3T_STOP' , methods=['GET' , 'POST'])
def stop():
    if request.method == 'GET':
        trajectory=request.args['trajectory']
        radius=request.args['radius']
        time=request.args['time']
        if trajectory and radius and time :
            querry="select trajectory, time ,ST_X(location::geometry),ST_Y(location::geometry) from point where trajectory=%s"
            try:
                cur.execute(querry,(trajectory,))
                result=cur.fetchall()
            except:
                return jsonify({'error':'trajectory not existe'})
            if result:
                A=[]
                i=1
                for obj in result:
                    A.append({"trajectoire":obj[0],
                               "time":obj[1],
                               "long":obj[2],
                               "lat":obj[3],
                               "num":i})#
                    i=i+1 #
                
                
                painted=[]
                color=['green','orange','pink','black']
                Points=[]
                Stop=[]
                i=0
                j=0
                k=0
                m=folium.Map(location=[46.1667 , -1.15] , zoom_start=13)

                while i < len(A)-1:
                    
                    j=i+1
                    while j < len(A) and checkDistance( A[i] , A[j] , float(radius) ) == True :
                        Points.append( A[j] )
                        j=j+1
                    if len(Points) >= 2:
                        center=getCenter(Points)
                        Points.insert(0 , A[i])
                        if checkTime( Points[0]['time'] , Points[-1]['time'] , float(time) ) == True :
                            Stop.append(center)  
                            for p in Points :
                                painted.append(p)
                                folium.Marker([ float(p['lat']) , float(p['long']) ] ,
                             
                                        popup='hrl',
                                        tooltip='click',
                                        icon=folium.Icon(color=color[k], icon='info-sign')).add_to(m)
                            k=k+1
                            if k == len(color):
                                k=0


                    i=i+j
                    j=0
                    Points=[] 
                           
                for obj in A :
                    folium.Marker([ float(obj['lat']) , float(obj['long']) ] ,
                                  popup= 'num_traj'+str(obj['num'])+'\n time'+str(obj['time']),
                                tooltip='click').add_to(m)
                for s in Stop :
                    folium.Marker([ float(s['lat']) , float(s['lon']) ] ,
                             
                             popup='hrl',
                             tooltip='click',
                             icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
                    folium.Circle(
                           location=[ s['lat'], s['lon'] ],
                            radius=float(radius),
                           color='#BF0000').add_to(m)
                
                m.save('map3.html')

                return jsonify(Stop)


if __name__ == '__main__':
    app.run(debug=True)