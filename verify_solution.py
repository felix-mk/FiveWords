def main():
	lines = open('results.txt', 'r').read().splitlines()
	words = set(open('en_words.txt', 'r').read().splitlines())

	for line in lines:
		line = line.replace(' ', '')

		# Each line contains five words of five characters each.
		assert len(line) == 5 * 5

		# Each character that appears occurs only once in all words.
		assert len(set(line)) == 5 * 5

		w1 = line[0:5]
		w2 = line[5:10]
		w3 = line[10:15]
		w4 = line[15:20]
		w5 = line[20:25]

		# All words are in the database.
		assert w1 in words
		assert w2 in words
		assert w3 in words
		assert w4 in words
		assert w5 in words

	print('Valid result.')

if __name__ == '__main__':
	main()
