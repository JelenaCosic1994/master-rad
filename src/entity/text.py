import nltk
from src.entity.sentence import Sentence


class Text:
    def __init__(self, text):
        self._sentences = []
        for sentence in nltk.tokenize.sent_tokenize(text):
            self._sentences.append(Sentence(sentence))
        self._pos_score = None
        self._neg_score = None

    def get_sentences(self):
        return self._sentences

    def set_sentences(self, sentences):
        self._sentences = sentences

    def set_pos_score(self, pos_score):
        self._pos_score = pos_score

    def set_neg_score(self, neg_score):
        self._neg_score = neg_score

    def get_pos_score(self):
        return self._pos_score

    def get_neg_score(self):
        return self._neg_score

    def __str__(self):
        return '\n'.join(str(sentence) for sentence in self._sentences)
