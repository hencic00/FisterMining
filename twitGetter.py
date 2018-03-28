import tweepy
from tweepy import OAuthHandler, AppAuthHandler
import sys
import jsonpickle
import os
 
access_token = '99273089-o5InyP9iT8g4RFIVYqZzl8jN5ghB8QtwqbJy2QCcz'
access_secret = 'pA7qZPiWLFCYlq1IlWt4QeySXxlsnZVkxEYArafarGLiQ'
API_KEY = 'j00jpHtExdR8Xq6S1XRB41BNq'
API_SECRET = 'T85doZBj26Qzqd80rhpZyBlTc3kXA7iK9VWIxEI0UWOtF0ie6q'
 
# auth = OAuthHandler(API_KEY, API_SECRET) # App aut => 180 zahtev na 15 minut in 100 tweetov na zahtevo.
# auth.set_access_token(access_token, access_secret) # Skupaj 18000 tweetov na 15 minut.
auth = AppAuthHandler(API_KEY, API_SECRET) # Account auth => 450 zahtev na 15 minut in 100 tweetov na zahtevo. Skupaj 45000 tweetov na 15 minut.
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

if (not api):
	print ("Can't Authenticate")
	sys.exit(-1)


searchQuery = '#cryptocurrency'
destinationFolder = "tweets/" + searchQuery
maxTweets = 10000000
maxTweetsPerFile = 20000
tweetsPerQry = 100

if not os.path.exists(destinationFolder):
	os.makedirs(destinationFolder)

tweetCount = 0
tweetCountPerFile = 0
tweets = []

since_id = None
max_id = None

while True:
	while len(tweets) < maxTweetsPerFile:
		if not max_id:
			tweets.extend(api.search(q=searchQuery, count=tweetsPerQry))
			max_id = tweets[-1].id - 1
		else:
			tweets.extend(api.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id)))
			max_id = tweets[-1].id - 1
		print(len(tweets))

	fileName = destinationFolder + "/" + str(tweets[0].id) + "_" + str(tweets[-1].id) + "_" + str(maxTweetsPerFile)
	f = open(fileName, 'w')
	
	
	for tweet in tweets[:maxTweetsPerFile]:
		f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')

	f.close()
	print ("Downloaded {0} tweets, Saved to {1}".format(maxTweetsPerFile, fileName))

	tweets = tweets[maxTweetsPerFile:]