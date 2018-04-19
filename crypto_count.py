import json
import os
import codecs
from collections import namedtuple
from crypto_dictionary import load_obj
import re

dirname = os.path.dirname(__file__)
relative_path = "tweets\979053718241918976_978993246129946624_20000.json"
filename = os.path.join(dirname, relative_path)

class Tweet:
    def __init__(self):
        self.cryptos = []
        self.sentiment_compoundSum = 0


#load from file
dict = load_obj("cryptos")  # crypto names/symbols dictionary
""" for c in dict:
    print (c)
    print dict[c] """

data = []
with codecs.open(filename,'rU','utf-8') as f:
    for line in f:
        # Parse JSON into an object with attributes corresponding to dict keys.
        x = json.loads(line)
        data.append(x)

analysis = []   
for tweet in data:
    tweet_text = tweet['text'].encode('utf-8').lower()
    wordList = re.sub("[^\w]", " ",  tweet_text).split()  
    instance = Tweet()

    for word in wordList:
        if word in dict:
            instance.cryptos.append(word)
            #TODO: dodaj sentiment analysis

    analysis.append(instance) #TODO: preveri, kako deluje obseg spremenljivk v Pythonu!


print analysis[4].cryptos
