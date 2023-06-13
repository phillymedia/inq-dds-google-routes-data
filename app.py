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

    df = calculateRoutes()

    timestamp = getSnapshotTime()

    saveDataToS3(json.dumps(df.to_dict(orient='records')),f'routes_{timestamp}.json')

    print("complete for", timestamp)
    
    time.sleep(600)