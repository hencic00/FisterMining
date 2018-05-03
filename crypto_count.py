import json
import os
import codecs
from collections import namedtuple
from crypto_dictionary import load_obj
import re
import analyze_sentiment_nltk as ansent
from multiprocessing import Process, Manager
import math

dirname = os.path.dirname(__file__)
relative_path = "tweets\979053718241918976_978993246129946624_20000.json"
filename = os.path.join(dirname, relative_path)

__main__ = True
dict = []
analysis = []

class Tweet:
    def __init__(self):
        self.cryptos = []
        self.sentiment = 0
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
        instance.sentiment=sent.analyse(tweet_text)[3]

        for word in wordList:
            if word in dict:
                instance.cryptos.append(word)

        analysis.append(instance)

    return analysis


def AnalyzeDataChunk(data, sent):
    for tweet in data:
        tweet_text = tweet['text'].encode('utf-8').lower()
        wordList = re.sub("[^\w]", " ",  tweet_text).split()  
        instance = Tweet()
        instance.tweet = tweet_text
        instance.sentiment=sent.analyse(tweet_text)[3]

        for word in wordList:
            if word in dict:
                instance.cryptos.append(word)

        analysis.append(instance)
    
    return True


def AnalizeTweetsMultiprocessed(numberOfProcesses):
    dict, sent = Init()

    data = []
    with codecs.open(filename,'rU','utf-8') as f:
        for line in f:
            # Parse JSON into an object with attributes corresponding to dict keys.
            x = json.loads(line)
            data.append(x)

    data_per_process = math.ceil(len(data) / float(numberOfProcesses))
    process_clusters = [] # array of data split into chunks, so we can divide them among multiple threads
    temp_list = []
    counter = 0 

    # splits data into process_clusters
    for data_index in range(0, len(data)):
        temp_list.append(data[data_index])
        counter += 1
        if(counter >= data_per_process or data_index == len(data) - 1):
            process_clusters.append(temp_list)
            temp_list = []
            counter = 0

    processes = []  # output array
    for i in range(0, numberOfProcesses):   
		if(i >= len(process_clusters)):
			break
		processes.append(Process(target = AnalyzeDataChunk, args =  (process_clusters[i], sent, )))
		processes[i].start()
        
    for k in range(0, len(processes)):
        processes[k].join()


    return processes


if __name__ == "__main__":
    AnalizeTweetsMultiprocessed(4)
    for i in analysis:
        print(i)
