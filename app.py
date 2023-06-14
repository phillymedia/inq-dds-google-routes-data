import pandas as pd
import numpy as np

import time
from datetime import datetime, timedelta, timezone

import requests
import json

import boto3
import string

from src.routes_func import calculateRoutes
from src.utils import saveDataToS3, getSnapshotTime

from dotenv import load_dotenv
load_dotenv('.env')

import os

while True:

    if datetime.now().hour >= 5 and datetime.now().hour <= 20:
    
        df = calculateRoutes()

        saveDataToS3(json.dumps(df.to_dict(orient='records')),f'routes_{timestamp}.json')

        timestamp = getSnapshotTime()

        print("complete for", timestamp)
    
    time.sleep(600)