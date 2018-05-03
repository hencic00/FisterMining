import nltk
#from nltk.sentiment import SentimentAnalyzer
#from nltk.sentiment.util import *
#from nltk.classify import NaiveBayesClassifier
#from nltk.corpus import subjectivity
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

class SentimentAnalyse:
	downloadLexiconFlag=False		
		
	def downloadLexicon(self):
		nltk.download('vader_lexicon')

	def analyse(self, text):
		sentences=self.splitText(text)
		compoundSum=0
		counter=0
		positive=0
		negative=0
		neutral=0
		sid=SentimentIntensityAnalyzer()
		for sentence in sentences:
			#print('\r\n'+sentence)
			ss=sid.polarity_scores(sentence)
			if(ss["compound"]<0):
				negative+=1
			elif(ss["compound"]==0):
				neutral+=1
			elif(ss["compound"]>0):
				positive+=1
			#for k in sorted(ss):
			#	print('{0}: {1}, '.format(k, ss[k]))
			compoundSum+=ss["compound"]
			counter+=1
		return [positive, neutral, negative,(compoundSum/counter)]

	def splitText(self, text):
		sentences=[]
		sentence=""
		for c in text:
			sentence+=c
			if(c=='.' or c=='!' or c=='?'):				
				sentences.append(sentence)
				sentence=""
		return sentences

#if __name__ == '__main__':
#    testText="This is a test text! I hope it works. If it doesn't work im gonna be sad."
#    sent=SentimentAnalyse()
#    if(sent.downloadLexiconFlag==True):
#    	sent.downloadLexicon()
#    analysedText=sent.analyse(testText)
#    print("Positive: "+str(analysedText[0])+", Neutral: "+str(analysedText[1])+", Negative: "+str(analysedText[2])+", Text Compound Average: "+str(analysedText[3]))