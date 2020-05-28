from pathlib import Path
import csv
import os
import chardet
import pandas as pd
import src.util.constants as const
import re


def load_text_from_txt_file(file_path):
    """
    Function for read data from .txt file
    :param file_path: path to the read file
    :return: string
    """
    filename = Path(file_path)
    encoding = find_encoding(filename)
    f = open(filename, encoding=encoding)
    data = f.read()
    f.close()
    return data.rstrip()


def find_encoding(file_path):
    """
    Function for find encoding for file
    :param file_path: path to the file
    :return: encoding
    """
    filename = Path(file_path)
    f = open(filename, "rb")
    raw_data = f.read()
    result = chardet.detect(raw_data)
    char_enc = result['encoding']
    f.close()
    return char_enc


def get_all_txt_file_paths_from_dir(dir_path):
    """
    Function for get all .txt files found in directory
    :param dir_path: path to the directory
    :return: list of .txt file paths
    """
    file_paths = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir_path):
        for file in f:
            if '.txt' in file:
                file_paths.append(os.path.join(r, file))
    return file_paths


def load_english_corpus(dir_path):
    """
    Function for loading english corpus
    :param dir_path: path to the directory where is english corpus
    :return: list of tuple(text, rating) - text: string which represents one film review,
             rating: constant which represents a rating of film review (POSITIVE or NEGATIVE)
    """
    all_english_file_paths = get_all_txt_file_paths_from_dir(dir_path)
    english_corpus = []
    for file_path in all_english_file_paths:
        text = load_text_from_txt_file(file_path)
        if 'pos' in file_path:
            english_corpus.append((text, const.POSITIVE))
        if 'neg' in file_path:
            english_corpus.append((text, const.NEGATIVE))
    return english_corpus


def load_serbian_corpus(file_path):
    """
    Function for loading serbian corpus
    :param file_path: path to the .csv file where is serbian corpus
    :return: list of tuple(text, rating) - text: string which represents one film review,
             rating: constant which represents a rating of film review (POSITIVE, NEGATIVE or NEUTRAL)
    """
    serbian_corpus = []
    with open(file_path, encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row_passed = False
        for row in csv_reader:
            if not first_row_passed:
                first_row_passed = True
                continue
            serbian_corpus.append((row[0], row[1]))
    return serbian_corpus


def load_stop_words(dir_path):
    """
    Function for loading stop words for serbian language
    :param dir_path: path to the directory where are serbian stop words, there are two files
    :return: set of all stop words
    """
    file_paths = get_all_txt_file_paths_from_dir(dir_path)
    data = ""
    for file_path in file_paths:
        s = load_text_from_txt_file(file_path)
        data += s
        data += "\n"
    return set(data.split())


def load_xlsx_file(file_path, sheet_number):
    """
    Function for loading first sheet in some xlsx file
    :param file_path: path to the xlsx file
    :param sheet_number: number of sheet in file
    :return: data frame with all data
    """
    xl = pd.ExcelFile(file_path)
    data_frame = xl.parse('Sheet' + str(sheet_number))
    return data_frame


def load_text_dictionary(ordinary, dir_path, three_classes):
    """
    Function for load serbian dictionary
    :param ordinary: ordinal number of text
    :param dir_path: path to the dictionary
    :param three_classes: if corpus contains three - true, otherwise - false
    :return:
    """

    if three_classes:
        # if corpus have 3 classes: positive, negative and neutral
        if 1 <= ordinary <= 841:
            class_tag = "pos"
        elif 842 <= ordinary <= 1682:
            class_tag = "neutr"
        else:
            class_tag = "neg"
    else:
        # if corpus have 2 classes: positive and negative
        if 1 <= ordinary <= 841:
            class_tag = "pos"
        else:
            class_tag = "neg"

    text_number = ordinary % 841
    if text_number == 0:
        text_number = 841

    # filename is in format number_pos.tt or number_neg.tt or number_neutr.tt
    filename = str(text_number) + "_" + class_tag + ".tt"

    data = []
    for r, d, f in os.walk(dir_path):
        for file in f:
            if filename == file:
                path = os.path.join(r, file)
                file = open(path, 'r', encoding='utf-8')

                lines = file.readlines()
                for line in lines:
                    splits = re.split(r'\s', line)
                    if len(splits) != 4:
                        continue
                    word = splits[0]
                    tag = splits[1]
                    lemma = splits[2]
                    data.append((word, tag, lemma))
                file.close()
    return data, filename
