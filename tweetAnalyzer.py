import os
import json
import time
import datetime
import progressbar
from dateutil.parser import parse
from pytz import timezone

class TweetAnalyzer:
	"""
	parameters: 
		startTime(string) = save tweets that are posted after this time;
		endTime(string) = save tweets that are posted before this time;
		folderPath(string) = folder where the tweet files are saved in JSON format, 20000 tweets per file;
	"""
	def getTweetsWithinTimeSpan(self, startTime, endTime, folderPath):
		validTweets = []
		lineNumber = 0
		try:
			fromTimestamp = int(time.mktime(parse(startTime).timetuple()))
			toTimestamp = int(time.mktime(parse(endTime).timetuple()))
			fileCount = len(os.listdir(folderPath))
			bar = progressbar.ProgressBar(maxval = fileCount * 20000, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
			bar.start()
			for filename in os.listdir(folderPath):
				with open(folderPath + "/" + filename, "r") as file:
					for line in file:
						lineNumber = lineNumber + 1					
						jsonData = json.loads(line)
						createdAt = jsonData["created_at"]
						dt = parse(createdAt)
						timestamp = int(time.mktime(dt.timetuple()))
						if(timestamp >= fromTimestamp and timestamp <= toTimestamp):
							validTweets.append(jsonData)
						bar.update(lineNumber)
			bar.finish()
			return validTweets
		except:
			print("An error occured! Check the datetime input format 'day/month/year hour:minute:second timezone' example: '28/3/2018 13:00:00 +0000'")
			return

	"""
	parameters: 
		tweetsList(list) = list of tweets in json format; 
		indents(int) = number of indents used to print json format; 
		sortKeys(boolean) = sort JSON keys by alphabet;
	"""
	def printTweetsInJsonFormat(self, tweetsList, indents, sortKeys):
		for tweet in tweetsList:
			print(json.dumps(tweet, indent = indents, sort_keys = sortKeys))
			print("\r\n")

	"""
	parameters:
		tweetsList(list) = list of tweets in json format;
		folderPath(string) = folder where to save the tweets file into;
	"""
	def saveTweetsInJsonFormatToFile(self, tweetsList, folderPath):
		if(len(tweetsList) == 0):
			print("Tweets list is empty!")
			return
		minTimestamp = int(time.mktime(parse(tweetsList[0]["created_at"]).timetuple()))
		maxTimestamp = int(time.mktime(parse(tweetsList[0]["created_at"]).timetuple()))
		tweetCounter=0
		for tweet in tweetsList:
			tweetCounter = tweetCounter + 1
			tweetCreatedAt = int(time.mktime(parse(tweet["created_at"]).timetuple()))
			if(tweetCreatedAt > maxTimestamp):
				maxTimestamp = tweetCreatedAt
			if(tweetCreatedAt < minTimestamp):
				minTimestamp = tweetCreatedAt
		try:
			readableMinTime=str(datetime.datetime.fromtimestamp(minTimestamp).replace(tzinfo=timezone('UTC')).strftime("%d-%m-%Y_%H:%M:%S_%z"))
			readableMaxTime=str(datetime.datetime.fromtimestamp(maxTimestamp).replace(tzinfo=timezone('UTC')).strftime("%d-%m-%Y_%H:%M:%S_%z"))
			fileName = "From:" + readableMinTime + "_To:"+ readableMaxTime + "_Ammount:" + str(tweetCounter)
			totalFilePath = folderPath + "/" + fileName
			with open(totalFilePath, "w") as outFile:
				json.dump(tweetsList, outFile)
			print("File saved to " + totalFilePath)
		except:
			print("An error occured while trying to save the file!")
			return


#Example of class and functions usage
"""
ta = TweetAnalyzer()
tweetsList = ta.getTweetsWithinTimeSpan("28/3/2018 13:59:00 +0000", "28/3/2018 14:00:00 +0000", "tweets/#cryptocurrency")
ta.printTweetsInJsonFormat(tweetsList, 2, True)
ta.saveTweetsInJsonFormatToFile(tweetsList, "tweets/timestamped")
"""