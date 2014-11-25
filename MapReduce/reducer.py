#!/usr/bin/python
import sys, re

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
			result = [last_word, word_count]
			#prints "word\t#occurs"
			print("\t".join(str(v) for v in result))
			#our "new" word
			last_word = word
			word_count = 1


if __name__ == "__main__":
	main(sys.argv)

