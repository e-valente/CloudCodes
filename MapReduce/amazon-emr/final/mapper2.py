#!/usr/bin/python
import sys, re
import collections

def main(argv):

	last_word = None
	word_count = 0
	NTH = 10
	#we don't want uncommon words
	cutoff = 1

	result_words = {}
	result_hashtags = {}
	result_users = {}

	for line in sys.stdin:
		line = line.strip()

		word, count = line.split("\t")

		count = int(count)

		if(count > cutoff):
			if word.startswith("#"):
				result_hashtags[word] = count
			elif word.startswith("@"):
				result_users[word] = count	
			else:
				result_words[word] = count	
	
 	#words
 	mylist = sorted(result_words, key=result_words.__getitem__, reverse=True)
 	if len(result_words) >= NTH :
 		for i in range(NTH):
 			print("%s\t%s" % (mylist[i], result_words[mylist[i]]))
 	else:
 		for i in range(len(result_words)):
 			print("%s\t%s" % (mylist[i], result_words[mylist[i]]))
 			

 	#users	
 	mylist = sorted(result_users, key=result_users.__getitem__, reverse=True)
 	if len(result_users) >= NTH:
 		for i in range(NTH):
 			print("%s\t%s" % (mylist[i], result_users[mylist[i]]))		
 	else:
 		for i in range(len(result_users)):
 			print("%s\t%s" % (mylist[i], result_users[mylist[i]]))	


 	#hashtags	
 	mylist = sorted(result_hashtags, key=result_hashtags.__getitem__, reverse=True)
 	if len(result_hashtags) >= NTH:
 		for i in range(NTH):
 			print("%s\t%s" % (mylist[i], result_hashtags[mylist[i]]))
 	else:
 		for i in range(len(result_hashtags)):
 			print("%s\t%s" % (mylist[i], result_hashtags[mylist[i]]))	
 			
 	

if __name__ == "__main__":
	main(sys.argv)

