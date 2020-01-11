import src.util.loader as loader
from src.util.wordnet_helper import WordNetHelper
import os

if __name__ == '__main__':

    # load serbian stop words
    serbian_stop_words = loader.load_stop_words(".." + os.sep + "input_data" + os.sep + "StopWords")
    # load english WordNet
    english_wordnet = loader.load_xlsx_file(".." + os.sep + "input_data" + os.sep + "wnen.xlsx")
    # load Serbian corpus - 2 classes
    serbian_corpus_2_classes = loader.load_serbian_corpus(".." + os.sep + "input_data" + os.sep + "serb-all-2.csv")
    # load english corpus - 2 classes
    english_corpus = loader.load_english_corpus(".." + os.sep + "input_data" + os.sep + "txt_sentoken - all items")

    wordnet_helper = WordNetHelper(english_wordnet, ".." + os.sep + "input_data" + os.sep + "wnsrp.xml", serbian_stop_words)

    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(english_corpus, True)
    result_file_english = open(".." + os.sep + "output_data" + os.sep + "english_corpus" + os.sep + "result.txt", "w", encoding='utf8')

    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_english.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_english.close()

    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False)
    result_file_serbian = open(".." + os.sep + "output_data" + os.sep + "serbian_corpus" + os.sep + "result.txt", "w", encoding='utf8')

    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_serbian.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_serbian.close()

