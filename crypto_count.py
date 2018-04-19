import json
import os
import codecs
from collections import namedtuple
from crypto_dictionary import load_obj

dirname = os.path.dirname(__file__)
relative_path = "tweets\979053718241918976_978993246129946624_20000.json"
filename = os.path.join(dirname, relative_path)


data = []
with codecs.open(filename,'rU','utf-8') as f:
    for line in f:
        # Parse JSON into an object with attributes corresponding to dict keys.
        x = json.loads(line)
        data.append(x)
        
for tweet in data:
    tweet['text'].encode('utf-8').lower()


#load from file
#dict = load_obj("cryptos")
#for c in dict:
#    print (c)
#    print dict[c]