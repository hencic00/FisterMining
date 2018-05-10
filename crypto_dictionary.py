import requests
from requests.auth import HTTPDigestAuth
import json
import pickle

url = "https://api.coinmarketcap.com/v1/ticker/?limit=0"
headers = {"Accept": "application/json"}

#save to file
def save_obj(obj, name):
    with open('dictionaries/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

#load from file
def load_obj(name):
    with open('dictionaries/'+ name + '.pkl', 'rb') as f:
        return pickle.load(f)

#get cryptocurrency names and symbols
def load_online_dictionary():
    data = '{}'
    dict  = {}
    response = requests.get(url,data = data)
    if(response.ok):
        jData = json.loads(response.content)
        print("Crypto market contains {0} cryptocurrencies".format(len(jData)))
        print("\n")
        
        for crypto in jData:
            dict[crypto['name'].encode('utf-8').lower()] = crypto['symbol'].encode('utf-8').lower()
    
    return dict


if __name__ == "__main__":
    dict = load_obj("cryptos")
    save_obj(dict, "cryptos")
    for c in dict:
        print (c)
        print dict[c]

