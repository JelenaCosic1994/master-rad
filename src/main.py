import src.util.loader as loader
from src.util.parser import Parser
from src.entity.text import Text
from src.util.wordnet_helper import WordNetHelper
import src.util.converter as converter
import src.util.constants as const

if __name__ == '__main__':

    # load stop words
    stop_words = loader.load_stop_words("..\\input_data\\StopWords")
    # load english WordNet
    data_frame_wnen = loader.load_xlsx_file("..\\input_data\\wnen.xlsx")
    # load Serbian corpus
    serbian_corpus = loader.load_serbian_corpus_from_csv_file("..\\input_data\\SerbMR-3C.csv")  # map
    # load english corpus
    all_english_file_paths = loader.get_all_txt_file_paths_from_dir("..\\input_data\\txt_sentoken")
    english_corpus = {}    # map
    for file_path in all_english_file_paths:
        text = loader.load_text_from_txt_file(file_path)
        if 'pos' in file_path:
            english_corpus[text] = const.POSITIVE
        if 'neg' in file_path:
            english_corpus[text] = const.NEGATIVE

    wordnet_helper = WordNetHelper(data_frame_wnen, "..\\input_data\\wnsrp.xml")
    parser = Parser(stop_words)

    def set_pos_neg_score_for_document(text, is_serbian):
        pos_sum = 0
        neg_sum = 0
        n = len(text.get_sentences())
        for sentence in text.get_sentences():
            if is_serbian and converter.is_cyrillic_text(str(sentence)):
                converter.convert_sentence_to_latinic(sentence)
            parser.remove_stop_words_from_sentence(sentence, is_serbian)
            parser.lemmatization_and_stemming_serbian_sentence(sentence) if is_serbian else parser.lemmatization_and_stemming_english_sentence(sentence)
            wordnet_helper.set_pos_neg_score_for_sentence(sentence, is_serbian)

            pos_sum += sentence.get_pos_score()
            neg_sum += sentence.get_neg_score()

        pos, neg = (pos_sum / n, neg_sum / n) if n != 0 else (0, 0)
        text.set_pos_score(pos)
        text.set_neg_score(neg)

    def set_rating_to_document(text):
        pos = text.get_pos_score()
        neg = text.get_neg_score()
        odst = 0.0001
        if abs(pos - neg) <= odst:
            text.set_rating(const.NEUTRAL)
        if pos - neg > odst:
            text.set_rating(const.POSITIVE)
        if neg - pos > odst:
            text.set_rating(const.NEGATIVE)


    def get_percent_for_corpus(corpus, is_serbian):  # corpus is a map
        counter = 0
        map_size = len(corpus)

        for review in corpus.keys():
            text = Text(review)
            rating = corpus[review]

            set_pos_neg_score_for_document(text, is_serbian)
            set_rating_to_document(text)

            if text.get_rating() == rating:
                counter += 1

        return counter / map_size * 100


    percent_serbian_corpus = get_percent_for_corpus(serbian_corpus, True)
    print(percent_serbian_corpus)
    # percent_english_corpus = get_percent_for_corpus(english_corpus, False)
    # print(percent_english_corpus)

# from src.util.serbian_stemmer import stem_str
# from src.util.serbian_stemmer import stem_arr
# print(stem_str("Film 'Kum' mi se uopšte ne dopada. Užasno mi je dosadan, dug i nezanimljiv!"))
# print(stem_arr("Film 'Kum' mi se uopšte ne dopada. Užasno mi je dosadan, dug i nezanimljiv!"))
