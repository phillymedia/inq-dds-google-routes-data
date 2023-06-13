import pandas as pd
import numpy as np

from datetime import datetime, timedelta, timezone

import requests
import json

import boto3
import string

from dotenv import load_dotenv
load_dotenv('.env')

import os

s3 = boto3.client('s3',aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
         aws_secret_access_key= os.getenv("AWS_SECRET_ACCESS_KEY"))
headers = {'content-type': 'application/json'}

def saveDataToS3(dict_data, s3_filename):
    """
    Function to convert and save Python dicts as json files in s3 buckets.
    Parameters:
        - dict_data : dict
            dict to be sent to s3 as a json file
        - s3_filename : str
            Name of the json file in s3.
        - s3_bucket : str
            Name of s3 bucket that we're sending file to.
        - s3_path : str
            Name of path within the s3 bucket.
    """
    upload_byte_stream = dict_data
    s3_bucket = os.getenv("AWS_BUCKET_NAME")
    s3_path = os.getenv("AWS_BUCKET_PATH")
    s3.put_object(  Body=upload_byte_stream, 
                    Bucket=s3_bucket, 
                    Key='{}/{}'.format(s3_path, s3_filename),
                    # ACL='public-read',
                    CacheControl = 'max-age=30')
    
def getSnapshotTime():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    second = str(now.second).zfill(2)

    return '{}_{}_{}_{}_{}_{}'.format(year, month, day, hour, minute, second)