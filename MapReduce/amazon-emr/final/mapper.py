#!/usr/bin/python
import json, sys, re


def processTweet(mytweet):
	pattern = re.compile("[a-zA-Z0-9@_#-][a-zA-Z0-9@_#-]+") 
	#pattern = re.compile("[\w@#]+") 
	for word in pattern.findall(mytweet): 
		#line.replace(',', " ")
		#words = line.split()
		if(len(word) >= 2):
			print(word.lower() + "\t" + "1")
			#print "LongValueSum:" + word.lower() + "\t" + "1" 


def getTweets():
	#tweet = []
	for line in sys.stdin:
		#tweet.insert(0, (json.loads(line)))
		tweet = json.loads(line)
		#print(tweet[0]["text"] + "\n")
		myteet = tweet["text"]
		processTweet(myteet)
	
if __name__ == '__main__':
	getTweets()


