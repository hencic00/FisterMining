from nltk.tokenize import TweetTokenizer
import nltk
import os.path
import json
import progressbar
import operator
import re

tknzr = TweetTokenizer()

# fileName = "../tweets/#cryptocurrency/978832770200887296_978716768754683913_20000"

fileNames = [
	"../tweets/#cryptocurrency/978585730359296000_978505978659315712_20000",
	"../tweets/#cryptocurrency/978651024561852416_978585540646797314_20000"
]


categories = ["Bitcoin|bitcoin|BITCOIN|btc|BTC|bitc|BITC", "ethereum|ETHEREUM|Ether|ether|ETH|eth", "Ripple|ripple|XRP|xrp"]
categorieNames = ["Bitcoin", "Ethereum", "Ripple", "Bitcoin_Cash"]
categoryTweets = ["", "", "", ""]
# compiledCategories = []

# for category in categories:
# 	compiledCategoried.append(re.compile(category))

for fileName in fileNames:
	if os.path.isfile(fileName):
		with open(fileName, "r") as f:
			bar = progressbar.ProgressBar(maxval = 20000, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
			bar.start()

			lineNumber = 0

			for line in f:
				lineNumber = lineNumber + 1
				bar.update(lineNumber)

				tweet = json.loads(line)
				
				count = 0
				maxMatches = 0
				categoryIndex = 0
				found = False

				for category in categories:
					matches = re.findall(category, tweet["text"])
					if len(matches) > maxMatches:
						maxMatches = len(matches)
						categoryIndex = count
						found = True
					count += 1

				if found:
					categoryTweets[categoryIndex] += line;

				found = False
				

			bar.finish()
	else:
		print("File does not exist")

# with open('tokens.json', 'w+') as file:
# 	file.write(json.dumps(sorted(tokenDictionary.ites(), key=operator.itemgetter(1))))

counter = 0
for fileName in categorieNames:
	with open(fileName, 'w+') as file:
		file.write(categoryTweets[counter])
	counter += 1
