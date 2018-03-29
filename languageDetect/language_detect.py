from langdetect import detect
from iso639_1_Dictionary import *  
import json
import progressbar
import os.path
import sys

fileName = "../tweets/#cryptocurrency/978832770200887296_978716768754683913_20000"
languageCounter = {}

if os.path.isfile(fileName):
	print("Detecting language for tweets. Please hold!")
	with open(fileName, "r") as f:
		bar = progressbar.ProgressBar(maxval = 20000, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

		bar.start()
		lineNumber = 0

		for line in f:
			lineNumber = lineNumber + 1
			bar.update(lineNumber)

			tweet = json.loads(line)
			detectedLang = detect(tweet["text"])
			
			if detectedLang in languageCounter:
				languageCounter[detectedLang] = languageCounter[detectedLang] + 1
			else:
				languageCounter[detectedLang] = 1

		bar.finish()
else:
	print("File does not exist")

for detectedLang in languageCounter:
	detectedLangFull = iso_639_Dictionary[detectedLang]
	print detectedLangFull, languageCounter[detectedLang]