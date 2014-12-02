#!/usr/bin/python


import sys, re
import collections

def main(argv):

	last_word = None
	word_count = 0

	
	for line in sys.stdin:
		line = line.strip()

		word, count = line.split("\t")

		count = int(count)

		#first time iteration
		if not last_word:
			last_word = word

		#just count
		if word == last_word:
			word_count += count

		#different word	
		else:
			final_result[last_word] = word_count
			#result_to_print = [last_word, word_count]
			#prints "word\t#occurs"
			print("\t".join(str(v) for v in result_to_print))
			#our "new" word
			last_word = word
 			word_count = 1

   

if __name__ == "__main__":
	main(sys.argv)

