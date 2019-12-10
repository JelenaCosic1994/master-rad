import src.util.converter as converter
import xml.etree.ElementTree as et


class WordNetHelper:

    def __init__(self, english_wordnet, serbian_wordnet_path):
        self._map_id_and_pos_neg_score = {}
        self._map_word_pos_neg_score = {}
        self._map_serbian_wordnet = {}

        self._create_map_id_and_pos_neg_score(english_wordnet['ID'], english_wordnet['PosScore'], english_wordnet['NegScore'])
        self._create_map_word_and_pos_neg_score(english_wordnet['SynsetTerms'], english_wordnet['ID'])
        self._create_map_serbian_wordnet(serbian_wordnet_path)

    def _create_map_id_and_pos_neg_score(self, id_in_wnen, pos_scores_in_wnen, neg_scores_in_wnen):
        for i in range(len(id_in_wnen)):
            br_str = converter.convert_from_float_to_string(id_in_wnen[i])
            self._map_id_and_pos_neg_score[br_str] = [pos_scores_in_wnen[i], neg_scores_in_wnen[i]]  # TODO use tuple

    def _create_map_word_and_ids(self, synset_terms, id_in_wnen):
        map_word_and_ids = {}
        for i in range(len(synset_terms)):
            words = synset_terms[i].split()     # list of words
            for word in words:
                word = word.partition('#')[0]
                br_str = converter.convert_from_float_to_string(id_in_wnen[i])
                if word in map_word_and_ids:
                    map_word_and_ids[word].append(br_str)
                else:
                    map_word_and_ids[word] = [br_str]
        return map_word_and_ids

    def _create_map_word_and_pos_neg_score(self, synset_terms, id_in_wnen):
        map_word_and_ids = self._create_map_word_and_ids(synset_terms, id_in_wnen)
        for word in map_word_and_ids:
            ids = map_word_and_ids[word]
            pos = 0
            neg = 0
            count = 0
            for id in ids:
                p = self._map_id_and_pos_neg_score[id][0]
                n = self._map_id_and_pos_neg_score[id][1]
                if p != n:
                    pos += p
                    neg += n
                    count += 1
            pos, neg = (pos / count, neg / count) if count != 0 else (0, 0)
            self._map_word_pos_neg_score[word] = [pos, neg]

    def _create_map_serbian_wordnet(self, xml_doc_path):
        xml_doc = et.parse(xml_doc_path)
        root = xml_doc.getroot()
        for synset in root.findall('SYNSET'):
            synonym = synset.find('SYNONYM')
            if synonym is not None:
                id_ = synset.find('ID').text[6:14]   # save only id number without other text
                list_literal = []
                for literal in synonym.findall('LITERAL'):
                    list_literal.append(converter.convert_serbian_word_to_aurora(literal.text))
                self._map_serbian_wordnet[id_] = list_literal

    def find_all_ids_for_word_in_serbian_wordnet(self, word):
        word_data = word.get_data().strip()
        list_of_ids = []
        for key in self._map_serbian_wordnet.keys():
            for value in self._map_serbian_wordnet[key]:
                if word_data in value:
                    list_of_ids.append(key)
                    break
        return list_of_ids

    def set_pos_neg_score_for_serbian_word(self, word):
        list_of_ids = self.find_all_ids_for_word_in_serbian_wordnet(word)
        count = 0
        pos_sum = 0
        neg_sum = 0
        for id_ in list_of_ids:
            if id_ in self._map_id_and_pos_neg_score:
                p = self._map_id_and_pos_neg_score[id_][0]
                n = self._map_id_and_pos_neg_score[id_][1]
                if p != n:
                    pos_sum += p
                    neg_sum += n
                    count += 1
        pos, neg = (pos_sum / count, neg_sum / count) if count != 0 else (0, 0)
        word.set_pos_score(pos)
        word.set_neg_score(neg)

    def set_pos_neg_score_for_english_word(self, word):
        word_data = word.get_data().strip()
        pos_sum = 0
        neg_sum = 0
        count = 0
        for k in self._map_word_pos_neg_score:
            if word_data in k:
                p = self._map_word_pos_neg_score[k][0]
                n = self._map_word_pos_neg_score[k][1]
                if p != n:
                    pos_sum += p
                    neg_sum += n
                    count += 1

        pos, neg = (pos_sum / count, neg_sum / count) if count != 0 else (0, 0)
        word.set_pos_score(pos)
        word.set_neg_score(neg)

    def set_pos_neg_score_for_sentence(self, sentence, is_serbian):
        pos_sum = 0
        neg_sum = 0
        count = 0
        for word in sentence.get_words():
            self.set_pos_neg_score_for_serbian_word(word) if is_serbian else self.set_pos_neg_score_for_english_word(word)
            p = word.get_pos_score()
            n = word.get_neg_score()
            # only words with different scores
            if p != n:
                pos_sum += p
                neg_sum += n
                count += 1
        pos, neg = (pos_sum/count, neg_sum/count) if count != 0 else (0, 0)
        sentence.set_pos_score(pos)
        sentence.set_neg_score(neg)
