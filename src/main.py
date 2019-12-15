import src.util.loader as loader
from src.util.wordnet_helper import WordNetHelper
import src.util.constants as const
from nltk import word_tokenize
import src.util.converter as converter
import src.util.serbian_stemmer as serbian_stemmer


if __name__ == '__main__':

    # load stop words
    stop_words = loader.load_stop_words("..\\input_data\\StopWords")
    # load english WordNet
    data_frame_wnen = loader.load_xlsx_file("..\\input_data\\wnen.xlsx")
    # load Serbian corpus
    serbian_corpus = loader.load_serbian_corpus_from_csv_file("..\\input_data\\serb-5.csv")
    # load english corpus
    # english_corpus = loader.load_english_corpus_from_dir("..\\input_data\\txt_sentoken_100")

    wordnet_helper = WordNetHelper(data_frame_wnen, "..\\input_data\\wnsrp.xml")

    # print(wordnet_helper.create_data_frame())

def swn_polarity(text):
    raw_sentences = converter.split_text_to_sentences(text)
    count_sentences = 0
    pos_score_text = 0
    neg_score_text = 0

    for sentence in raw_sentences:
        pos_sum_sen = 0
        neg_sum_sen = 0
        count_words = 0
        for word in word_tokenize(sentence):
            word = word.lower().strip()
            # if is word in cyrillic convert to latinic
            if converter.is_cyrillic_text(word):
                word = converter.convert_word_to_latinic(word)

            # ignore stop words
            if word in stop_words:
                continue

            # stemming
            stem_word = serbian_stemmer.stem_str(word)

            # pos and neg score
            p, n = wordnet_helper.get_pos_neg_score_for_serbian_word(stem_word)
            if p != n:
                pos_sum_sen += p
                neg_sum_sen += n
                count_words += 1

        pos_avg_sentence, neg_avg_sentence = (pos_sum_sen / count_words, neg_sum_sen / count_words) if count_words != 0 else (0, 0)
        if pos_avg_sentence != neg_avg_sentence:
            pos_score_text += pos_avg_sentence
            neg_score_text += neg_avg_sentence
            count_sentences += 1

    pos_avg_text, neg_avg_text = (pos_score_text / count_sentences, neg_score_text / count_sentences) if count_sentences != 0 else (0, 0)
    if pos_avg_text > neg_avg_text:
        return 'POSITIVE'
    else:
        return 'NEGATIVE'


def calc_percent_for_corpus(english_corpus: list) -> tuple:
    """
    For given corpus calculate precision and recall for positive and negative reviews
    :param english_corpus:
    :return: tuple (precision_p, precision_n, recall_p, recall_n)
    """
    true_positive_p = 0
    true_positive_n = 0
    all_positive = 0
    all_negative = 0
    map_size = len(english_corpus)

    for text, rating in english_corpus:
        new_r = swn_polarity(text)

        if new_r == 'POSITIVE':
            all_positive += 1
        if new_r == 'NEGATIVE':
            all_negative += 1

        if new_r == rating:
            if rating == 'POSITIVE':
                true_positive_p += 1
            if rating == 'NEGATIVE':
                true_positive_n += 1

    return true_positive_p / all_positive * 100, true_positive_n / all_negative * 100, 2 * true_positive_p / map_size * 100, 2 * true_positive_n / map_size * 100


precision_p, precision_n, recall_p, recall_n = calc_percent_for_corpus(serbian_corpus)
print("Precision for positive: " + str(precision_p) + ", recall for positive: " + str(recall_p) + ", f measure: " + str(2 * (precision_p * recall_p) / (precision_p + recall_p)) + "\n")
print("Precision for negative: " + str(precision_n) + ", recall for negative: " + str(recall_n) + ", f measure: " + str(2 * (precision_n * recall_n) / (precision_n + recall_n)) + "\n")
