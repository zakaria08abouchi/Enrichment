import  json
from main import main

with open('input.json', 'r') as input_stream:
        parsed_input = json.loads(input_stream.read())

obj=main(parsed_input)
print('\n')
print(obj)


"""m=folium.Map(location=[35.300048416948435 , -120.65977871417999] , zoom_start=13)

jsonFile=open('input.json','r') 
jsonData=jsonFile.read()
obj=json.loads(jsonData)


t1=['pink','beige','cadetblue','red','lightblue','orange','white','lightred','lightgray','lightgreen','darkblue','darkgreen','darkred','blue','darkpurple','gray','green','orange','black','purple']
i=0
j=1
for o in obj['trajectories']:
   
    if i==len(t1)-1:
        i=0
    for t in o:
        folium.Marker([t['x'] , t['y']] ,
               popup='traj : \n'+str(j),
               tooltip='click for more info',
               icon=folium.Icon(color=t1[i], icon='info-sign')).add_to(m)
    i=i+1
    j=j+1
    

m.save('input.html')

m2=folium.Map(location=[35.300048416948435 , -120.65977871417999] , zoom_start=13)
jsonFile=open('output.json','r') 
jsonData=jsonFile.read()
obj2=json.loads(jsonData)

k=0
for o in obj2:
    if k==len(t1)-1:
        i=0
    for t in o:
        folium.Marker([t['x'] , t['y']] ,
               popup='traj: \n',
               tooltip='click for more info',
               icon=folium.Icon(color=t1[k], icon='info-sign')).add_to(m2)
    k=k+1

m2.save('output.html')"""




