#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import re
from dateutil.parser import parse
import bisect
import progressbar
import numpy as np
# from io import StringIO
import matplotlib.pyplot as plt
from datetime import datetime
import time
import math


class countAndClassify():
	tweetsFolder = "tweets/cryptocurrency"

	def __init__(self, regexes, names):
		self.categoryRegexes = regexes
		self.categoryNames = names

		self.bins = self.genBinsFromTweets(self.tweetsFolder, 100)
		self.nekaj = self.bins
		

	def genBinsFromTweets(self, folder, nmOfBins):
		newestFile = open(folder + "/" + sorted(os.listdir(folder))[-1])
		oldestFile = open(folder + "/" + sorted(os.listdir(folder))[0])

		self.newestTimeStamp = json.loads(newestFile.readline())["created_at"]

		for line in oldestFile:
			self.oldestTimeStamp = line

		self.oldestTimeStamp = json.loads(self.oldestTimeStamp)["created_at"]

		self.newestTimeStamp = 1525910400
		self.oldestTimeStamp = 1524528000

		# print(self.oldestTimeStamp)
		# print(self.newestTimeStamp)

		bins = [0] * nmOfBins
		step = (self.newestTimeStamp - self.oldestTimeStamp) / (nmOfBins - 1)

		bins[0] = self.oldestTimeStamp
		for i in xrange(1, nmOfBins):
			bins[i] = bins[i - 1] + step

		return bins

	def mojBisect(self, lisst, num):
		i = bisect.bisect(lisst, num)
		if i != len(lisst):
			if abs(lisst[i] - num) < abs(lisst[i - 1] - num):
				return i
			else:
				return i - 1
		else:
			return i - 1

	def calculate(self):
		bar = progressbar.ProgressBar(maxval = 20000*76, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

		self.binsForCoins = []
		self.binsForCoins = [[0 for x in range(len(self.bins))] for y in range(len(self.categoryNames))] 

		# self.maxTimeStamp

		bar.start()
		lineCounter = 0

		for tweetFileName in os.listdir(self.tweetsFolder):
			tweetFile = open(self.tweetsFolder + "/" + tweetFileName)

			for line in tweetFile:
				lineCounter += 1

				tweetJson = json.loads(line)
				tweetText = tweetJson["text"]

				maxMatches = 0
				maxMatchesIndex = -1
				count = 0

				for regex in self.categoryRegexes:
					matches = re.findall(regex, tweetText)

					if len(matches) > maxMatches:
						maxMatches = len(matches)
						maxMatchesIndex = count

					count += 1

				if maxMatchesIndex != -1:
					timestamp = tweetJson["created_at"]
					timestamp = int(time.mktime(parse(timestamp).timetuple()))

					if timestamp >= self.oldestTimeStamp and timestamp <= self.newestTimeStamp:
						indexOfBin = self.mojBisect(self.bins, timestamp)
						self.binsForCoins[maxMatchesIndex][indexOfBin] += 1
					
				bar.update(lineCounter)

				
		bar.finish()	

		# print(self.binsForCoins)
		# print(test)

	def resultsToFile(self, file):
		f = open(file, 'w+')
		results = {}
		count = 0

		for name in self.categoryNames:
			results[name] = self.binsForCoins[count]
			count += 1

		s = json.dumps(results)
			
		f.write(s)

	def readFromFile(self, file):
		f = open(file, 'r')
		text = f.read()
		self.results = json.loads(text)
		# print(self.results)

	def draw(self, coin):
		
		fig = plt.figure(figsize = (14, 9))
		subplt = plt.subplot(1, 1, 1)

		times = []
		for time in self.nekaj:
			times.append(datetime.fromtimestamp(float(time)).strftime('%d-%m'))
			
		# print(times)

		step = int(math.ceil(100 / 17.0))
		print(step)
		index = 0

		nekaj = []
		for i in range(0, 18):
			# print(index)
			if index > 100:
				index = 99
			nekaj.append(times[index])
			index += step

		print(nekaj)
			

		subplt.plot(self.results[coin], linewidth=2)
		# print(len(self.results[coin]))

		plt.xticks(np.arange(0, 100, step=step), nekaj)
		plt.xlabel("Cas v dnevih", fontsize = 16)
		plt.ylabel("Stevilo pojavitev", fontsize = 16)
		# plt.rcParams.update({'font.size': 20})

		ax = plt.gca()
		ax.tick_params(axis = 'both', which = 'major', labelsize = 11)
		ax.tick_params(axis = 'both', which = 'minor', labelsize = 11)
		# subplt.bar(np.arange(len(self.results[coin])), self.results[coin])

		plt.show()

	def printInterval(self):
		print("From: " + str(self.oldestTimeStamp))
		print("To: " + str(self.newestTimeStamp))


categoryRegexes = ["Bitcoin|bitcoin|BITCOIN|btc|BTC|bitc|BITC", "ethereum|ETHEREUM|Ether|ether|ETH|eth", "Ripple|ripple|XRP|xrp"]
categoryNames = ["Bitcoin", "Ethereum", "Ripple"]
yes = countAndClassify(categoryRegexes, categoryNames)
# yes.calculate()
# yes.resultsToFile("results")
# yes.genBinsFromTweets("tweeets/cryptocurrency", 100)
yes.readFromFile("results")
yes.draw("Ethereum")
yes.printInterval()