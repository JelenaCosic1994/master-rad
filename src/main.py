import src.util.loader as loader
from src.util.parser import Parser
from src.entity.text import Text
from src.util.wordnet_helper import WordNetHelper
import src.util.converter as converter

if __name__ == '__main__':

    # load stop words
    stop_words = loader.load_stop_words("..\\input_data\\StopWords")
    # load english WordNet
    data_frame_wnen = loader.load_xlsx_file("..\\input_data\\wnen.xlsx")
    # load Serbian corpus
    serbian_reviews = loader.load_text_list_from_csv_file("..\\input_data\\SerbMR-3C.csv")  # list of strings
    # load english corpus
    all_english_file_paths = loader.get_all_txt_file_paths_from_dir("..\\input_data\\txt_sentoken")
    english_reviews = []   # list of strings
    for file_path in all_english_file_paths:
        text = loader.load_text_from_txt_file(file_path)
        english_reviews.append(text)

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

    # print rating - serbian corpus
    for review in serbian_reviews:
        text = Text(review)
        set_pos_neg_score_for_document(text, True)
        print("Rating document - pos:", text.get_pos_score(), " , neg:", text.get_neg_score())

    # print rating - english corpus
    for review in english_reviews:
        text = Text(review)
        set_pos_neg_score_for_document(text, False)
        print("Rating document - pos:", text.get_pos_score(), " , neg:", text.get_neg_score())

