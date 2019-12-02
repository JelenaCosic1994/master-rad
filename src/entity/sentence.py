import re
from src.entity.word import Word
import src.util.converter as converter


class Sentence:
    def __init__(self, sentence, is_serbian):
        self._words = []
        for word in re.findall(r'\w+', sentence):
            if is_serbian and converter.is_cyrillic_text(word):
                self._words.append(Word(converter.convert_word_to_latinic(word)))
            else:
                self._words.append(Word(word))
        self._pos_score = None
        self._neg_score = None

    def get_words(self):
        return self._words

    def set_words(self, words):
        self._words = words

    def set_pos_score(self, pos_score):
        self._pos_score = pos_score

    def set_neg_score(self, neg_score):
        self._neg_score = neg_score

    def get_pos_score(self):
        return self._pos_score

    def get_neg_score(self):
        return self._neg_score

    def __str__(self):
        return ' '.join(word.get_data() for word in self._words)


