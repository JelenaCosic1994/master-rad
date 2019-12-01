import re
from transliterate import translit
from src.word import Word
import src.stemmer.stemmer as stemmer
import xml.etree.ElementTree as et


class Parser:  # TODO change name

    def __init__(self, stop_words, wnsrp_path, wnen, dictionary=None):
        self._stop_words = stop_words
        self._wnsrp = self.parse_serbian_wordnet_xml(wnsrp_path)
        self.convert_serbian_words_to_aurora(self._wnsrp)
        self._dictionary = dictionary
        self._map_id_and_pos_neg_score = {}
        self._map_words_and_pos_neg_score = {}

        self._create_map_id_and_pos_neg_score(wnen['ID'], wnen['PosScore'], wnen['NegScore'])
        self._create_map_words_and_pos_neg_score(wnen['SynsetTerms'], wnen['PosScore'], wnen['NegScore'])

    def get_map_id_and_pos_neg_score(self):
        return self._map_id_and_pos_neg_score

    def get_map_words_and_pos_neg_score(self):
        return self._map_words_and_pos_neg_score

    def _create_map_id_and_pos_neg_score(self, id_in_wnen, pos_scores_in_wnen, neg_scores_in_wnen):
        for i in range(len(id_in_wnen)):
            br_str = Parser.convert_from_float_to_string(id_in_wnen[i])
            self._map_id_and_pos_neg_score[br_str] = [pos_scores_in_wnen[i], neg_scores_in_wnen[i]]  # TODO use tuple

    def _create_map_words_and_pos_neg_score(self, synset_terms, pos_scores_in_wnen, neg_scores_in_wnen):
        for i in range(len(synset_terms)):
            self._map_words_and_pos_neg_score[synset_terms[i]] = [pos_scores_in_wnen[i], neg_scores_in_wnen[i]]
            #  TODO use tuple

    def remove_stop_words_from_sentence(self, sentence):
        words = sentence.get_words()
        result_words = []
        for word in words:
            if word.get_data().lower() not in self._stop_words:
                result_words.append(word)
        sentence.set_words(result_words)

    @staticmethod
    def is_cyrillic_text(text):
        return bool(re.search('[а-шА-Ш]', text))

    @staticmethod
    def convert_sentence_to_latinic(sentence):
        words = sentence.get_words()
        result_words = []
        for word in words:
            word = Word(translit(word.get_data(), 'sr', reversed=True))
            result_words.append(word)
        sentence.set_words(result_words)

    def is_word_in_dictionary(self, word):  # word is a object of class Word
        return False
        #  TODO implement

    def lemmatization_and_stemming_sentence(self, sentence):
        words = sentence.get_words()
        result_words = []
        for word in words:
            # if word is in dictionary then replace them with lemma from dictionary
            if self.is_word_in_dictionary(word):
                result_words.append(word)
            # else apply stemmer
            else:
                stem_str = stemmer.stem_str(word.get_data())
                result_words.append(Word(stem_str))
        sentence.set_words(result_words)

    @staticmethod
    def parse_serbian_wordnet_xml(xml_doc_path):
        xml_doc = et.parse(xml_doc_path)
        root = xml_doc.getroot()
        map = {}
        for synset in root.findall('SYNSET'):
            synonym = synset.find('SYNONYM')
            if synonym is not None:
                id_ = synset.find('ID').text[6:14]   # save only id number without other text
                list_literal = []
                for literal in synonym.findall('LITERAL'):
                    list_literal.append(literal.text)
                map[id_] = list_literal
        return map

    @staticmethod
    def convert_serbian_words_to_aurora(serbian_wn_map):
        for key in serbian_wn_map.keys():
            for i in range(len(serbian_wn_map[key])):
                str = serbian_wn_map[key][i]
                str = str.replace("š", "sx")
                str = str.replace("č", "cx")
                str = str.replace("ć", "cy")
                str = str.replace("đ", "dx")
                str = str.replace("ž", "zx")
                str = str.replace("Š", "sx")
                str = str.replace("Č", "cx")
                str = str.replace("Ć", "cy")
                str = str.replace("Đ", "dx")
                str = str.replace("Ž", "zx")
                serbian_wn_map[key][i] = str  # TODO check if it works without this line

    def find_all_ids_for_word_in_wnsrp(self, word):
        word_data = word.get_data()
        list_of_ids = []

        for key in self._wnsrp.keys():
            for value in self._wnsrp[key]:
                if word_data.strip() in value:
                    list_of_ids.append(key)
                    break
        return list_of_ids

    def set_pos_neg_score_for_word_from_wnen(self, word):
        list_of_ids = self.find_all_ids_for_word_in_wnsrp(word)
        n = 0
        pos_sum = 0
        neg_sum = 0

        for id_ in list_of_ids:
            if id_ in self._map_id_and_pos_neg_score:
                pos_sum += self._map_id_and_pos_neg_score[id_][0]
                neg_sum += self._map_id_and_pos_neg_score[id_][1]
                n += 1

        pos, neg = (pos_sum / n, neg_sum / n) if n != 0 else (0, 0)
        word.set_pos_score(pos)
        word.set_neg_score(neg)

    def set_pos_neg_score_for_sentence_from_wnen(self, sentence):
        pos_sum = 0
        neg_sum = 0
        n = len(sentence.get_words())
        for word in sentence.get_words():
            self.set_pos_neg_score_for_word_from_wnen(word)
            pos_sum += word.get_pos_score()
            neg_sum += word.get_neg_score()
        pos, neg = (pos_sum/n, neg_sum/n) if n != 0 else (0, 0)
        sentence.set_pos_score(pos)
        sentence.set_neg_score(neg)

    @staticmethod
    def convert_from_float_to_string(num_float):
        try:
            int_num = int(num_float)
            num_string = str(int_num)
            if len(num_string) < 8:
                n = 8 - len(num_string)
                num_string = '0'*n + num_string
            return num_string
        except:
            return -1  # TODO check if this is correct

    def calculate_pos_neg_score_for_dokument_split_by_sentences(self, text):
        pos_sum = 0
        neg_sum = 0
        n = len(text.get_sentences())
        for sentence in text.get_sentences():
            if self.is_cyrillic_text(sentence.__str__()):
                self.convert_sentence_to_latinic(sentence)
            self.remove_stop_words_from_sentence(sentence)
            self.lemmatization_and_stemming_sentence(sentence)
            self.set_pos_neg_score_for_sentence_from_wnen(sentence)
            # print(sentence.get_pos_score(), " , ", sentence.get_neg_score())
            pos_sum += sentence.get_pos_score()
            neg_sum += sentence.get_neg_score()
        if n != 0:
            return pos_sum/n, neg_sum/n
        else:
            return 0, 0
