import src.util.converter as converter
import xml.etree.ElementTree as et


class WordNetHelper:

    def __init__(self, english_wordnet, serbian_wordnet_path):
        map_serbian_wordnet = self._create_map_serbian_wordnet(serbian_wordnet_path)  # id and list of literals
        map_id_and_pos_neg_score = self._create_map_id_and_pos_neg_score(english_wordnet['ID'], english_wordnet['PosScore'], english_wordnet['NegScore'])
        self._wordnet_data = self._create_wordnet_data(map_serbian_wordnet, map_id_and_pos_neg_score)   # id, score, literals

    @staticmethod
    def _create_map_id_and_pos_neg_score(id_in_wnen, pos_scores_in_wnen, neg_scores_in_wnen):
        """
        Function for creating map for english wordnet data
        :param id_in_wnen: column of ids in english wordnet data frame
        :param pos_scores_in_wnen: column of positive scores in english wordnet data frame
        :param neg_scores_in_wnen: column of negative scores in english wordnet data frame
        :return: map - key: id for synset = string number which length is 8 chars
                       value: list which elements are positive and negative score for id in synset
        """
        map_id_and_pos_neg_score = {}
        for i in range(len(id_in_wnen)):
            br_str = converter.convert_from_float_to_string(id_in_wnen[i])
            map_id_and_pos_neg_score[br_str] = [pos_scores_in_wnen[i], neg_scores_in_wnen[i]]  # TODO use tuple
        return map_id_and_pos_neg_score

    @staticmethod
    def _create_map_serbian_wordnet(serbian_wordnet_path):
        """
        Function for creating map for serbian wordnet data
        :param serbian_wordnet_path: path to the serbian wordnet file
        :return: map - key: id for synset = string number which length is 8 chars,
                       value: tuple of literals in synset
        """
        map_serbian_wordnet = {}
        xml_doc = et.parse(serbian_wordnet_path)
        root = xml_doc.getroot()
        for synset in root.findall('SYNSET'):
            synonym = synset.find('SYNONYM')
            if synonym is not None:
                id_ = synset.find('ID').text[6:14]   # save only id number without other text
                list_literal = []
                for literal in synonym.findall('LITERAL'):
                    lit_aurora = converter.convert_serbian_word_to_aurora(literal.text)
                    list_literal.append(lit_aurora.lower())
                map_serbian_wordnet[id_] = tuple(list_literal)
        return map_serbian_wordnet

    @staticmethod
    def _create_wordnet_data(map_serbian_wordnet, map_id_and_pos_neg_score):
        """
        Function for creating one map from serbian and english wordnet maps
        :param map_serbian_wordnet: map for serbian wordnet
        :param map_id_and_pos_neg_score: map for english wordnet
        :return: data with columns id, score and literals from both maps - this is map intersection
        """
        ids = []
        scores = []
        literals = []

        for id_ in map_serbian_wordnet:
            if id_ in map_id_and_pos_neg_score:
                ids.append(id_)
                scores.append(map_id_and_pos_neg_score[id_])
                literals.append(map_serbian_wordnet[id_])

        data = {"id": ids,
                "score": scores,
                "literals": literals}

        return data

    def get_pos_neg_score_for_serbian_word(self, word, file):
        """
        Function for calculating positive and negative score for serbian word
        :param word: input word
        :param file: file for writing results
        :return: positive and negative score
        """
        pos_scores = []
        neg_scores = []

        for i in range(len(self._wordnet_data["id"])):
            literals = self._wordnet_data["literals"][i]
            for literal in literals:
                if literal.startswith(word):
                    score = self._wordnet_data["score"][i]
                    file.write("\nSENTIMENT: " + "positive: " + str(score[0]) + ", negative: " + str(score[1]) + "\n")
                    if score[0] != score[1] or score[0] != 0:
                        pos_scores.append(score[0])
                        neg_scores.append(score[1])
                        break
        if len(pos_scores) > 0:
            return sum(pos_scores) / len(pos_scores), sum(neg_scores) / len(neg_scores)
        else:
            return 0, 0
