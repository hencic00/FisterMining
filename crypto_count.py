import json
import os
import codecs
from collections import namedtuple
from crypto_dictionary import load_obj
import re
import analyze_sentiment_nltk as ansent

dirname = os.path.dirname(__file__)
relative_path = "tweets\979053718241918976_978993246129946624_20000.json"
filename = os.path.join(dirname, relative_path)

__main__ = True


class Tweet:
    def __init__(self):
        self.cryptos = []
        self.sentiment = []
        self.tweet = ""


def Init():
    dict = load_obj("cryptos")  # loads crypto names/symbols dictionary
    sent=ansent.SentimentAnalyse() # loads lexicon for nltk
    sent.downloadLexicon()
    return dict, sent


def AnalizeTweets():
    dict, sent = Init()

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
        instance.tweet = tweet_text
        instance.sentiment=sent.analyse(tweet_text)

        for word in wordList:
            if word in dict:
                instance.cryptos.append(word)

        analysis.append(instance)

    return analysis





if(__main__):
    analysis = AnalizeTweets()
    for i in analysis:
            if i.cryptos:
                print i.cryptos


