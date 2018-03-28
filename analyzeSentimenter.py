from aylienapiclient import textapi

client = textapi.Client("1c5d67bf", "434a38920d4582583ff7572828c077e2")
sentiment = client.Sentiment({'text': 'enter some of your own text here'})
print(sentiment)