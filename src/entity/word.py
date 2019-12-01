

class Word:
    def __init__(self, word):
        self._pos_score = None
        self._neg_score = None
        self._data = word

    def get_data(self):
        return self._data

    def set_pos_score(self, pos_score):
        self._pos_score = pos_score

    def set_neg_score(self, neg_score):
        self._neg_score = neg_score

    def get_pos_score(self):
        return self._pos_score

    def get_neg_score(self):
        return self._neg_score

    def __str__(self):
        return '' + self._data  # TODO remove concatenation
