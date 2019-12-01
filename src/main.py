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
    reviews_from_csv_3C = loader.load_text_list_from_csv_file("..\\input_data\\SerbMR-3C.csv")  # list of strings

    wordnet_helper = WordNetHelper(data_frame_wnen, "..\\input_data\\wnsrp.xml")
    parser = Parser(stop_words)

    def set_pos_neg_score_for_document(text):
        pos_sum = 0
        neg_sum = 0
        n = len(text.get_sentences())
        for sentence in text.get_sentences():
            if converter.is_cyrillic_text(str(sentence)):
                converter.convert_sentence_to_latinic(sentence)
            parser.remove_stop_words_from_sentence(sentence)
            parser.lemmatization_and_stemming_sentence(sentence)
            wordnet_helper.set_pos_neg_score_for_sentence_from_english_wordnet(sentence)
            pos_sum += sentence.get_pos_score()
            neg_sum += sentence.get_neg_score()
        pos, neg = (pos_sum / n, neg_sum / n) if n != 0 else (0, 0)
        text.set_pos_score(pos)
        text.set_neg_score(neg)

    # print rating
    for review in reviews_from_csv_3C:
        text = Text(review)
        set_pos_neg_score_for_document(text)
        print("Rating document - pos:", text.get_pos_score(), " , neg:", text.get_neg_score())

