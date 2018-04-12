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
	"../tweets/#cryptocurrency/978651024561852416_978585540646797314_20000",
	"../tweets/#cryptocurrency/978717001106448384_978650948942880769_20000",
	"../tweets/#cryptocurrency/978832770200887296_978716768754683913_20000",
	"../tweets/#cryptocurrency/978925585312333824_978832119832170497_20000",
	"../tweets/#cryptocurrency/978993358700818432_978925407549485057_20000",
	"../tweets/#cryptocurrency/979053718241918976_978993246129946624_20000"
]

tokenDictionary = {}
for fileName in fileNames:
	if os.path.isfile(fileName):
		with open(fileName, "r") as f:
			bar = progressbar.ProgressBar(maxval = 20000, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
			bar.start()
			pattern = re.compile("^[A-Za-z0-9]*$")

			lineNumber = 0

			for line in f:
				lineNumber = lineNumber + 1
				bar.update(lineNumber)

				tweet = json.loads(line)

				# tokenList = tknzr.word_tokenize(sentence)(tweet["text"])
				tokenList = nltk.word_tokenize(tweet["text"])
				
				for token in tokenList:
					if pattern.match(token):
						if token in tokenDictionary:
							tokenDictionary[token] = tokenDictionary[token] + 1
						else:
							tokenDictionary[token] = 1

			bar.finish()
	else:
		print("File does not exist")

with open('tokens.json', 'w+') as file:
	file.write(json.dumps(sorted(tokenDictionary.items(), key=operator.itemgetter(1))))
