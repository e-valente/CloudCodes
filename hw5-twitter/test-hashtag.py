def parsePost(msg):
	wordlist = msg.split()
	result = []
	for word in wordlist:
		if word.startswith("#"):
			result.append(word)


	return result

				

