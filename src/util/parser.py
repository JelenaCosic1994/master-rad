from src.entity.word import Word
import src.util.serbian_stemmer as serbian_stemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


class Parser:   # TODO: change name

    def __init__(self, stop_words, dictionary=None):
        self._serbian_stop_words = stop_words
        self._dictionary = dictionary
        self._english_lemmatizer = WordNetLemmatizer()
        self._english_stemmer = PorterStemmer()
        self._english_stop_words = set(stopwords.words('english'))

    def remove_stop_words_from_sentence(self, sentence, is_serbian):
        stop_words = self._serbian_stop_words if is_serbian else self._english_stop_words
        words = sentence.get_words()
        result_words = []
        for word in words:
            if word.get_data().lower() not in stop_words:
                result_words.append(word)
        sentence.set_words(result_words)

    def is_word_in_dictionary(self, word):  # word is a object of class Word
        return False
        #  TODO implement

    def lemmatization_and_stemming_serbian_sentence(self, sentence):
        words = sentence.get_words()
        result_words = []
        for word in words:
            # if word is in dictionary then replace them with lemma from dictionary
            if self.is_word_in_dictionary(word):
                result_words.append(word)
            # else apply serbian stemmer
            else:
                stem_str = serbian_stemmer.stem_str(word.get_data())
                result_words.append(Word(stem_str))
        sentence.set_words(result_words)

    def lemmatization_and_stemming_english_sentence(self, sentence):
        words = sentence.get_words()
        result_words = []
        for word in words:
            lemma = self._english_lemmatizer.lemmatize(word.get_data())
            result_words.append(Word(self._english_stemmer.stem(lemma)))
        sentence.set_words(result_words)

