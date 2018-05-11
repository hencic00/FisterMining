import os
import json
import jsonpickle

minId = 991984776600055808
fileSize = 20000

tweets = []

for filename in sorted(os.listdir('tweets/cryptocurrency1/')):
	# print(filename)
	with open("tweets/cryptocurrency1/" + filename) as f:

		lines = f.readlines()
		lines.reverse()

		for line in lines:
			tweet = json.loads(line)
			if tweet["id"] > minId:
				tweets.insert(0, tweet)
				
			print(len(tweets))
			if len(tweets) == 20000:
				fileName = "tweets/cryptocurrency/" + str(tweets[0]["id"]) + "_" + str(tweets[-1]["id"]) + "_20000"
				f = open(fileName, 'w')

				for tweet in tweets:
					f.write(jsonpickle.encode(tweet, unpicklable=False) + '\n')

				f.close()
				tweets = []




