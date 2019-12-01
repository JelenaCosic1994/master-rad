import src.util.converter as converter
import xml.etree.ElementTree as et


class WordNetHelper:

    def __init__(self, english_wordnet, serbian_wordnet_path):
        self._map_id_and_pos_neg_score = {}
        self._map_words_and_pos_neg_score = {}
        self._map_serbian_wordnet = {}

        self._create_map_id_and_pos_neg_score(english_wordnet['ID'], english_wordnet['PosScore'], english_wordnet['NegScore'])
        self._create_map_words_and_pos_neg_score(english_wordnet['SynsetTerms'], english_wordnet['PosScore'], english_wordnet['NegScore'])
        self._create_map_serbian_wordnet(serbian_wordnet_path)
        converter.convert_serbian_words_to_aurora(self._map_serbian_wordnet)

    def get_map_id_and_pos_neg_score(self):
        return self._map_id_and_pos_neg_score

    def get_map_words_and_pos_neg_score(self):
        return self._map_words_and_pos_neg_score

    def _create_map_id_and_pos_neg_score(self, id_in_wnen, pos_scores_in_wnen, neg_scores_in_wnen):
        for i in range(len(id_in_wnen)):
            br_str = converter.convert_from_float_to_string(id_in_wnen[i])
            self._map_id_and_pos_neg_score[br_str] = [pos_scores_in_wnen[i], neg_scores_in_wnen[i]]  # TODO use tuple

    def _create_map_words_and_pos_neg_score(self, synset_terms, pos_scores_in_wnen, neg_scores_in_wnen):
        for i in range(len(synset_terms)):
            self._map_words_and_pos_neg_score[synset_terms[i]] = [pos_scores_in_wnen[i], neg_scores_in_wnen[i]]
            #  TODO use tuple

    def _create_map_serbian_wordnet(self, xml_doc_path):
        xml_doc = et.parse(xml_doc_path)
        root = xml_doc.getroot()
        for synset in root.findall('SYNSET'):
            synonym = synset.find('SYNONYM')
            if synonym is not None:
                id_ = synset.find('ID').text[6:14]   # save only id number without other text
                list_literal = []
                for literal in synonym.findall('LITERAL'):
                    list_literal.append(literal.text)
                self._map_serbian_wordnet[id_] = list_literal

    def find_all_ids_for_word_in_serbian_wordnet(self, word):
        word_data = word.get_data()
        list_of_ids = []
        for key in self._map_serbian_wordnet.keys():
            for value in self._map_serbian_wordnet[key]:
                if word_data.strip() in value:
                    list_of_ids.append(key)
                    break
        return list_of_ids

    def set_pos_neg_score_for_serbian_word(self, word):
        list_of_ids = self.find_all_ids_for_word_in_serbian_wordnet(word)
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

    def set_pos_neg_score_for_english_word(self, word):
        pos_sum = 0
        neg_sum = 0
        n = 0
        for key in self._map_words_and_pos_neg_score:
            if word.get_data().strip() in key:
                pos_sum += self._map_words_and_pos_neg_score[key][0]
                neg_sum += self._map_words_and_pos_neg_score[key][1]
                n += 1
        pos, neg = (pos_sum / n, neg_sum / n) if n != 0 else (0, 0)
        word.set_pos_score(pos)
        word.set_neg_score(neg)

    def set_pos_neg_score_for_sentence(self, sentence, is_serbian):
        pos_sum = 0
        neg_sum = 0
        n = len(sentence.get_words())
        for word in sentence.get_words():
            self.set_pos_neg_score_for_serbian_word(word) if is_serbian else self.set_pos_neg_score_for_english_word(word)
            pos_sum += word.get_pos_score()
            neg_sum += word.get_neg_score()
        pos, neg = (pos_sum/n, neg_sum/n) if n != 0 else (0, 0)
        sentence.set_pos_score(pos)
        sentence.set_neg_score(neg)
