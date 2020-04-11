import src.util.loader as loader
from src.util.wordnet_helper import WordNetHelper
from src.util.classifier_helper import svm_classifier
import os


if __name__ == '__main__':

    # load serbian stop words
    serbian_stop_words = loader.load_stop_words(".." + os.sep + "input_data" + os.sep + "StopWords")
    # load english WordNet
    english_wordnet = loader.load_xlsx_file(".." + os.sep + "input_data" + os.sep + "wnen.xlsx")
    # load Serbian corpus - 2 classes
    serbian_corpus_2_classes = loader.load_serbian_corpus(".." + os.sep + "input_data" + os.sep + "serb-all-2.csv")
    # load Serbian corpus - 3 classes
    serbian_corpus_3_classes = loader.load_serbian_corpus(".." + os.sep + "input_data" + os.sep + "serb-all-3.csv")
    # load english corpus - 2 classes
    english_corpus = loader.load_english_corpus(".." + os.sep + "input_data" + os.sep + "txt_sentoken - all items")

    wordnet_helper = WordNetHelper(english_wordnet, ".." + os.sep + "input_data" + os.sep + "wnsrp.xml", serbian_stop_words, ".." + os.sep + "input_data" + os.sep + "dictionary")

    # English corpus - 2 classes
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(english_corpus, True, False)
    result_file_english = open(".." + os.sep + "output_data" + os.sep + "english_corpus" + os.sep + "result.txt", "w", encoding='utf8')
    print("English corpus - 2 classes:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_english.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_english.close()

    # Serbian corpus - 2 classes
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False, False)
    result_file_serbian2 = open(".." + os.sep + "output_data" + os.sep + "serbian_corpus_3" + os.sep + "result2.txt", "w", encoding='utf8')
    print("Serbian corpus - 2 classes:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_serbian2.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_serbian2.close()

    # Serbian corpus - 3 classes
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_3_classes, False, True)
    result_file_serbian3 = open(".." + os.sep + "output_data" + os.sep + "serbian_corpus_3" + os.sep + "result3.txt", "w", encoding='utf8')
    print("Serbian corpus - 3 classes:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_serbian3.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_serbian3.close()

    # English corpus - 2 classes - svm classifier
    classification_report = svm_classifier(wordnet_helper, english_corpus, True)
    print("SVM classifier - english corpus: \n" + classification_report)
    result_svm_english = open(".." + os.sep + "output_data" + os.sep + "result_svm_english.txt", "w", encoding='utf8')
    result_svm_english.write(classification_report)
    result_svm_english.close()

    # Serbian corpus - 2 classes - svm classifier
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_2_classes, False)
    print("SVM classifier - serbian corpus - 2 classes: \n" + classification_report)
    result_svm_serbian2 = open(".." + os.sep + "output_data" + os.sep + "result_svm_serbian2.txt", "w", encoding='utf8')
    result_svm_serbian2.write(classification_report)
    result_svm_serbian2.close()

    # Serbian corpus - 3 classes - svm classifier
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_3_classes, False)
    print("SVM classifier - serbian corpus - 3 classes: \n" + classification_report)
    result_svm_serbian3 = open(".." + os.sep + "output_data" + os.sep + "result_svm_serbian3.txt", "w", encoding='utf8')
    result_svm_serbian3.write(classification_report)
    result_svm_serbian3.close()
