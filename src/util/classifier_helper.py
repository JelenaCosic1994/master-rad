import src.util.converter as converter
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report


def create_model(wordnet_helper, corpus, is_english):
    """
    Create model
    :param wordnet_helper: instance of wordnet helper
    :param corpus: given corpus
    :param is_english: True is language is english, False otherwise
    :return: model
    """
    vocabulary = {}
    id = 0
    y_data = []
    data = []   # array for all texts which element is list which element is tuple(id, diff) for word in text
    i = 1
    for t, rating in corpus:
        y_data.append(rating)
        word_list = []

        if is_english:
            text = converter.remove_punctuation(t)
            clean_text = wordnet_helper.clear_english_text(text)
            for lemma, wn_tag in clean_text:
                pos, neg = wordnet_helper.get_pos_neg_score_for_english_word(lemma, wn_tag)
                diff = pos - neg
                if lemma not in vocabulary:
                    vocabulary[lemma] = (id, diff)
                    id += 1
                word_list.append(vocabulary[lemma])

            data.append(word_list)
        else:
            clean_text = wordnet_helper.clear_serbian_text(i)
            for word in clean_text:
                pos, neg = wordnet_helper.get_pos_neg_score_for_serbian_word(word)
                diff = pos - neg
                if word not in vocabulary:
                    vocabulary[word] = (id, diff)
                    id += 1
                word_list.append(vocabulary[word])

            data.append(word_list)
        i += 1
    x_data = create_sparse_matrix(data, vocabulary)
    # delete data from memory
    del data
    del vocabulary

    return x_data, y_data


def create_sparse_matrix(data, vocabulary):
    """
    Crete sparse matrix for training and testing
    :param data: data for create x_data
    :param vocabulary: given vocabulary
    :return: x_data for training
    """
    m = len(data)
    n = len(vocabulary)
    sparse_matrix = np.zeros((m, n), dtype='f')

    for i in range(m):
        for j in range(n):
            for id, diff in data[i]:
                if id == j:
                    sparse_matrix[i][j] = sparse_matrix[i][j] + diff
    return sparse_matrix


def svm_classifier(wordnet_helper, corpus, is_english):
    """
    Implementation of svm classifier
    :param wordnet_helper: instance of wordnet helper
    :param corpus: given corpus
    :param is_english: True is language is english, False otherwise
    :return: classification report
    """
    # Create model for  corpus
    x_data, y_data = create_model(wordnet_helper, corpus, is_english)
    X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.20)

    # Classification
    svclassifier = SVC(kernel='linear')
    svclassifier.fit(X_train, y_train)
    y_pred = svclassifier.predict(X_test)

    return classification_report(y_test, y_pred)
