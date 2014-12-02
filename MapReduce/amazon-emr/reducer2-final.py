#!/usr/bin/python
import sys, re
import collections

def main(argv):

	result_words = {}
	result_hashtags = {}
	result_users = {}

	for line in sys.stdin:
		line = line.strip()

		word, count = line.split("\t")

		count = int(count)

		#hashtags
		if word.startswith("#"):
			if result_hashtags.get(word, 0) == 0:
				result_hashtags[word] = count
			else:
				result_hashtags[word] += count 				

		#users		
		elif word.startswith("@"):
			if result_users.get(word, 0) == 0:
				result_users[word] = count	
			else:
				result_users[word] += count		
		
		#common words
		else:
			if result_words.get(word, 0) == 0:
				result_words[word] = count
			else:
				result_words[word] += count	
		
		

 	#print("\n---- Result ----\n")
 	#words
 	mylist = sorted(result_words, key=result_words.__getitem__, reverse=True)
 	for i in range(5):
 		print("%s\t%s" % (mylist[i], result_words[mylist[i]]))

 	#hashtags	
 	mylist = sorted(result_hashtags, key=result_hashtags.__getitem__, reverse=True)
 	for i in range(5):
 		print("%s\t%s" % (mylist[i], result_hashtags[mylist[i]]))

 	#users	
 	mylist = sorted(result_users, key=result_users.__getitem__, reverse=True)
 	for i in range(5):
 		print("%s\t%s" % (mylist[i], result_users[mylist[i]]))		
 		
 				
 		
 		
 	

if __name__ == "__main__":
	main(sys.argv)

