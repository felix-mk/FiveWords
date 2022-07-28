import math, time
from datetime import timedelta

word_db = 'en_words.txt'
word_res_db = 'results.txt'

def read_words(filename):
	try:
		file = open(filename, 'r')
		return file.read().splitlines()
	except FileNotFoundError:
		print('The file {} does not exist.'.format(filename))
		exit(1)

def write_words(words, filename):
	file = open(filename, 'w')

	if 0 < len(words):
		file.write(words[0])
		for word in words[1:]:
			file.write('\n' + word)

def filter_duplicates(words):
	word_set = set()
	for word in words:
		if word not in word_set:
			word_set.add(word)

	return [word for word in word_set]

def filter_length_5(words):
	words_len_5 = []
	for word in words:
		if 5 == len(word):
			words_len_5.append(word)

	return words_len_5

def filter_duplicate_letters(words):
	words_no_duplicate_letters = []

	for word in words:
		char_set = set()
		no_duplicates = True

		for char in word:
			if char not in char_set:
				char_set.add(char)
			else:
				no_duplicates = False
				break

		if no_duplicates:
			words_no_duplicate_letters.append(word)

	return words_no_duplicate_letters

def filter_anagrams(words):
	anagram_table = {}

	for word in words:
		sorted_word = ''.join(sorted(word))
		if sorted_word in anagram_table:
			anagram_table[sorted_word].append(word)
		else:
			anagram_table[sorted_word] = [word]

	return [key for key in anagram_table], anagram_table

def is_valid_pair(word1, word2):
	char_set = set(word1)
	for char in word2:
		if char in char_set:
			return False

	return True

def valid_pairs(words):
	t0 = time.time()

	valid_pairs = []
	for word_idx1 in range(len(words)):
		if word_idx1 & 0xF == 0:
			t1 = time.time()

			num_total_words = 0.5 * (len(words) * (len(words) - 1))
			num_current_words = num_total_words - 0.5 * (len(words) - word_idx1) * (len(words) - word_idx1 - 1)
			num_current_words = num_current_words if 0 < num_current_words else 1

			time_delta = t1 - t0
			time_per_word = time_delta / num_current_words
			time_delta_seconds = math.floor(time_per_word * (num_total_words - num_current_words))
			time_to_go = timedelta(seconds=time_delta_seconds)

			if 0 == word_idx1:
				print('{:.2f}% [remaining time: ...]'.format((100.0 * num_current_words) / num_total_words), end=(20 * ' ' + '\r'))
			else:
				print('{:.2f}% [remaining time: {}]'.format((100.0 * num_current_words) / num_total_words, time_to_go), end=(20 * ' ' + '\r'))

		word1 = words[word_idx1]
		for word_idx2 in range(word_idx1 + 1, len(words)):
			word2 = words[word_idx2]

			if is_valid_pair(word1, word2):
				valid_pairs.append(word1 + word2)

	print(70 * ' ', end='\r')
	return valid_pairs

def valid_pairs2(words1, words2):
	valid_pairs = []
	for word1 in words1:
		for word2 in words2:
			if is_valid_pair(word1, word2):
				valid_pairs.append(word1 + word2)

	return valid_pairs

def split_word(word):
	return (word[:5], word[5:10], word[10:15], word[15:20], word[20:25])

def split_words(words):
	return [split_word(word) for word in words]

def substitute_anagrams(words, anagrams, pair_anagrams, pair_pair_anagrams):
	words_as_touple = split_words(words)

	pair_pair_word = []
	for word in words_as_touple:
		ac = pair_pair_anagrams[word[0] + word[1] + word[2] + word[3]]
		for a in ac:
			pair_pair_word.append(split_word(a + word[4]))

	word_word_pair_word = []
	for word in pair_pair_word:
		ac = pair_anagrams[word[0] + word[1]]
		for a in ac:
			word_word_pair_word.append(split_word(a + word[2] + word[3] + word[4]))

	word_word_word_word_word = []
	for word in word_word_pair_word:
		ac = pair_anagrams[word[2] + word[3]]
		for a in ac:
			word_word_word_word_word.append(split_word(word[0] + word[1] + a + word[4]))

	res = set()
	for word in word_word_word_word_word:
		ac = anagrams[word[0]]
		for a in ac:
			aac = anagrams[word[1]]
			for aa in aac:
				aaac = anagrams[word[2]]
				for aaa in aaac:
					aaaac = anagrams[word[3]]
					for aaaa in aaaac:
						aaaaac = anagrams[word[4]]
						for aaaaa in aaaaac:
							res.add(' '.join(sorted([a, aa, aaa, aaaa, aaaaa])))

	return [elem for elem in res]

def main():
	words = read_words(word_db)
	print(len(words), 'words.')
	words = filter_duplicates(words)
	print(len(words), 'unique words')
	words = filter_length_5(words)
	print(len(words), 'length 5 words.')
	words = filter_duplicate_letters(words)
	print(len(words), 'words with unique letters.')
	words, anagrams = filter_anagrams(words)
	print(len(words), 'equivalent words up to letter rearrangement.')
	w_words = words
	words = valid_pairs(words)
	print(len(words), 'valid pairs.')
	words, pair_anagrams = filter_anagrams(words)
	print(len(words), 'equivalent pairs up to letter rearrangement.')
	words = valid_pairs(words)
	print(len(words), 'valid pairs of pairs')
	words, pair_pair_anagrams = filter_anagrams(words)
	print(len(words), 'equivalent pairs of pairs up to letter rearrangement.')
	words = valid_pairs2(words, w_words)
	print(len(words), 'valid pairs of pairs and word.')
	words = substitute_anagrams(words, anagrams, pair_anagrams, pair_pair_anagrams)
	print(len(words), 'valid combinations with anagrams.')
	write_words(words, word_res_db)
	print('done.')

if __name__ == '__main__':
	main()
