from os import path
from wordcloud import WordCloud
import json
import pickle
import matplotlib.pyplot as plt
import time

def load_obj(name):
    with open('../dictionaries/'+ name + '.pkl', 'rb') as f:
        return pickle.load(f)

def generateWordCloud(wordCountFP, dictionaryFP, limit, generateImage):
	data=json.load(open(wordCountFP))
	dictionary=load_obj(dictionaryFP)
	occurances=[]
	text=""
	for entry in data:
		#for c in dictionary:
			#if(entry[0].lower()==c.lower() and entry[1]>=limit):
			if entry[0] in dictionary:
				for i in range(0, entry[1]):
					text = text + " " + entry[0].lower()
				occurances.append(entry)		

	#save text to file
	with open("files/occurancesText.txt", "w") as text_file:
		text_file.write(text)

	#generate WordCloud image
	if(generateImage):
		wordcloud = WordCloud(max_font_size=40).generate(text)
		plt.figure()
		plt.imshow(wordcloud, interpolation="bilinear")
		plt.axis("off")
		plt.savefig("wordCloud"+str(time.time())+".png", dpi=100)
		plt.show()
		

#generateWordCloud("files/tokens.json", "cryptos", 500, False)
