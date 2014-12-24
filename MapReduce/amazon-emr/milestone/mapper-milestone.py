#!/usr/bin/python
import json, sys, re
'''
data = []
with open('sample.bin') as f:
    for line in f:
        data.append(json.loads(line))
'''

def processTweet(mytweet):
	pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*") 
	#pattern = re.compile("[\w@#]+") 
	for word in pattern.findall(mytweet): 
		if len(word) >= 2:
			print "LongValueSum:" + word.lower() + "\t" + "1" 


def getTweets():
	tweet = []
	for line in sys.stdin:
		tweet.insert(0, (json.loads(line)))
		#print(tweet[0]["text"] + "\n")
		myteet = tweet[0]["text"]
		processTweet(myteet)
	
if __name__ == '__main__':
	getTweets()


