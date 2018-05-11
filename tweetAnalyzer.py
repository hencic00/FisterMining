import os
import json
import time
import datetime
import math
import progressbar
from multiprocessing import Process, Manager
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
	implementation of above function for searching large ammounts of tweets and simultanious saving to avoid RAM cap
	parameters: 
		startTime(string) = save tweets that are posted after this time;
		endTime(string) = save tweets that are posted before this time;
		folderPath(string) = folder where the tweet files are saved in JSON format, 20000 tweets per file;
		saveFolderPath(string) = folder where to save tweet files
		limitToSave(int) = ammount of tweets to save per file
	"""
	def getTweetsWithinTimeSpanAndSave(self, startTime, endTime, folderPath, saveFolderPath, limitToSave):
		start_time=time.time()
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
							if(len(validTweets) == limitToSave):
								self.saveTweetsInJsonFormatToFile(validTweets, saveFolderPath)
								validTweets = []
						bar.update(lineNumber)
			if(len(validTweets) != 0):
				self.saveTweetsInJsonFormatToFile(validTweets, saveFolderPath)
			bar.finish()
		except:
			print("An error occured! Check the datetime input format 'day/month/year hour:minute:second timezone' example: '28/3/2018 13:00:00 +0000'")
			return
		print("Multiprocessed time " + str(time.time() - start_time))

	"""
	implementation of above function for multiprocessing purposes
	parameters:
		startTime(string) = save tweets that are posted after this time;
		endTime(string) = save tweets that are posted before this time;
		filePaths (list of strings) = list of file paths from where to read tweets; 20000 tweets per file
		saveFolderPath(string) = folder where to save tweet files
		limitToSave(int) = ammount of tweets to save per file
	"""
	def getTweetsWithinTimeSpanAndSave2(self, startTime, endTime, filePaths, saveFolderPath, limitToSave):
		validTweets = []
		#lineNumber = 0
		try:
			fromTimestamp = int(time.mktime(parse(startTime).timetuple()))
			toTimestamp = int(time.mktime(parse(endTime).timetuple()))
			fileCount = len(filePaths)
			#bar = progressbar.ProgressBar(maxval = fileCount * 20000, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
			#bar.start()
			for filename in filePaths:
				with open(filename) as file:
					for line in file:
						#lineNumber = lineNumber + 1					
						jsonData = json.loads(line)
						createdAt = jsonData["created_at"]
						dt = parse(createdAt)
						timestamp = int(time.mktime(dt.timetuple()))
						if(timestamp >= fromTimestamp and timestamp <= toTimestamp):
							validTweets.append(jsonData)
							if(len(validTweets) == limitToSave):
								self.saveTweetsInJsonFormatToFile(validTweets, saveFolderPath)
								validTweets = []
						#bar.update(lineNumber)
			if(len(validTweets) != 0):
				self.saveTweetsInJsonFormatToFile(validTweets, saveFolderPath)
			#bar.finish()
			return True
		except:
			print("An error occured! Check the datetime input format 'day/month/year hour:minute:second timezone' example: '28/3/2018 13:00:00 +0000'")
			return False

	"""
	parameters:
		startTime(string) = save tweets that are posted after this time;
		endTime(string) = save tweets that are posted before this time;
		filePaths (list of strings) = list of file paths from where to read tweets; 20000 tweets per file
		saveFolderPath(string) = folder where to save tweet files
		limitToSave(int) = ammount of tweets to save per file
		numberOfProcesses(int) = ammount of processes to spawn
	"""		
	def getTweetsMultiprocessed(self, startTime, endTime, folderPath, saveFolderPath, limitToSave, numberOfProcesses):
		start_time=time.time()
		if not os.path.exists(saveFolderPath):
			os.makedirs(saveFolderPath)
		validTweets = []
		fileList = os.listdir(folderPath)
		if(len(fileList) == 0):
			print("Folder " + filderPath + " empty!")
			return
		filesPerProcess = math.ceil(len(fileList) / float(numberOfProcesses))
		processFileLists = []
		tmpList = []
		counter=0
		for j in range(0, len(fileList)):
			tmpList.append(folderPath + "/" + fileList[j])
			counter = counter + 1
			if(counter >= filesPerProcess or j == len(fileList) - 1):
				processFileLists.append(tmpList)
				tmpList = []
				counter = 0
		processesList=[]
		for i in range(0, numberOfProcesses):
			if(i >= len(processFileLists)):
				break
			processesList.append(Process(target = self.getTweetsWithinTimeSpanAndSave3, args = (startTime, endTime, processFileLists[i], saveFolderPath, limitToSave,)))
			#print("Spawning process " + str(i) + " with " + str(processFileLists[i]))
			processesList[i].start()
			
		for k in range(0, len(processesList)):
			processesList[k].join()
		#print("Multiprocessed time " + str(time.time() - start_time))

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
		if not os.path.exists(folderPath):
			os.makedirs(folderPath)
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
		#try:
		readableMinTime=str(datetime.datetime.fromtimestamp(minTimestamp).replace(tzinfo=timezone('CET')).strftime("%d-%m-%Y_%H-%M-%S_%z"))
		readableMaxTime=str(datetime.datetime.fromtimestamp(maxTimestamp).replace(tzinfo=timezone('CET')).strftime("%d-%m-%Y_%H-%M-%S_%z"))
		fileName = readableMinTime + "_"+ readableMaxTime + "_" + str(tweetCounter)
		totalFilePath = folderPath + "/" + fileName
		with open(totalFilePath, 'w') as outFile:
			json.dump(tweetsList, outFile)
		#print(totalFilePath + " saved!")
		#except:
		#	print("An error occured while trying to save the file!")
		#	return

	def ReadAnalyzedData(self,filename):
	    with open(filename) as json_data:
	        data = json.load(json_data)

	    data = json.loads(data)
	    return data

	def getTweetsWithinTimeSpanAndSave3(self, startTime, endTime, filePaths, saveFolderPath, limitToSave):
			validTweets = []
			#lineNumber = 0
			#try:
			fromTimestamp = int(time.mktime(parse(startTime).timetuple()))
			toTimestamp = int(time.mktime(parse(endTime).timetuple()))
			fileCount = len(filePaths)
			#bar = progressbar.ProgressBar(maxval = fileCount * 20000, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
			#bar.start()
			for filename in filePaths:
				data=self.ReadAnalyzedData(filename)
				for tweetEncoded in data:
					jsonData=json.loads(tweetEncoded)
					#lineNumber = lineNumber + 1					
					createdAt = jsonData["created_at"]
					dt = parse(createdAt)
					timestamp = int(time.mktime(dt.timetuple()))
					if(timestamp >= fromTimestamp and timestamp <= toTimestamp):
						validTweets.append(jsonData)
						if(len(validTweets) == limitToSave):
							self.saveTweetsInJsonFormatToFile(validTweets, saveFolderPath)
							validTweets = []
					#bar.update(lineNumber)
			if(len(validTweets) != 0):
				self.saveTweetsInJsonFormatToFile(validTweets, saveFolderPath)
			#bar.finish()
			return True
			#except:
			#	print("An error occured! Check the datetime input format 'day/month/year hour:minute:second timezone' example: '28/3/2018 13:00:00 +0000'")
			#	return False

#Example of class and functions usage

#ta = TweetAnalyzer()
#ta.getTweetsMultiprocessed("28/3/2018 13:59:00 +0000", "28/3/2018 14:00:00 +0000", "tweets/#cryptocurrency", "tweets/timestamped/testRun1", 5000, 4)
#ta.getTweetsWithinTimeSpanAndSave("28/3/2018 13:59:00 +0000", "28/3/2018 14:00:00 +0000", "tweets/#cryptocurrency", "tweets/timestamped/testRun2", 5000)
#tweetsList = ta.getTweetsWithinTimeSpan("28/1/2018 13:59:00 +0000", "28/4/2018 14:00:00 +0000", "tweets/#cryptocurrency")
#ta.printTweetsInJsonFormat(tweetsList, 2, True)
#ta.saveTweetsInJsonFormatToFile(tweetsList, "tweets/timestamped")
