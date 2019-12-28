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
    serbian_corpus = loader.load_serbian_corpus_from_csv_file("..\\input_data\\serb-all-2.csv")

    wordnet_helper = WordNetHelper(data_frame_wnen, "..\\input_data\\wnsrp.xml")


    def swn_polarity(text, file):
        raw_sentences = converter.split_text_to_sentences(text)
        count_sentences = 0
        pos_score_text = 0
        neg_score_text = 0

        for sentence in raw_sentences:
            pos_sum_sen = 0
            neg_sum_sen = 0
            count_words = 0
            for w in word_tokenize(sentence):
                # convert word to lowercase and delete spaces
                word = w.lower().strip()

                # if is word in cyrillic convert to latinic
                if converter.is_cyrillic_text(word):
                    word = converter.convert_word_to_latinic(word)

                # ignore stop words
                if word in stop_words:
                    continue

                # stemming
                stem_word = serbian_stemmer.stem_str(word)

                file.write("WORD " + word + "\t")
                file.write("STEM WORD: " + stem_word + "\n")
                # pos and neg score from english wordnet
                p, n = wordnet_helper.get_pos_neg_score_for_serbian_word(stem_word.strip(), file)

                if p != n or p != 0:
                    pos_sum_sen += p
                    neg_sum_sen += n
                    count_words += 1

            pos_avg_sentence, neg_avg_sentence = (pos_sum_sen / count_words, neg_sum_sen / count_words) if count_words != 0 else (0, 0)
            if pos_avg_sentence != neg_avg_sentence or pos_avg_sentence != 0:
                pos_score_text += pos_avg_sentence
                neg_score_text += neg_avg_sentence
                count_sentences += 1

        pos_avg_text, neg_avg_text = (pos_score_text / count_sentences, neg_score_text / count_sentences) if count_sentences != 0 else (0, 0)
        if pos_avg_text > neg_avg_text:
            return const.POSITIVE
        else:
            return const.NEGATIVE


    def calc_percent_for_corpus(serbian_corpus: list) -> tuple:
        """
        For given corpus calculate tp,tn,fp,fn
        :param english_corpus:
        :return:
        """
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        i = 1
        for t, rating in serbian_corpus:
            text = converter.remove_punctuation(t)
            file = open("..\\output_data\\serbian_corpus\\" + str(i) + "_" + rating + ".txt", "w", encoding='utf8')
            i += 1

            new_r = swn_polarity(text, file)
            file.write("\nNew Rating: " + new_r)
            file.close()

            if rating == const.POSITIVE:
                if new_r == const.POSITIVE:
                    tp += 1
                if new_r == const.NEGATIVE:
                    fn += 1
            if rating == const.NEGATIVE:
                if new_r == const.POSITIVE:
                    fp += 1
                if new_r == const.NEGATIVE:
                    tn += 1

        return tp, tn, fp, fn

    tp, tn, fp, fn = calc_percent_for_corpus(serbian_corpus)
    precision = tp / (tp + fp) * 100
    recall = tp / (tp + fn) * 100
    f_measure = 2*precision*recall/(precision + recall)

    precision_recall_file = open("..\\output_data\\serbian_corpus\\precision_recall.txt", "w", encoding='utf8')
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure))
    precision_recall_file.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure))
    precision_recall_file.close()
