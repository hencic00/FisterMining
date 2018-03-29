from aylienapiclient import textapi
import json
import time

client = textapi.Client("1c5d67bf", "434a38920d4582583ff7572828c077e2")

f = open("tweets/#cryptocurrency/978832770200887296_978716768754683913_20000", "r")

neutral = 0
negative = 0
positive = 0

for x in xrange(1, 11):
	line = f.readline()
	tweet = json.loads(line)

	sentiment = client.Sentiment({'text': tweet["text"].encode('utf-8')})

	print(sentiment["polarity"])
	if sentiment["polarity"] == "neutral":
		neutral += 1;
	elif sentiment["polarity"] == "positive":
		positive += 1;
	elif sentiment["polarity"] == "negative":
		negative += 1;


print("neutral: " + str(neutral))
print("negative: " + str(negative))
print("positive: " + str(positive))