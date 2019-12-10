import src.util.loader as loader
from src.util.parser import Parser
from src.entity.text import Text
from src.util.wordnet_helper import WordNetHelper
import src.util.constants as const

if __name__ == '__main__':

    # load stop words
    stop_words = loader.load_stop_words("..\\input_data\\StopWords")
    # load english WordNet
    data_frame_wnen = loader.load_xlsx_file("..\\input_data\\wnen.xlsx")
    # load Serbian corpus
    # serbian_corpus = loader.load_serbian_corpus_from_csv_file("..\\input_data\\SerbMR-3C - 5.csv")
    # load english corpus
    english_corpus = loader.load_english_corpus_from_dir("..\\input_data\\txt_sentoken_100")

    wordnet_helper = WordNetHelper(data_frame_wnen, "..\\input_data\\wnsrp.xml")
    parser = Parser(stop_words)

    def set_pos_neg_score_for_document(text, is_serbian):
        pos_sum = 0
        neg_sum = 0
        count = 0
        for sentence in text.get_sentences():
            parser.remove_stop_words_from_sentence(sentence, is_serbian)
            parser.lemmatization_and_stemming_serbian_sentence(sentence) if is_serbian else parser.lemmatization_and_stemming_english_sentence(sentence)
            wordnet_helper.set_pos_neg_score_for_sentence(sentence, is_serbian)
            p = sentence.get_pos_score()
            n = sentence.get_neg_score()
            if p != n:
                pos_sum += p
                neg_sum += n
                count += 1

        pos, neg = (pos_sum / count, neg_sum / count) if count != 0 else (0, 0)
        text.set_pos_score(pos)
        text.set_neg_score(neg)


    def set_rating_to_document(text):
        pos = text.get_pos_score()
        neg = text.get_neg_score()
        odst = 0.0001
        # if abs(pos - neg) <= odst:
        #     text.set_rating(const.NEUTRAL)
        # if pos - neg > odst:
        #     text.set_rating(const.POSITIVE)
        # if neg - pos > odst:
        #     text.set_rating(const.NEGATIVE)
        if pos > neg:
            text.set_rating(const.POSITIVE)
        else:
            text.set_rating(const.NEGATIVE)


    def get_percent_for_corpus(corpus, is_serbian):
        true_positive_p = 0
        true_positive_n = 0
        all_positive = 0
        all_negative = 0

        map_size = len(corpus)
        i = 1

        for review, rating in corpus:
            print(i)
            i += 1

            text = Text(review, is_serbian)
            set_pos_neg_score_for_document(text, is_serbian)
            set_rating_to_document(text)

            if text.get_rating() == const.POSITIVE:
                all_positive += 1
            if text.get_rating() == const.NEGATIVE:
                all_negative += 1

            if text.get_rating() == rating:
                if rating == const.POSITIVE:
                    true_positive_p += 1
                if rating == const.NEGATIVE:
                    true_positive_n += 1

        return true_positive_p/all_positive * 100, true_positive_n/all_negative * 100, 2*true_positive_p / map_size * 100, 2*true_positive_n / map_size * 100


    precision_p, precision_n, recall_p, recall_n = get_percent_for_corpus(english_corpus, False)
    print("Precision for positive: " + str(precision_p) + ", recall for positive: " + str(recall_p) + "\n")
    print("Precision for negative: " + str(precision_n) + ", recall for negative: " + str(recall_n) + "\n")
