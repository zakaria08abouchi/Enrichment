
from flask import Flask , jsonify , request
import psycopg2
from dbConnection import DatabaseConnection
from datetime import datetime , time , date , timezone
from geopy.distance import geodesic
from DA3T_STOP_Function import getUnixTime , getCenter , checkDistance
import folium , json


host='localhost'
database='da3t_db'
user='postgres'
password='barca821997'


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
                for obj in result:
                    A.append({"trajectoire":obj[0],
                               "time":obj[1],
                               "long":obj[2],
                               "lat":obj[3]})
                Points=[]
                Stop=[]
                i=0
                j=0

                while i <= len(A)-1 :
                    j=i+1
                    while j < len(A) and (getUnixTime(A[j]['time']) - getUnixTime(A[i]['time'])) <= int(time)*60 :
                        Points.append(A[j])
                        j=j+1
                    if len(Points) >= 2:
                        Points.append(A[i])
                    else:
                        Points=[]
                    if len(Points)>0:
                        center=getCenter(Points)
                        if checkDistance(Points,center,float(radius)) == True:
                            Stop.append(center) 
                      
                    Points=[]
                    i=i+1
                    j=0
                m = folium.Map(location=[46.1667, -1.15] , zoom_start=13)  
                k=1
                for obj in A :
                    folium.Marker([obj['lat'], obj['long']], tooltip='click me',popup="num_pos : "+str(k)+"\n\n lat : "+str(obj['lat'])+"\n\n lon :  "+str(obj['long'])+"\n\n time : "+str(obj['time']).split(' ')[1]+"\n\n traj_id : "+str(obj['trajectoire'])).add_to(m)
                    k=k+1
                for stop in Stop:
                    folium.Marker([stop['lat'], stop['lon']], tooltip='click me',popup="stop \n "+str(stop['lat'])+" "+str(stop['lon']), icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
                    folium.Circle(
                          radius=radius,
                          location=[ stop['lat'] , stop['lon'] ],
                          popup='stop',
                          color='crimson',
                          fill=False,
                            ).add_to(m)
                m.save('index.html')
                return jsonify(Stop)
        else:
            return jsonify({'error':'empty element'})
    
    if request.method=='POST':
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
                for obj in result:
                    A.append({"trajectoire":obj[0],
                               "time":obj[1],
                               "long":obj[2],
                               "lat":obj[3]})
                Points=[]
                Stop=[]
                i=0
                j=0

                while i <= len(A)-1 :
                    j=i+1
                    while j < len(A) and (getUnixTime(A[j]['time']) - getUnixTime(A[i]['time'])) <= int(time)*60 :
                        Points.append(A[j])
                        j=j+1
                    if len(Points) >= 2:
                        Points.append(A[i])
                    else:
                        Points=[]
                    if len(Points)>0:
                        center=getCenter(Points)
                        if checkDistance(Points,center,float(radius)) == True:
                            Stop.append(center) 
                      
                    Points=[]
                    i=i+1
                    j=0
                m = folium.Map(location=[46.1667, -1.15] , zoom_start=13)  
                k=1
                for obj in A :
                    folium.Marker([obj['lat'], obj['long']], tooltip='click me',popup="num_pos : "+str(k)+"\n\n lat : "+str(obj['lat'])+"\n\n lon :  "+str(obj['long'])+"\n\n time : "+str(obj['time']).split(' ')[1]+"\n\n traj_id : "+str(obj['trajectoire'])).add_to(m)
                    k=k+1
                for stop in Stop:
                    folium.Marker([stop['lat'], stop['lon']], tooltip='click me',popup="stop \n "+str(stop['lat'])+" "+str(stop['lon']), icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
                    folium.Circle(
                          radius=radius,
                          location=[ stop['lat'] , stop['lon'] ],
                          popup='stop',
                          color='crimson',
                          fill=False,
                            ).add_to(m)
                m.save('index.html')
                return jsonify(Stop)
        else:
            return jsonify({'eroor':'empty element'})       

if __name__ == '__main__':
    app.run(debug=True)



"""
SELECT ST_Distance(
			ST_Transform('SRID=4326;POINT(-1.15052603 46.16020276  )'::geometry, 3857),
			ST_Transform('SRID=4326;POINT(-1.15174341  46.15997644)'::geometry, 3857)
		) * cosd(42.3521);
        """