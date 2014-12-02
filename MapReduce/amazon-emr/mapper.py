#!/usr/bin/python
import sys, re

def main(argv):
	for line in sys.stdin:
		line = line.strip()
	    #pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
		#pattern = re.compile("\w+")
		for word in pattern.findall(line):
			line.replace(',', " ")
			#words = line.split()
			print(word.lower() + "\t" + "1")

if __name__ == "__main__":
	main(sys.argv)

