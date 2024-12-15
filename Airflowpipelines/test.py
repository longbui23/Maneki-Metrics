import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib
import yfinance as yf
import json

ca = certifi.where()


username = urllib.parse.quote_plus('longb8186')
password = urllib.parse.quote_plus('longlong32')

uri = f"mongodb+srv://longb8186:longlong32@sp500comp.rnqta.mongodb.net/?retryWrites=true&w=majority&appName=SP500comp"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=ca)
db = client['sp500']
collection = db['news']

all_news = collection.find({'Symbol':'AAPL'})

print(all_news)