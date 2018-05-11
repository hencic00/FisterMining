#!/usr/bin/python

import time
import http.client
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import json

def getPrices(forCryptoCurrency, inCurrencies, fromHere, toHere, nmOfPoints):
	currentTimeStamp = fromHere
	jump = int((toHere - fromHere) / (nmOfPoints - 1))
	prices = [0] * nmOfPoints

	connection = http.client.HTTPSConnection("min-api.cryptocompare.com")
	urlPattern = "/data/pricehistorical?fsym={0}&tsyms={1}&ts={2}"

	counter = 0

	second = 0
	minute = 0
	hour = 0

	timeStart = time.time()
	timeEnd = time.time()

	requestLimitPerSecond = 15
	requestLimitPerMinute = 300
	requestLimitPerHour = 8000

	numberOfRequestsPerSecond = 0
	numberOfRequestsPerMinute = 0
	numberOfRequestsPerHour = 0
	
	i = 0

	while True:

		if numberOfRequestsPerSecond == requestLimitPerSecond:
			if second > 0 and second < 1:
				time.sleep(1 - second + 1.3)

			second = 0
			numberOfRequestsPerSecond = 0
			timeStart = time.time()

		if requestLimitPerMinute == numberOfRequestsPerMinute:
			if minute > 0 and minute < 60:
				time.sleep(60 - minute + 0.3)
			
			second = 0
			minute = 0
			numberOfRequestsPerSecond = 0
			numberOfRequestsPerMinute = 0
			timeStart = time.time()

		if requestLimitPerHour == numberOfRequestsPerHour:
			if hour > 0 and hour < 3600:
				time.sleep(3600 - hour + 0.3)

			second = 0
			minute = 0
			hour = 0
			numberOfRequestsPerSecond = 0
			numberOfRequestsPerMinute = 0
			numberOfRequestsPerHour = 0
			timeStart = time.time()
		
		request = urlPattern.format(forCryptoCurrency, inCurrencies, currentTimeStamp)

		timeEnd = time.time()
		second += (timeEnd - timeStart)
		minute += (timeEnd - timeStart)
		hour += (timeEnd - timeStart)

		connection.request("GET", request)
		response = connection.getresponse()

		timeStart = time.time()

		# print(response.read())
		# print(numberOfRequestsPerSecond)
		print(i)

		numberOfRequestsPerSecond += 1
		numberOfRequestsPerMinute += 1
		numberOfRequestsPerHour += 1
		prices[i] = json.loads(response.read())

		currentTimeStamp += jump
		i += 1
		
			
		if i == nmOfPoints:
			return prices




	


# startDate = "1/10/17 16:31:32"
# endDate = "1/04/18 16:31:32"

# startTimeStamp = int(time.mktime(datetime.strptime(startDate, '%d/%m/%y %H:%M:%S').timetuple()))
# endTimeStamp = int(time.mktime(datetime.strptime(endDate, '%d/%m/%y %H:%M:%S').timetuple()))

prices = getPrices("BTC", "USD,EUR", 1524418928, 1525425375, 12)

prices1 = []
for price in prices:
	prices1.append(price["BTC"]["USD"])
	# print(price)

fig = plt.figure(figsize = (9, 9))
subplt = plt.subplot(1, 1, 1)
subplt.bar(np.arange(len(prices1)), np.array(prices1))

priceDifferences = []
for i in range(1, 11):
	priceDifferences.append(int(abs(prices1[i] - prices1[i - 1])))
	# print(i - 1)
print(priceDifferences)

fig = plt.figure(figsize = (9, 9))
subplt = plt.subplot(1, 1, 1)
subplt.bar(np.arange(len(priceDifferences)), np.array(priceDifferences))

plt.show()
