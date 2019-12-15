import src.util.converter as converter
import xml.etree.ElementTree as et
import pandas as pd


class WordNetHelper:

    def __init__(self, english_wordnet, serbian_wordnet_path):
        self._map_id_and_pos_neg_score = {}  # id : list(pos, neg score)  much bigger than _map_serbian_wordnet
        self._map_serbian_wordnet = {}  # id : tuple(words)

        self._create_map_serbian_wordnet(serbian_wordnet_path)
        self._create_map_id_and_pos_neg_score(english_wordnet['ID'], english_wordnet['PosScore'], english_wordnet['NegScore'])

        self._data_frame_wordnet = self._create_data_frame()
        print(self._data_frame_wordnet)

    def _create_map_id_and_pos_neg_score(self, id_in_wnen, pos_scores_in_wnen, neg_scores_in_wnen):
        for i in range(len(id_in_wnen)):
            br_str = converter.convert_from_float_to_string(id_in_wnen[i])
            self._map_id_and_pos_neg_score[br_str] = [pos_scores_in_wnen[i], neg_scores_in_wnen[i]]  # TODO use tuple

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
                self._map_serbian_wordnet[id_] = tuple(list_literal)

    def _create_data_frame(self):
        ids = []
        scores = []
        literals = []

        for id_ in self._map_serbian_wordnet:
            if id_ in self._map_id_and_pos_neg_score:
                ids.append(id_)
                scores.append(self._map_id_and_pos_neg_score[id_])
                literals.append(self._map_serbian_wordnet[id_])

        data = {"id": ids,
                "score": scores,
                "literals": literals}

        return pd.DataFrame(data)

    def find_all_ids_for_word_in_serbian_wordnet(self, word_data):
        list_of_ids = []
        for key in self._map_serbian_wordnet.keys():
            for value in self._map_serbian_wordnet[key]:
                if word_data in value:
                    list_of_ids.append(key)
                    break
        return list_of_ids

    def get_pos_neg_score_for_serbian_word(self, word):
        if not self.find_all_ids_for_word_in_serbian_wordnet(word):
            return 0, 0

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
        return pos, neg
