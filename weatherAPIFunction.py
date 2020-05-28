import requests
from flask import jsonify
def getQuery(type,lat,lon,radius):
    query="""query{
                       poi(
                           size:%d,
                           filters:[
                               { isLocatedAt: {schema_geo: { _geo_distance: {lng: "%f" , lat: "%f" , distance: "%d" } }}},
                               {rdf_type: {_eq: "https://www.datatourisme.gouv.fr/ontology/core#%s"}}
                           ]
                       ){
                           total
                           results{
                               _uri
                               rdfs_label{
                                   value
                                   lang
                               }
                               rdfs_comment{
                                    value
                                    lang
                                }
                                 hasContact{
                                    foaf_homepage
                                    schema_legalName
                                    schema_logo
                                    schema_email
                                    schema_telephone
                                    schema_givenName
                                    schema_familyName

                                }
                               takesPlaceAt{
                                   startTime
                                   endDate
                                   endTime
                                   startDate
                               }
                                hasBeenCreatedBy{
                                    foaf_homepage
                                    schema_legalName
                                    schema_logo
                                    schema_email
                                    schema_telephone
                                    schema_givenName
                                    schema_familyName
                                }
                                
                                isLocatedAt{
                                    schema_address{
                                        schema_addressLocality
                                        schema_postalCode
                                        schema_streetAddress

                                    }
                                    schema_geo{
                                        schema_longitude
                                        schema_latitude

                                    }
                                }
                                
                                
                           }
                       }

                      }""" %(10,float(lon),float(lat),int(radius),type) 
    return query


def getPlacePOI(lat,lon,radius,keyword,type,key):
    
    url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&keyword={}&type={}&key={}"
    url=url.format(lat,lon,radius,keyword,type,key)
    response=requests.get(url)
    if response.status_code == 200:
        responseJson=response.json()
        return responseJson
    else:
        return {'error':'Connection Error {}'.format(response.status_code)}


def getGeodatatminePOI(type,id):
    url='https://geodatamine.fr/data/{}/{}?format=geojson&aspoint=true&radius=7'
    url=url.format(type,id)
    response=requests.get(url)
    if response.status_code == 200:
        responseJson=response.json()
        return responseJson
    else:
        return {'error':'Connection Error {}'.format(response.status_code)}

def getDistance(origin,poiLocation):
    url='https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={},{}&destinations={},{}&key='
    url=url.format(origin['lat'],origin['lon'],poiLocation['lat'],poiLocation['lon'])
    response=requests.get(url)
    if response.status_code == 200:
        return response.json()['rows'][0]['elements'][0]['distance']['value']
    else:
        return jsonify({'error':'connection error'})




#https://geodatamine.fr/boundaries/search?text=la%20rochellle
#https://geodatamine.fr/themes