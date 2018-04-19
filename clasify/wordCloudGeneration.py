from os import path
from wordcloud import wordcloud
import json
import pickle

def load_obj(name):
    with open('../dictionaries/'+ name + '.pkl', 'rb') as f:
        return pickle.load(f)

def getCryptoCurrencyCount(wordCountFP, dictionaryFP):
	data=json.load(open(wordCountFP))
	dictionary=load_obj(dictionaryFP)
	for entry in data:
		for c in dictionary:
			if(entry[0].lower()==c):
				print(c)

getCryptoCurrencyCount("tokens.json", "cryptos")
