import tweepy
from tweepy import OAuthHandler
import sys
import jsonpickle
import os
 
access_token = '99273089-o5InyP9iT8g4RFIVYqZzl8jN5ghB8QtwqbJy2QCcz'
access_secret = 'pA7qZPiWLFCYlq1IlWt4QeySXxlsnZVkxEYArafarGLiQ'
API_KEY = 'j00jpHtExdR8Xq6S1XRB41BNq'
API_SECRET = 'T85doZBj26Qzqd80rhpZyBlTc3kXA7iK9VWIxEI0UWOtF0ie6q'
 
auth = OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(access_token, access_secret)
# auth = OAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
	print ("Can't Authenticate")
	sys.exit(-1)



searchQuery = '#Slovenia'
maxTweets = 10000000
tweetsPerQry = 100
fName = 'tweets.txt'


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
	while tweetCount < maxTweets:
		try:
			if (max_id <= 0):
				if (not sinceId):
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
				else:
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since_id=sinceId)
			else:
				if (not sinceId):
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1))
				else:
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1), since_id=sinceId)
			if not new_tweets:
				print("No more tweets found")
				break
			for tweet in new_tweets:
				f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
			tweetCount += len(new_tweets)
			print("Downloaded {0} tweets".format(tweetCount))
			max_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			print("some error : " + str(e))
			break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))