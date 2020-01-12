import src.util.converter as converter
import src.util.serbian_stemmer as serbian_stemmer
import src.util.constants as const
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
import os
import xml.etree.ElementTree as et


class WordNetHelper:

    def __init__(self, english_wordnet, serbian_wordnet_path, serbian_stop_words):
        map_serbian_wordnet = self._create_map_serbian_wordnet(serbian_wordnet_path)  # id and list of literals
        map_id_and_pos_neg_score = self._create_map_id_and_pos_neg_score(english_wordnet['ID'], english_wordnet['PosScore'], english_wordnet['NegScore'])
        self._wordnet_data = self._create_wordnet_data(map_serbian_wordnet, map_id_and_pos_neg_score)   # id, score, literals
        self._lemmatizer = WordNetLemmatizer()
        self._english_stop_words = set(stopwords.words('english'))
        self._serbian_stop_words = serbian_stop_words

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

    def calc_percents_for_corpus(self, corpus, is_english, three_classes):
        """
        Function for calculating precision, recall, f measure and accuracy for given corpus
        :param corpus: given corpus (english or serbian)
        :param is_english: True if corpus is english, False if corpus is serbian
        :param three_classes: True if  corpus have 3 classes (positive, negative and neutral), False otherwise
        :return: precision, recall, f measure and accuracy for given corpus
        """
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        i = 1
        for t, rating in corpus:
            text = converter.remove_punctuation(t)

            if is_english:
                file = open(".." + os.sep + "output_data" + os.sep + "english_corpus" + os.sep + str(i) + "_" + rating + ".txt", "w", encoding='utf8')
            else:
                file = open(".." + os.sep + "output_data" + os.sep + "serbian_corpus" + os.sep + str(i) + "_" + rating + ".txt", "w", encoding='utf8')
            i += 1

            new_rating = self.swn_polarity(text, is_english, three_classes, file)

            file.write("\nNew Rating: " + new_rating)
            file.close()

            if rating == const.POSITIVE:
                if new_rating == const.POSITIVE:
                    tp += 1
                if new_rating == const.NEGATIVE:
                    fn += 1
            if rating == const.NEGATIVE:
                if new_rating == const.POSITIVE:
                    fp += 1
                if new_rating == const.NEGATIVE:
                    tn += 1

        precision = tp / (tp + fp) * 100
        recall = tp / (tp + fn) * 100
        f_measure = 2 * precision * recall / (precision + recall)
        accuracy = (tp + tn) / (tp + fp + fn + tn) * 100

        return precision, recall, f_measure, accuracy

    def swn_polarity(self, text, is_english, three_classes, file):
        """
        Function for calculating sentiment polarity: NEGATIVE or POSITIVE for given text
        :param text: string which represents text - film review
        :param is_english: param for recognizing language
        :param three_classes: True if  corpus have 3 classes (positive, negative and neutral), False otherwise
        :param file: file to write results
        :return: sentiment polarity for given text
        """
        pos_score_text, neg_score_text, count_words = self._get_score_for_text(text, is_english)
        pos_avg_text, neg_avg_text = (pos_score_text / count_words, neg_score_text / count_words) if count_words != 0 else (0, 0)
        file.write("\n score for text: positive - " + str(pos_avg_text) + " , negative - " + str(neg_avg_text) + " and diff: " + str(pos_avg_text-neg_avg_text) + "\n")

        treshold_value = 0.05
        if three_classes:
            if abs(pos_avg_text - neg_avg_text) <= treshold_value:
                return const.NEUTRAL
            if (pos_avg_text - neg_avg_text) > treshold_value:
                return const.POSITIVE
            if (neg_avg_text - pos_avg_text) > treshold_value:
                return const.NEGATIVE
        else:
            if pos_avg_text > neg_avg_text:
                return const.POSITIVE
            else:
                return const.NEGATIVE

    def _get_score_for_text(self, text, is_english):
        """
        Private function for calculating score for text
        :param text: given text
        :param is_english: param for recognizing language
        :return: positive score, negative score and number of right words
        """
        count_words = 0
        pos_score_text = 0
        neg_score_text = 0
        par = 1

        if is_english:
            clean_text = self.clear_english_text(text)
            for lemma, wn_tag in clean_text:
                pos, neg = self.get_pos_neg_score_for_english_word(lemma, wn_tag)

                if pos != neg or pos != 0:
                    pos_score_text += pos * par
                    neg_score_text += neg * par
                    count_words += 1
                    par += 1
        else:
            clean_text = self.clear_serbian_text(text)
            for word in clean_text:
                # get pos and neg score for word from wordnet
                pos, neg = self.get_pos_neg_score_for_serbian_word(word)

                if pos != neg or pos != 0:
                    pos_score_text += pos * par
                    neg_score_text += neg * par
                    count_words += 1
                    # par += 1
        return pos_score_text, neg_score_text, count_words

    def clear_english_text(self, text):
        """
        Clear english text (ignore words with wrong tag, ignore stop words i do lemmatization)
        :param text: given text
        :return: clean text
        """
        clean_text = []

        tagged_text = pos_tag(word_tokenize(text))

        for word, tag in tagged_text:
            wn_tag = converter.penn_to_wn(tag)

            # ignore words with wrong tag
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            # ignore stop words
            if word in self._english_stop_words:
                continue

            # lemmatization
            lemma = self._lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue

            clean_text.append((lemma, wn_tag))

        return clean_text

    def clear_serbian_text(self, text):
        """
        Clear serbian text(convert to latinic, ignore stop words, and stemming)
        :param text: given text
        :return: clean text
        """
        clean_text = []

        for w in word_tokenize(text):
            # convert word to lowercase and delete spaces
            word = w.lower().strip()

            # if is word in cyrillic convert to latinic
            if converter.is_cyrillic_text(word):
                word = converter.convert_word_to_latinic(word)

            # ignore stop words
            if word in self._serbian_stop_words:
                continue

            # stemming
            stem_word = serbian_stemmer.stem_str(word)

            result_word = stem_word.strip()

            clean_text.append(result_word)

        return clean_text

    def get_pos_neg_score_for_serbian_word(self, word):
        """
        Function for calculating positive and negative score for serbian word
        :param word: input word
        :return: positive and negative score
        """
        pos_scores = []
        neg_scores = []

        for i in range(len(self._wordnet_data["id"])):
            literals = self._wordnet_data["literals"][i]
            for literal in literals:
                if literal.startswith(word):
                    score = self._wordnet_data["score"][i]
                    if score[0] != score[1] or score[0] != 0:
                        pos_scores.append(score[0])
                        neg_scores.append(score[1])
                        break
        if len(pos_scores) > 0:
            return sum(pos_scores) / len(pos_scores), sum(neg_scores) / len(neg_scores)
        else:
            return 0, 0

    def get_pos_neg_score_for_english_word(self, lemma, wn_tag):
        """
        Function for calculating positive and negative score for english word
        :param lemma: input lemma for word
        :param wn_tag: tag from wordnet
        :return: positive and negative score
        """
        # get synsets for lemma
        synsets = wn.synsets(lemma, pos=wn_tag)
        pos = 0
        neg = 0

        if synsets:
            # take first synset
            swn_synset = swn.senti_synset(synsets[0].name())
            pos = swn_synset.pos_score()
            neg = swn_synset.neg_score()

        return pos, neg
