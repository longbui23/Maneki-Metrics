#cloud
import boto3 #AWS
import io
import certifi
import urllib

from google.oauth2 import service_account #GCP
from google.cloud import bigquery 

from pymongo.mongo_client import MongoClient #MongoDB
from pymongo.server_api import ServerApi

import streamlit as st


def connect_bigquery():
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
    )


    credentials = service_account.Credentials.from_service_account_file('gcp_key.json')
    client = bigquery.Client(credentials=credentials)

    return client


def connect_mongo():

    ca = certifi.where()
    uri = f"mongodb+srv://longb8186:##sp500comp.rnqta.mongodb.net/?retryWrites=true&w=majority&appName=SP500comp"

    # Create a new client and connect to the server
    mongo_client = MongoClient(uri, tlsCAFile=ca)

    return mongo_client