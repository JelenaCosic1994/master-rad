import src.util.converter as converter
import src.util.loader as loader
import src.util.constants as const
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag


class WordNetHelper:

    def __init__(self, english_wordnet, serbian_wordnet_original, serbian_wordnet_changed, serbian_wordnet_deleted,
                 serbian_stop_words, dictionary_path):
        # data for english wordnet, contains TAG, SCORE(pos, neg), LITERALS
        self._wnen_data = self._create_data_for_wnen(english_wordnet['# POS'], english_wordnet['PosScore'],
                                                     english_wordnet['NegScore'], english_wordnet['SynsetTerms'])
        # data for serbian wordnet, contains ID, LITERAL, POS_SCORE, NEG_SCORE
        self._wnsrb_data_original = self._create_data_for_wnsrb(serbian_wordnet_original['ID'],
                                                                serbian_wordnet_original['Literal'],
                                                                serbian_wordnet_original['positive'],
                                                                serbian_wordnet_original['negative'])
        self._wnsrb_data_changed = self._create_data_for_wnsrb(serbian_wordnet_changed['ID'],
                                                               serbian_wordnet_changed['Literal'],
                                                               serbian_wordnet_changed['positive'],
                                                               serbian_wordnet_changed['negative'])
        self._wnsrb_data_deleted = self._create_data_for_wnsrb(serbian_wordnet_deleted['ID'],
                                                               serbian_wordnet_deleted['Literal'],
                                                               serbian_wordnet_deleted['positive'],
                                                               serbian_wordnet_deleted['negative'])

        self._lemmatizer = WordNetLemmatizer()
        self._english_stop_words = set(stopwords.words('english'))
        self._serbian_stop_words = serbian_stop_words
        self._dictionary_path = dictionary_path

    @staticmethod
    def _create_data_for_wnen(tag_in_wnen, pos_scores_in_wnen, neg_scores_in_wnen, literals_in_wnen):
        """
        Function for creating data for english wordnet
        :param tag_in_wnen: column of tags in english wordnet data frame
        :param pos_scores_in_wnen: column of positive scores in english wordnet data frame
        :param neg_scores_in_wnen: column of negative scores in english wordnet data frame
        :param literals_in_wnen: column of literals in english wordnet data frame
        :return: data - data with columns: tags, score(pos, neg) and literals
        """
        list_pos_neg_score = []
        all_literals = []
        for i in range(len(tag_in_wnen)):
            list_pos_neg_score.append((pos_scores_in_wnen[i], neg_scores_in_wnen[i]))
            literals = []
            for l in literals_in_wnen[i].split(" "):
                literals.append(l.split("#")[0])
            all_literals.append(literals)

        data = {"tag": list(tag_in_wnen),
                "score": list_pos_neg_score,
                "literals": all_literals}
        return data

    @staticmethod
    def _create_data_for_wnsrb(id, literal, pos_score, neg_score):
        """
        Function for creating data for serbian wordnet
        :param id: data with all ids
        :param literal: data with all literals
        :param pos_score: data with all pos scores
        :param neg_score: data with all neg scores
        :return: data - data with columns: id, literal, pos_score, neg_score
        """
        data = {"id": list(id),
                "literal": list(literal),
                "pos_score": list(pos_score),
                "neg_score": list(neg_score)}
        return data

    def calc_percents_for_corpus(self, corpus, is_english, three_classes, wnsrb_param=None, is_prefix=None, treshold_value=None):
        """
        Function for calculating precision, recall, f measure and accuracy for given corpus
        :param corpus: given corpus (english or serbian)
        :param is_english: True if corpus is english, False if corpus is serbian
        :param three_classes: True if corpus have 3 classes (positive, negative and neutral), False otherwise
        :param wnsrb_param: 'o' for use _wnsrb_data_original
                            'c' for use _wnsrb_data_changed
                            'd' for use _wnsrb_data_deleted
        :param is_prefix: True if word is prefix of literal, False if word is equals to literal
        :param treshold_value: value for neutral class range
        :return: precision, recall, f measure and accuracy for given corpus
        """

        i = 1
        # variables for two classes
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        # variables for POSITIVE class
        pos_pos = 0
        pos_neg = 0
        pos_neu = 0
        # variables for NEGATIVE class
        neg_pos = 0
        neg_neg = 0
        neg_neu = 0
        # variables for NEUTRAL class
        neu_pos = 0
        neu_neg = 0
        neu_neu = 0

        for text, rating in corpus:
            new_rating = self.swn_polarity(i, text, is_english, three_classes, wnsrb_param, is_prefix, treshold_value)
            i += 1

            if three_classes:
                if rating == const.POSITIVE:
                    if new_rating == const.POSITIVE:
                        pos_pos += 1
                    if new_rating == const.NEGATIVE:
                        pos_neg += 1
                    if new_rating == const.NEUTRAL:
                        pos_neu += 1
                if rating == const.NEGATIVE:
                    if new_rating == const.POSITIVE:
                        neg_pos += 1
                    if new_rating == const.NEGATIVE:
                        neg_neg += 1
                    if new_rating == const.NEUTRAL:
                        neg_neu += 1
                if rating == const.NEUTRAL:
                    if new_rating == const.POSITIVE:
                        neu_pos += 1
                    if new_rating == const.NEGATIVE:
                        neu_neg += 1
                    if new_rating == const.NEUTRAL:
                        neu_neu += 1
            else:
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

        print("FOR POSITIVE CLASS: pos:" + str(pos_pos) + ", neg: " + str(pos_neg) + ", neu:" + str(pos_neu))
        print("FOR NEGATIVE CLASS: pos:" + str(neg_pos) + ", neg: " + str(neg_neg) + ", neu:" + str(neg_neu))
        print("FOR NEUTRAL CLASS: pos:" + str(neu_pos) + ", neg: " + str(neu_neg) + ", neu:" + str(neu_neu))
        sum_neu = neg_neu + pos_neu + neu_neu
        sum_pos = neg_pos + pos_pos + neu_pos
        sum_neg = neg_neg + pos_neg + neu_neg
        print("Positive: " + str(sum_pos))
        print("Negative: " + str(sum_neg))
        print("Neutral: " + str(sum_neu))

        if three_classes:
            # calculating
            tp_pos = pos_pos
            fp_pos = neg_pos + neu_pos
            tn_pos = neg_neg + neg_neu + neu_neg + neu_neu
            fn_pos = pos_neg + pos_neu

            precision_pos = tp_pos / (tp_pos + fp_pos) * 100
            recall_pos = tp_pos / (tp_pos + fn_pos) * 100
            f_measure_pos = 2 * precision_pos * recall_pos / (precision_pos + recall_pos)
            accuracy_pos = (tp_pos + tn_pos) / (tp_pos + fp_pos + fn_pos + tn_pos) * 100

            tp_neg = neg_neg
            fp_neg = pos_neg + neu_neg
            tn_neg = pos_pos + pos_neu + neu_pos + neu_neu
            fn_neg = neg_pos + neg_neu

            precision_neg = tp_neg / (tp_neg + fp_neg) * 100
            recall_neg = tp_neg / (tp_neg + fn_neg) * 100
            f_measure_neg = 2 * precision_neg * recall_neg / (precision_neg + recall_neg)
            accuracy_neg = (tp_neg + tn_neg) / (tp_neg + fp_neg + fn_neg + tn_neg) * 100

            tp_neu = neu_neu
            fp_neu = pos_neu + neg_neu
            tn_neu = pos_pos + pos_neg + neg_pos + neg_neg
            fn_neu = neu_pos + neu_neg

            precision_neu = tp_neu / (tp_neu + fp_neu) * 100
            recall_neu = tp_neu / (tp_neu + fn_neu) * 100
            f_measure_neu = 2 * precision_neu * recall_neu / (precision_neu + recall_neu)
            accuracy_neu = (tp_neu + tn_neu) / (tp_neu + fp_neu + fn_neu + tn_neu) * 100

            # calculating score for all classes
            precision = (precision_pos + precision_neg + precision_neu) / 3
            recall = (recall_pos + recall_neg + recall_neu) / 3
            f_measure = (f_measure_pos + f_measure_neg + f_measure_neu) / 3
            accuracy = (accuracy_pos + accuracy_neg + accuracy_neu) / 3

            print("Positive: precision: " + str(precision_pos) + ", recall: " + str(recall_pos) + ", f_measure: " + str(f_measure_pos) + ", accuracy:" + str(accuracy_pos))
            print("Negative: precision: " + str(precision_neg) + ", recall: " + str(recall_neg) + ", f_measure: " + str(
                f_measure_neg) + ", accuracy:" + str(accuracy_neg))
            print("Neutral: precision: " + str(precision_neu) + ", recall: " + str(recall_neu) + ", f_measure: " + str(
                f_measure_neu) + ", accuracy:" + str(accuracy_neu))

            return precision, recall, f_measure, accuracy

        else:
            precision = tp / (tp + fp) * 100
            recall = tp / (tp + fn) * 100
            f_measure = 2 * precision * recall / (precision + recall)
            accuracy = (tp + tn) / (tp + fp + fn + tn) * 100
            print("FOR TWO CLASSES: tp:" + str(tp) + ", fp: " + str(fp) + ", tn:" + str(tn) + " fn:" + str(fn))

            return precision, recall, f_measure, accuracy

    def swn_polarity(self, ordinal, text, is_english, three_classes, wnsrb_param=None, is_prefix=None, treshold_value=None):
        """
        Function for calculating sentiment polarity: NEGATIVE or POSITIVE for given text
        :param ordinal: ordinal number for text in dictionary
        :param text: string which represents text - film review
        :param is_english: param for recognizing language
        :param three_classes: True if  corpus have 3 classes (positive, negative and neutral), False otherwise
        :param wnsrb_param: 'o' for use _wnsrb_data_original
                            'c' for use _wnsrb_data_changed
                            'd' for use _wnsrb_data_deleted
        :param is_prefix: True if word is prefix of literal, False if word is equals to literal
        :param treshold_value: value for neutral class range
        :return: sentiment polarity for given text
        """
        pos_score_text, neg_score_text, count_words = self.get_score_for_text(ordinal, text, is_english,
                                                                                         three_classes, wnsrb_param,
                                                                                         is_prefix)
        pos_avg_text, neg_avg_text = (pos_score_text / count_words, neg_score_text / count_words) if count_words != 0 else (0, 0)

        diff_1 = round(pos_avg_text - neg_avg_text, 2)
        diff_2 = round(neg_avg_text - pos_avg_text, 2)

        if three_classes:
            if abs(diff_1) <= treshold_value:
                return const.NEUTRAL
            if diff_1 > treshold_value:
                return const.POSITIVE
            if diff_2 > treshold_value:
                return const.NEGATIVE
        else:
            if pos_avg_text > neg_avg_text:
                return const.POSITIVE
            else:
                return const.NEGATIVE

    def get_score_for_text(self, ordinal, text, is_english, three_classes, wnsrb_param=None, is_prefix=None):
        """
        Private function for calculating score for text
        :param ordinal: ordinal number for text in dictionary
        :param text: given text
        :param is_english: param for recognizing language
        :param three_classes: True if  corpus have 3 classes (positive, negative and neutral), False otherwise
        :param wnsrb_param: 'o' for use _wnsrb_data_original
                            'c' for use _wnsrb_data_changed
                            'd' for use _wnsrb_data_deleted
        :param is_prefix: True if word is prefix of literal, False if word is equals to literal
        :return: positive score, negative score and number of right words
        """
        count_words = 0
        pos_score_text = 0
        neg_score_text = 0

        if is_english:
            clean_text = self.clear_english_text(text)
            for lemma, wn_tag in clean_text:
                pos, neg = self.get_score_for_english_word(lemma, wn_tag)
                if pos != -1 and (pos != neg or pos != 0):
                    pos_score_text += pos
                    neg_score_text += neg
                    count_words += 1
        else:
            clean_text = self.clear_serbian_text(ordinal, three_classes)
            for word in clean_text:
                pos, neg = self.get_score_for_serbian_word(word, wnsrb_param, is_prefix)
                if pos != -1 and (pos != neg or pos != 0):
                    pos_score_text += pos
                    neg_score_text += neg
                    count_words += 1

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

    def clear_serbian_text(self, ordinal, three_classes):
        """
        Clear serbian text(convert to latinic, ignore stop words, lemmatization and stemming)
        :param ordinal: given ordinal of text
        :param three_classes: True if  corpus have 3 classes (positive, negative and neutral), False otherwise
        :return: clean text
        """
        clean_text = []

        data_text = loader.load_text_dictionary(ordinal, self._dictionary_path, three_classes)
        for w, tag, lemma in data_text:
            # convert word to lowercase and delete spaces
            word = w.lower().strip()

            # if is word in cyrillic convert to latinic
            if converter.is_cyrillic_text(word):
                word = converter.convert_text_to_latinic(word)

            # ignore stop words
            if word in self._serbian_stop_words:
                continue

            if not (tag.startswith("ADV") or tag.startswith("A:") or tag.startswith("N:") or tag.startswith("V:")):
                continue

            result_word = lemma.lower().strip()

            clean_text.append(result_word)

        return clean_text

    def get_score_for_serbian_word(self, word, wnsrb_param, is_prefix):
        """
        Function for calculating positive and negative score for serbian word
        :param word: input word
        :param wnsrb_param: 'o' for use _wnsrb_data_original
                            'c' for use _wnsrb_data_changed
                            'd' for use _wnsrb_data_deleted
        :param is_prefix: True if word is prefix of literal, False if word is equals to literal
        :return: positive and negative score for input word, or -1,-1 if word is not found in wnsrb
        """
        if wnsrb_param == 'c':
            sentiments = self._wnsrb_data_changed
        elif wnsrb_param == 'd':
            sentiments = self._wnsrb_data_deleted
        else:
            sentiments = self._wnsrb_data_original

        pos_scores = []
        neg_scores = []
        for i in range(len(sentiments["literal"])):
            lit = sentiments["literal"][i]
            if is_prefix:
                if lit.startswith(word):
                    pos_scores.append(sentiments["pos_score"][i])
                    neg_scores.append(sentiments["neg_score"][i])
            else:
                if word == lit:
                    pos_scores.append(sentiments["pos_score"][i])
                    neg_scores.append(sentiments["neg_score"][i])

        if len(pos_scores) > 0:
            return sum(pos_scores) / len(pos_scores), sum(neg_scores) / len(neg_scores)
        else:
            return -1, -1

    def get_score_for_english_word(self, lemma, wn_tag):
        """
        Function for calculating positive and negative score for english word
        :param lemma: input lemma for word
        :param wn_tag: tag from wordnet
        :return: positive and negative score
        """
        pos_scores = []
        neg_scores = []
        for i in range(len(self._wnen_data["tag"])):
            tag = self._wnen_data["tag"][i]
            literals = self._wnen_data["literals"][i]

            for lit in literals:
                if lit == lemma and tag == wn_tag:
                    pos, neg = self._wnen_data["score"][i]
                    pos_scores.append(pos)
                    neg_scores.append(neg)

        if len(pos_scores) > 0:
            return sum(pos_scores) / len(pos_scores), sum(neg_scores) / len(neg_scores)
        else:
            return -1, -1
