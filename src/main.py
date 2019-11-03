from src.parser.loader import Loader
from src.parser.parser import Parser


if __name__ == '__main__':
    # Load stop words from directory
    stop_words = Loader.load_stop_words("C:\\Users\\jeca\\Desktop\\master_rad\\sentiment-text-analysis-using-lexical-resources\\input_data\\StopWords")

    # Load reviews lists from .csv files
    reviews_from_csv_2C = Loader.load_text_list_from_csv_file("C:\\Users\\jeca\\Desktop\\master_rad\\SerbMR-2C.csv") # list of strings
    reviews_from_csv_3C = Loader.load_text_list_from_csv_file("C:\\Users\\jeca\\Desktop\\master_rad\\SerbMR-3C.csv") # list of strings

    # Load txt file paths from directory
    txt_file_paths_from_dir = Loader.get_all_txt_file_paths_from_dir("C:\\Users\\jeca\\Desktop\\master_rad\\Collected_movie_reviews_in_Serbian")

    # Load reviews from txt files
    reviews_from_txt_files = []   # list of strings
    for file_path in txt_file_paths_from_dir:
        text = Loader.load_text_from_txt_file(file_path)
        reviews_from_txt_files.append(text)

    # Get texts without stop words - return value = list whose element is a list of words in text without stop words
    parser = Parser(stop_words)
    reviews_without_stop_words_1 = parser.get_texts_without_stop_words(reviews_from_csv_2C)
    print("Done 1")
    reviews_without_stop_words_2 = parser.get_texts_without_stop_words(reviews_from_csv_3C)
    print("Done 2")
    reviews_without_stop_words_3 = parser.get_texts_without_stop_words(reviews_from_txt_files)
    print("Done 3")
