import json
import os
import codecs
from collections import namedtuple
from crypto_dictionary import load_obj
from crypto_dictionary import load_online_dictionary
import re
import analyze_sentiment_nltk as ansent
from multiprocessing import Process, Manager
import math
import re
import time
import datetime
from dateutil.parser import parse
from pytz import timezone
from tweetAnalyzer import TweetAnalyzer

dirname = os.path.dirname(__file__)
relative_path = "tweets/979053718241918976_978993246129946624_20000.json"
results_folder_path = "./tweets/sentiment_results/"


class Tweet:
    def __init__(self):
        self.cryptos = []
        self.sentiment = 0
        self.tweet_date = ""


def Init():
    dict = load_obj("cryptos")  # loads crypto names/symbols dictionary
    dict = load_online_dictionary()
    sent=ansent.SentimentAnalyse() # loads lexicon for nltk
    sent.downloadLexicon()
    return dict, sent


def AnalyzeTweets():
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


def AnalyzeDataChunk(data, dict, sent, processID):
    output = []
   
    for tweet in data:
        tweet_text = tweet['text'].encode('utf-8').lower() 
        instance = Tweet()
        instance.tweet_date = tweet['created_at'].encode('utf-8')
        instance.sentiment=sent.analyse(tweet_text)[3]

        for crypto in dict:
            m = re.match(".*[@# ]" + crypto + "[ ,.!?].*", tweet_text) #search for full crypto name
            if m:
                instance.cryptos.append(crypto)
            else:
                m = re.match(".*[@# ]" + dict[crypto] + "[ ,.!?].*", tweet_text) #search for acronym
                if m and len(dict[crypto]) > 2:
                    instance.cryptos.append(crypto)

        if len(instance.cryptos) != 0:  # ignores tweets that doesn't mention any of the cryptos from the dictionary
            output.append(json.dumps(instance.__dict__, ensure_ascii=False))
            #print((instance.cryptos))
        
    json_string = json.dumps(output, ensure_ascii=False) 
    filename = results_folder_path + "results" + str(processID)  
    with open(filename, 'w') as outfile:
        json.dump(json_string, outfile) 

    return True


def AnalyzeTweetsMultiprocessed(numberOfProcesses, filename):
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
		processes.append(Process(target = AnalyzeDataChunk, args =  (process_clusters[i], dict, sent, i,)))
		processes[i].start()
        
    for k in range(0, len(processes)):
        processes[k].join()


    return processes


def ReadAnalyzedData():
    return
    
def getTweetsInTimespanAndAnalyze(startTime, endTime, numberOfSlots, folderLoadPath, folderSavePath, saveLimit):
    

if __name__ == "__main__":
    
    

    #filename = os.path.join(dirname, relative_path)
    #AnalyzeTweetsMultiprocessed(6, filename)

    """
    dict = load_obj("cryptos")  # loads crypto names/symbols dictionary
    for i in dict:
        print(i)
    """
    
    #AnalizeTweets()

