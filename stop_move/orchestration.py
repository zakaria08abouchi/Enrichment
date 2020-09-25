from flask import jsonify , Flask , request , render_template
import psycopg2
from dbConnection import DatabaseConnection
import json
from datetime import datetime , time , date , timezone
from geopy.distance import geodesic
import matplotlib.pyplot as plt 
import os
from orchestration_function import *


images_folder= os.path.join('static' , 'images')





host='localhost'
database='da3t_db'
user='postgres'
password='barca821997'

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = images_folder

connection=DatabaseConnection(user,password,host,database)
con=connection.getCon()
cur=con.cursor()

@app.route('/da3t_orchestration', methods=['GET' , 'POST'])
def orchestration():
    if request.method=='GET' :
        trajectory=request.args['trajectory']
        radius=request.args['radius']
        time=request.args['time']
        station= str(request.args['station'])
        if trajectory and radius and time and station :
            querry1="select trajectory, time ,ST_X(location::geometry),ST_Y(location::geometry) from point where trajectory=%s"
            querry2="select trajectory , time from point where trajectory = %s"
            querry3="select datetime , weather_station , description from weather where weather_station = %s"
            try:
                cur.execute(querry1,(trajectory,))
                result1=cur.fetchall()
                #return jsonify(result1)
                cur.execute(querry2,(trajectory,))
                result2=cur.fetchall()
                cur.execute(querry3,(station,))
                result3=cur.fetchall()
            except:
                return jsonify({'error':'trajectory not existe'})
            if result1 and result2 and result3 :
                trajectorys_stop_move =[]
                i=1#
                for obj in result1:
                    trajectorys_stop_move.append({"trajectoire":obj[0],
                               "time":obj[1],
                               "long":obj[2],
                               "lat":obj[3],
                               "num":i})#
                    i=i+1 #

                # stop algo
                
                Points=[]
                Stop=[]
                stops_duration=[]
                i=0
                j=0
                while i < len(trajectorys_stop_move)-1:
                    
                    j=i+1
                    while j < len(trajectorys_stop_move) and checkDistance( trajectorys_stop_move[i] , trajectorys_stop_move[j] , float(radius) ) == True :
                        Points.append( trajectorys_stop_move[j] )
                        j=j+1
                    if len(Points) >= 2:
                        center=getCenter(Points)
                        Points.insert(0 , trajectorys_stop_move[i])
                        if checkTime( Points[0]['time'] , Points[-1]['time'] , float(time) ) == True :
                            Stop.append(center)  
                            stops_duration.append({ "start" : Points[0]['time'] , "end" : Points[-1]['time'] })
                            
                    i=i+j
                    j=0
                    Points=[]
                    #end stop algo

                    # start weather visualisation
                    trajectorys_weather=[]
                    weathers=[]
                    i=1#
                    for obj2 in result2:
                        trajectorys_weather.append({"trajectoire":obj2[0],
                               "time":obj2[1],
                               "num":i})
                        i=i+1 
                    j=1
                    for obj3 in result3:
                        weathers.append({"datetime":obj3[0],
                               "station":obj3[1],
                               "description":obj3[2]})#
                        j=j+1
                    # end weather visualisation
                if len(stops_duration)>0 :
                    visualise(trajectorys_stop_move , stops_duration , float(time) , trajectorys_weather , weathers)
                    full_filename=os.path.join(app.config['UPLOAD_FOLDER'] , 'chart.png')
                    return render_template("chart.html", user_image = full_filename)
                
                #return jsonify(Stop)
            return jsonify(stops_duration)

if __name__ == '__main__':
    app.run(debug=True)