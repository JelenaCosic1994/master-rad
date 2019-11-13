import src.parser.loader as loader
from src.parser.parser import Parser
import src.stemmer.stemmer as stemmer


if __name__ == '__main__':
    # Load stop words from directory
    stop_words = loader.load_stop_words("..\\input_data\\StopWords")

    # Load reviews lists from .csv files
    reviews_from_csv_2C = loader.load_text_list_from_csv_file("..\\input_data\\SerbMR-2C.csv")  # list of strings
    reviews_from_csv_3C = loader.load_text_list_from_csv_file("..\\input_data\\SerbMR-3C.csv")  # list of strings

    # Load txt file paths from directory
    #  TODO: remove absolute file path
    txt_file_paths_from_dir = loader.get_all_txt_file_paths_from_dir("C:\\Users\\jeca\\Desktop\\master_rad\\sentiment-text-analysis-using-lexical-resources\\input_data\\Collected_movie_reviews_in_Serbian")

    # Load reviews from txt files
    reviews_from_txt_files = []   # list of strings
    for file_path in txt_file_paths_from_dir:
        text = loader.load_text_from_txt_file(file_path)
        reviews_from_txt_files.append(text)

    # If text is cyrillic convert to latinic
    Parser.convert_list_of_strings_from_cyrillic_to_latinic(reviews_from_csv_2C)
    print("Done: convert list 1")
    Parser.convert_list_of_strings_from_cyrillic_to_latinic(reviews_from_csv_3C)
    print("Done: convert list 2")
    Parser.convert_list_of_strings_from_cyrillic_to_latinic(reviews_from_txt_files)
    print("Done: convert list 3")

    # Get texts without stop words - return value = list whose element is a list of words in text without stop words
    parser = Parser(stop_words)
    reviews_without_stop_words_1 = parser.get_texts_without_stop_words(reviews_from_csv_2C)
    print("Done: list 1 without stop words")
    reviews_without_stop_words_2 = parser.get_texts_without_stop_words(reviews_from_csv_3C)
    print("Done: list 2 without stop words")
    reviews_without_stop_words_3 = parser.get_texts_without_stop_words(reviews_from_txt_files)
    print("Done: list 3 without stop words")

    # Applying stemmer
    stem_text_words_1 = stemmer.stem_list_of_texts(reviews_without_stop_words_1)
    print("Done: stemmer on list 1")
    stem_text_words_2 = stemmer.stem_list_of_texts(reviews_without_stop_words_2)
    print("Done: stemmer on list 2")
    stem_text_words_3 = stemmer.stem_list_of_texts(reviews_without_stop_words_3)
    print("Done: stemmer on list 3")


