import pandas as pd
import numpy as np

from datetime import datetime, timedelta, timezone

import os

import requests
import json

import boto3
import string

def calculateRoutes():

    locations_a = [
        {"placename": "City Hall", "latlong": (39.952397,-75.163584)},
        {"placename": "First Bank of the US", "latlong": (39.9482458,-75.1465486)},
        {"placename": "Pat's King of Steaks", "latlong": (39.9336659,-75.1623161)},
        {"placename": "Stephen Girard Park", "latlong": (39.9224074,-75.1844242)}, # South Philly west of Broad
        {"placename": "Art Museum", "latlong": (39.9657038,-75.180172)},
        {"placename": "Malcolm X Memorial Park", "latlong": (39.9505757,-75.2365055)}, # West Philly
        {"placename": "Temple University", "latlong": (39.9830577,-75.158053)}
    ]

    locations_b = [
        {"placename": "Frankford Transportation Center", "latlong": (40.0207241,-75.0773766)},
        {"placename":"Northeast High School", "latlong": (40.0562487,-75.0768435)},
        {"placename": "Philadelphia Mills Mall", "latlong": (40.0722131,-75.070122)},
        {"placename": "Bensalem High School", "latlong": (40.1127089,-74.9363815)},
        {"placename": "Burlington City High School", "latlong": (40.0704719,-74.856208)},
        {"placename": "Palymra Municipal Court", "latlong": (40.0032616,-75.0412747)},
        {"placename": "King of Prussia Mall", "latlong": (40.0884892,-75.3952688)}
    ]

    origins = []
    destinations = []

    for loc_a in locations_a:
        waypoint = {
          "waypoint": {
            "location": {
              "latLng": {
                "latitude": loc_a['latlong'][0],
                "longitude": loc_a['latlong'][1]
              }
            }
          }
        }
        origins.append(waypoint)

    for loc_b in locations_b:
        waypoint = {
          "waypoint": {
            "location": {
              "latLng": {
                "latitude": loc_b['latlong'][0],
                "longitude": loc_b['latlong'][1]
              }
            }
          }
        }
        destinations.append(waypoint)

    matrix_params_there = {
        "origins": origins,
        "destinations": destinations,
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE"
    }

    matrix_params_back = {
        "origins": destinations,
        "destinations": origins,
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE"
    }

    response_there = requests.post(
        url = 'https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix',
        data = json.dumps(matrix_params_there),
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-FieldMask' : 'originIndex,destinationIndex,duration,distanceMeters,status,condition,travelAdvisory',
            'X-Goog-Api-Key' : os.getenv("ROUTES_API_KEY")
        }
    )

    response_back = requests.post(
        url = 'https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix',
        data = json.dumps(matrix_params_back),
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-FieldMask' : 'originIndex,destinationIndex,duration,distanceMeters,status,condition,travelAdvisory',
            'X-Goog-Api-Key' : os.getenv("ROUTES_API_KEY")
        }
    )

    results_there = response_there.json()
    results_back = response_back.json()
    
    for result in results_there:
        result['originName'] = locations_a[result['originIndex']]['placename']
        result['destinationName'] = locations_b[result['destinationIndex']]['placename']
        result['duration'] = int(result['duration'][:-1])/60
    for result in results_back:
        result['originName'] = locations_a[result['destinationIndex']]['placename']
        result['destinationName'] = locations_b[result['originIndex']]['placename']
        result['duration'] = int(result['duration'][:-1])/60 

    df_there = pd.DataFrame(results_there)
    df_back = pd.DataFrame(results_back)
    df = pd.concat([df_there,df_back],axis=0)
    
    return df