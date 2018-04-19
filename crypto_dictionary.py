import requests
from requests.auth import HTTPDigestAuth
import json
import pickle
url = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
headers = {"Accept": "application/json"}
data = '{}'
dict  = {}

def save_obj(obj, name):
    with open('dictionaries/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('dictionaries/'+ name + '.pkl', 'rb') as f:
        return pickle.load(f)


""" #get cryptocurrency names and symbols
response = requests.get(url,data = data)
if(response.ok):
    jData = json.loads(response.content)
    print("Crypto market contains {0} cryptocurrencies".format(len(jData)))
    print("\n")
    
    for crypto in jData:
        dict[crypto['name'].encode('utf-8').lower()] = crypto['symbol'].encode('utf-8').lower()


#save to file
save_obj(dict, "cryptos")

#load from file
dict = load_obj("cryptos")
for c in dict:
    print (c)
    print dict[c] """

