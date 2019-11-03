import re
import nltk


class Parser:

    def __init__(self, stop_words):
        self._stop_words = stop_words

    @staticmethod
    def get_words_from_sentence(sentence):
        return re.findall(r'\w+', sentence)

    @staticmethod
    def get_sentences_from_text(text):
        # nltk.download('punkt')  # ovo je moralo prvi put da se pozove da se skine biblioteka
        return nltk.tokenize.sent_tokenize(text)

    def remove_stop_words_from_sentence(self, sentence):
        words = Parser.get_words_from_sentence(sentence)
        result_words = []
        for word in words:
            if word.lower() not in self._stop_words:
                result_words.append(word)
        return result_words

    def remove_stop_words_from_text(self, text):
        sentences = Parser.get_sentences_from_text(text)
        text_without_stop_words = []
        for sentence in sentences:
            sentence_without_stop_words = Parser(self._stop_words).remove_stop_words_from_sentence(sentence)
            text_without_stop_words += sentence_without_stop_words
        return text_without_stop_words     # list of strings

    def get_texts_without_stop_words(self, reviews_list):
        reviews_without_stop_words = []
        for review in reviews_list:
            list_of_words_without_stop_words = Parser(self._stop_words).remove_stop_words_from_text(review)
            reviews_without_stop_words.append(list_of_words_without_stop_words)
        return reviews_without_stop_words   # list of lists
