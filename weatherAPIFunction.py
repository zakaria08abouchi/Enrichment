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
    url='https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={},{}&destinations={},{}&key=google_key'
    url=url.format(origin['lat'],origin['lon'],poiLocation['lat'],poiLocation['lon'])
    response=requests.get(url)
    if response.status_code == 200:
        return response.json()['rows'][0]['elements'][0]['distance']['value']
    else:
        return jsonify({'error':'connection error'})

def getAddress(location):
    url='https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&language=fr&result_type=locality|plus_code&key=google_key'
    url=url.format(location['lat'],location['lon'])
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results'][0]['address_components'][0]['short_name']
    else:
        return jsonify({'error':'function getAddress()'})

def getID(address):
    url='https://geodatamine.fr/boundaries/search?text={}'
    url=url.format(address)
    response=requests.get(url)
    if response.status_code == 200:
        return response.json()

def getPointOfInterest(type,id):
    url='https://geodatamine.fr/data/{}/{}?format=geojson&aspoint=true'
    url=url.format(type,id)
    response=requests.get(url)
    if response.status_code == 200:
        return response.json()
from math import sin, cos, sqrt, atan2, radians
def dis(loc1,loc2):
   R=6373.0
   lat1 = radians(loc1['lat'])
   lon1 = radians(loc1['lon'])
   lat2 = radians(loc2['lat'])
   lon2 = radians(loc2['lon'])
   dlon = lon2 - lon1
   dlat = lat2 - lat1
   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))
   return R * c






#https://geodatamine.fr/boundaries/search?text=la%20rochellle
#https://geodatamine.fr/themes
#https://www.gps-coordinates.net/api