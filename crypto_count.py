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
import matplotlib.pyplot as plt
import uuid

dirname = os.path.dirname(__file__)
relative_path = "tweets/979053718241918976_978993246129946624_20000.json"
results_folder_path = "./tweets/sentiment_results/"


class Tweet:
    def __init__(self):
        self.cryptos = []
        self.sentiment = 0
        self.created_at = ""


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
        instance.created_at = tweet['created_at'].encode('utf-8')
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


def AnalyzeDataChunk2(data, regexList, sent):
    output = []
   
    for tweet in data:
        tweet_text = tweet['text'].encode('utf-8').lower() 
        instance = Tweet()
        instance.created_at = tweet['created_at'].encode('utf-8')
        instance.sentiment=sent.analyse(tweet_text)[3]

        for crypto in regexList:
            m = re.match(".*[@# ]" + crypto + "[ ,.!?].*", tweet_text) #search for full crypto name
            if m:
                instance.cryptos.append(crypto)

        if len(instance.cryptos) != 0:  # ignores tweets that doesn't mention any of the cryptos from the dictionary
            output.append(json.dumps(instance.__dict__, ensure_ascii=False))
            #print((instance.cryptos))
        
    json_string = json.dumps(output, ensure_ascii=False) 
    filename = results_folder_path + "results" + str(uuid.uuid1())  
    with open(filename, 'w') as outfile:
        json.dump(json_string, outfile) 

    return True


def AnalyzeTweetsMultiprocessed(numberOfProcesses, filename, regexList):
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
        elif len(regexList)==0:
            processes.append(Process(target = AnalyzeDataChunk, args =  (process_clusters[i], dict, sent, i, )))
        else:
            processes.append(Process(target = AnalyzeDataChunk2, args =  (process_clusters[i], regexList, sent, )))

        processes[i].start()
        
    for k in range(0, len(processes)):
        processes[k].join()

    return processes


def ReadAnalyzedData(filename):
    with open(filename) as json_data:
        data = json.load(json_data)

    data = json.loads(data)
    return data


def graphDrawFromFilesBySlots(folderLoadPath, timeslots, timeFrom, timeTo, crypto_string):
    fromTimestamp = int(time.mktime(parse(timeFrom).timetuple()))
    toTimestamp = int(time.mktime(parse(timeTo).timetuple()))
    difference=toTimestamp-fromTimestamp
    stepSize=86400 #difference/timeslots
    counterArray=[0]*timeslots
    sentimentPos=[0]*timeslots
    sentimentNeu=[0]*timeslots
    sentimentNeg=[0]*timeslots
    sentimentPosSum=[0]*timeslots
    sentimentNegSum=[0]*timeslots
    for filename in os.listdir(folderLoadPath):
        with open(folderLoadPath+"/"+filename) as file:
            jsonData=json.load(file)
            for data in jsonData:
                cryptos = data["cryptos"]
                if not crypto_string in cryptos:
                    continue

                tweetTimestamp=int(time.mktime(parse(data["created_at"]).timetuple()))
                assignedSlot=int(math.floor((tweetTimestamp-fromTimestamp)/stepSize))
                if(assignedSlot>=timeslots):
                    assignedSlot=timeslots-1
                
                counterArray[assignedSlot]+=1
                sentimentValue=data["sentiment"]
                if(sentimentValue>0):
                    sentimentPos[assignedSlot]+=1
                    sentimentPosSum[assignedSlot]+=sentimentValue
                elif(sentimentValue<0):
                    sentimentNeg[assignedSlot]+=1
                    sentimentNegSum[assignedSlot]+=sentimentValue
                else:
                    sentimentNeu[assignedSlot]+=1

    sentimentPerSlot=[0]*timeslots
    for slt in range(0, timeslots):
    	sentimentPerSlot[slt]=sentimentPosSum[slt]+sentimentNegSum[slt]

    slotTimestamps=[None]*(timeslots)
    ticks=range(0, timeslots)
    for slot in range(0, timeslots-1):
    	slotTimestamps[slot]=str(datetime.datetime.fromtimestamp((fromTimestamp+stepSize*slot)).replace(tzinfo=timezone('CET')).strftime("%d-%m"))
    slotTimestamps[timeslots-1]=str(datetime.datetime.fromtimestamp(toTimestamp).replace(tzinfo=timezone('CET')).strftime("%d-%m"))
    x=range(timeslots)
    width=1
    fig=plt.figure(figsize=(9,9))
    
    #subplt=plt.subplot(1,1,1)
    #subplt.plot(sentimentPos, color="green")
    #subplt.plot(sentimentNeu, color="blue")
    #subplt.plot(sentimentNeg, color="red")

    plt.bar(x, sentimentPos, width=width*1, color="lightgreen", label="Positive Tweets")
    plt.bar(x, sentimentNeu, width=width*0.6, color="orange", label="Neutral Tweets")
    plt.bar(x, sentimentNeg, width=width*0.2, color="purple", label="Negative Tweets")
    plt.xticks(ticks, slotTimestamps, rotation="30")
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Ammount of Tweets", fontsize=14)
    

    fig2=plt.figure(figsize=(9,9))
    
    plt.bar(x, sentimentPerSlot)
    plt.xticks(ticks, slotTimestamps, rotation="30")
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Sentiment score", fontsize=14)
    plt.show()




if __name__ == "__main__":


    """
    folder_path = "C:/Users/Dejan/Desktop/SCHOOL/Povezljivi sistemi in inteligentne storitve/_tweetMiner/FisterMining/tweets/cryptocurrency/"
    filenames = os.listdir(folder_path)
    for i in range(0, len(filenames)):
        AnalyzeTweetsMultiprocessed(6, folder_path + "\\" + filenames[i], ["bitcoin", "ethereum", "btc", "eth"])
    """
    
    """
    ta = TweetAnalyzer()
    ta.getTweetsMultiprocessed("23/4/2018 00:00:00 +0000", "9/5/2018 23:59:59 +0000", "tweets/sentiment_results", "tweets/timestamped", 5000, 6)
    """
    
    
    graphDrawFromFilesBySlots("tweets/timestamped", 17, "23/04/2018 00:00:00 +0000", "09/05/2018 23:59:59 +0000", "ethereum")
    
    

    """
    dict = load_obj("cryptos")  # loads crypto names/symbols dictionary
    for i in dict:
        print(i)
    """

