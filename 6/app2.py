class WordFactory:
    def __init__(self, dictionary):
        self.dictionary = set(dictionary)

    def get_words(self):
        return self.dictionary

    def get_words_len(self, word_len):
        return WordFactory(filter(lambda x: len(x) == word_len, self.dictionary))

    def exclude_words_with_latter(self, letter: str, position: int):
        return WordFactory(filter(lambda x: x[position] != letter, self.dictionary))


class Player:
    def __init__(self, dictionary: set, word_len: int):
        self.factory = WordFactory(dictionary).get_words_len(word_len)

    def guess(self, latter, pos):
        result = self.factory.exclude_words_with_latter(latter, pos)
        if len(result.get_words()) == 0:
            return "OK"
        self.factory = result
        return "MISS"
