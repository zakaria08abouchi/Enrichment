from flask import Flask , jsonify , request
import psycopg2
from dbConnection import DatabaseConnection
from DA3T_2TRAJ_Functions import convertToTraj
from main import main
import json

host='localhost'
database='da3t_db'
user='postgres'
password='barca821997'

app=Flask(__name__)

connection=DatabaseConnection(user,password,host,database)
con=connection.getCon()
cur=con.cursor()

@app.route('/DA3T_2TRAJ', methods=['GET' , 'POST'])
def traj():
    if request.method == 'GET':
        traj_1=request.args['traj1']
        traj_2=request.args['traj2']
        if traj_1 and traj_2 :
            query_1="select trajectory , time , ST_X(location::geometry) as latitude,ST_Y(location::geometry) as longitude from point where trajectory=%s"
            query_2="select trajectory , time , ST_X(location::geometry) as latitude,ST_Y(location::geometry) as longitude from point where trajectory=%s"
            try:
                cur.execute(query_1,(traj_1,))
                result_1=cur.fetchall()
                cur.execute(query_2,(traj_2,))
                result_2=cur.fetchall()
            except:
                return jsonify({'error':'trajectory not existe'})
            #return jsonify(result_2)
            if result_1 and result_2:
                input_object = convertToTraj(result_1,result_2)
                """with open('input.json', 'r') as input_stream:
                    parsed_input = json.loads(input_stream.read())"""

                with open('input.json', 'w') as output_stream:
                    output_stream.write(json.dumps(input_object,indent=4))

                output_object = main(input_object)

                with open('output.json', 'w') as output_stream:
                    output_stream.write(json.dumps(output_object,indent=4))
        
                return jsonify(output_object)
            else:
                return jsonify({'error':'empty result for entring trajectories'})


        else:
            return jsonify({'error':'empty element'})



if __name__ == '__main__' :
    app.run(debug=True)

