import re


class Alphabets:
    def __init__(self, arg):
        self.alphabet = arg.upper()
        self.regex = r'[A-Za-z]+'

    def identify(self):
        words = re.findall(self.regex, self.alphabet)
        return words

    def num_of_words(self):
        words = self.identify()
        return len(words)

    def num_of_chars(self):
        chars = self.alphabet
        return len(chars) - (self.num_of_words() - 1)

    def count(self):
        word_arr = self.identify()
        word_count = {}
        for word in word_arr:
            if word in word_count:
                word_count[word] += 1
            elif word not in word_count:
                word_count[word] = 1
        return word_count

    def most_frequent(self):
        key_value = self.count().items()
        max_frequency = ("", 0)
        for k, v in key_value:
            if v > max_frequency[1]:
                max_frequency = (k, v)
            else:
                continue
        return max_frequency
