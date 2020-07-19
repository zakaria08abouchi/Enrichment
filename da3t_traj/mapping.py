import folium
import json
import os




c=['beige','purple','cadetblue','lightgreen','gray','pink','orange','darkred','lightblue','cadetblue']
i=0

jsonFile=open('input.json','r') 
jsonData=jsonFile.read()
obj=json.loads(jsonData)
m=folium.Map(location=[46.1667 , -1.15] , zoom_start=13)
for ob in obj['trajectories'] :
    if i == len(c):
        i=0
    for o in ob:
        folium.Marker([o['x'] ,o['y'] ] ,
               popup='actual position',
               tooltip='click for more info',
               icon=folium.Icon(color=c[i], icon='info-sign')).add_to(m)
    i=i+1



m.save('input.html')
print(str(i))

jsonFile2=open('output.json','r') 
jsonData2=jsonFile2.read()
obj2=json.loads(jsonData2)
j=0
m2=folium.Map(location=[46.16 , -1.15] , zoom_start=13)
for ob in obj2:
    if j == len(c):
        j=0
    for o in ob:
        folium.Marker([o['x'] ,o['y'] ] ,
               popup='actual position',
               tooltip='click for more info',
               icon=folium.Icon(color=c[j], icon='info-sign')).add_to(m2)
    j=j+1


m2.save('output.html')








