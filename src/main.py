import src.util.loader as loader
from src.util.wordnet_helper import WordNetHelper
from src.util.classifier_helper import svm_classifier
import os


if __name__ == '__main__':

    # load serbian stop words
    serbian_stop_words = loader.load_stop_words(".." + os.sep + "input_data" + os.sep + "StopWords")
    # load english WordNet
    english_wordnet = loader.load_xlsx_file(".." + os.sep + "input_data" + os.sep + "wnen.xlsx", 1)
    # load serbian WordNet - original items
    serbian_wordnet_original = loader.load_xlsx_file(".." + os.sep + "input_data" + os.sep + "sentiments_original.xlsx", 2)
    # load serbian WordNet - changed items
    serbian_wordnet_changed = loader.load_xlsx_file(".." + os.sep + "input_data" + os.sep + "sentiments_with_replaced_items.xlsx", 2)
    # load serbian WordNet - deleted items
    serbian_wordnet_deleted = loader.load_xlsx_file(".." + os.sep + "input_data" + os.sep + "sentiments_without_items.xlsx", 2)
    # load Serbian corpus - 2 classes
    serbian_corpus_2_classes = loader.load_serbian_corpus(".." + os.sep + "input_data" + os.sep + "serb-all-2.csv")
    # load Serbian corpus - 3 classes
    serbian_corpus_3_classes = loader.load_serbian_corpus(".." + os.sep + "input_data" + os.sep + "serb-all-3.csv")
    # load english corpus - 2 classes
    english_corpus = loader.load_english_corpus(".." + os.sep + "input_data" + os.sep + "txt_sentoken - all items")

    wordnet_helper = WordNetHelper(english_wordnet, serbian_wordnet_original, serbian_wordnet_changed, serbian_wordnet_deleted,
                                   serbian_stop_words, ".." + os.sep + "input_data" + os.sep + "dictionary")

    # English corpus - 2 classes
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(english_corpus, True, False)
    result_file_english = open(".." + os.sep + "output_data" + os.sep + "english_corpus" + os.sep + "result.txt", "w",
                               encoding='utf8')
    print("English corpus - 2 classes:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure) + " accuracy: " + str(accuracy))
    result_file_english.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))
    result_file_english.close()

    # Serbian corpus - 2 classes - original serbian wordnet
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False,
                                                                                     False, 'o', False)
    print("Serbian corpus - 2 classes - original serbian wordnet:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 2 classes - changed serbian wordnet
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False,
                                                                                     False, 'c', False)
    print("Serbian corpus - 2 classes - changed serbian wordnet:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 2 classes - deleted serbian wordnet
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False,
                                                                                     False, 'd', False)
    print("Serbian corpus - 2 classes - deleted serbian wordnet:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 2 classes - original serbian wordnet where word is prefix of literal
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False,
                                                                                     False, 'o', True)
    print("Serbian corpus - 2 classes - original serbian wordnet where word is prefix of literal:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 2 classes - changed serbian wordnet where word is prefix of literal
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False,
                                                                                     False, 'c', True)
    print("Serbian corpus - 2 classes - changed serbian wordnet where word is prefix of literal:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 2 classes - deleted serbian wordnet where word is prefix of literal
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_2_classes, False,
                                                                                     False, 'd', True)
    print("Serbian corpus - 2 classes - deleted serbian wordnet where word is prefix of literal:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 3 classes - original serbian wordnet
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_3_classes, False,
                                                                                     True, 'o', False, 0.05)
    print("Serbian corpus - 3 classes - original serbian wordnet:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 3 classes - changed serbian wordnet
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_3_classes, False,
                                                                                     True, 'c', False, 0.05)
    print("Serbian corpus - 3 classes - changed serbian wordnet:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 3 classes - deleted serbian wordnet
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_3_classes, False,
                                                                                     True, 'd', False, 0.05)
    print("Serbian corpus - 3 classes - deleted serbian wordnet:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 3 classes - original serbian wordnet where word is prefix of literal
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_3_classes, False,
                                                                                     True, 'o', True, 0.02)
    print("Serbian corpus - 3 classes - original serbian wordnet where word is prefix of literal:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 3 classes - changed serbian wordnet where word is prefix of literal
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_3_classes, False,
                                                                                     True, 'c', True, 0.02)
    print("Serbian corpus - 3 classes - changed serbian wordnet where word is prefix of literal:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # Serbian corpus - 3 classes - deleted serbian wordnet where word is prefix of literal
    precision, recall, f_measure, accuracy = wordnet_helper.calc_percents_for_corpus(serbian_corpus_3_classes, False,
                                                                                     True, 'd', True, 0.02)
    print("Serbian corpus - 3 classes - deleted serbian wordnet where word is prefix of literal:\n")
    print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(
        f_measure) + " accuracy: " + str(accuracy))

    # ------SVM---------

    # English corpus - 2 classes - svm classifier
    classification_report = svm_classifier(wordnet_helper, english_corpus, True, 0.20)
    print("SVM classifier - english corpus: \n" + classification_report)

    # Serbian corpus - 2 classes - svm classifier - original serbian wordnet
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_2_classes, False, 0.20, False, 'o', False)
    print("SVM classifier - serbian corpus - 2 classes - original serbian wordnet: \n" + classification_report)

    # Serbian corpus - 2 classes - svm classifier - changed serbian wordnet
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_2_classes, False, 0.20, False, 'c', False)
    print("SVM classifier - serbian corpus - 2 classes - changed serbian wordnet: \n" + classification_report)

    # Serbian corpus - 2 classes - svm classifier - deleted serbian wordnet
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_2_classes, False, 0.20, False, 'd', False)
    print("SVM classifier - serbian corpus - 2 classes - deleted serbian wordnet: \n" + classification_report)

    # Serbian corpus - 2 classes - svm classifier - original serbian wordnet where word is prefix of literal
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_2_classes, False, 0.20, False, 'o', True)
    print(
        "SVM classifier - serbian corpus - 2 classes - original serbian wordnet where word is prefix of literal: \n" + classification_report)

    # Serbian corpus - 2 classes - svm classifier - changed serbian wordnet where word is prefix of literal
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_2_classes, False, 0.20, False, 'c', True)
    print(
        "SVM classifier - serbian corpus - 2 classes - changed serbian wordnet where word is prefix of literal: \n" + classification_report)

    # Serbian corpus - 2 classes - svm classifier - deleted serbian wordnet where word is prefix of literal
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_2_classes, False, 0.20, False, 'd', True)
    print(
        "SVM classifier - serbian corpus - 2 classes - deleted serbian wordnet where word is prefix of literal: \n" + classification_report)

    # Serbian corpus - 3 classes - svm classifier - original serbian wordnet
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_3_classes, False, 0.20, True, 'o', False)
    print("SVM classifier - serbian corpus - 3 classes - original serbian wordnet: \n" + classification_report)

    # Serbian corpus - 3 classes - svm classifier - changed serbian wordnet
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_3_classes, False, 0.20, True, 'c', False)
    print("SVM classifier - serbian corpus - 3 classes - changed serbian wordnet: \n" + classification_report)

    # Serbian corpus - 3 classes - svm classifier - deleted serbian wordnet
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_3_classes, False, 0.20, True, 'd', False)
    print("SVM classifier - serbian corpus - 3 classes - deleted serbian wordnet: \n" + classification_report)

    # Serbian corpus - 3 classes - svm classifier - original serbian wordnet where word is prefix of literal
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_3_classes, False, 0.20, True, 'o', True)
    print(
        "SVM classifier - serbian corpus - 3 classes - original serbian wordnet where word is prefix of literal: \n" + classification_report)
    #
    # Serbian corpus - 3 classes - svm classifier - original serbian wordnet where word is prefix of literal
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_3_classes, False, 0.20, True, 'c', True)
    print(
        "SVM classifier - serbian corpus - 3 classes - changed serbian wordnet where word is prefix of literal: \n" + classification_report)

    # Serbian corpus - 3 classes - svm classifier - original serbian wordnet where word is prefix of literal
    classification_report = svm_classifier(wordnet_helper, serbian_corpus_3_classes, False, 0.20, True, 'd', True)
    print(
        "SVM classifier - serbian corpus - 3 classes - deleted serbian wordnet where word is prefix of literal: \n" + classification_report)
