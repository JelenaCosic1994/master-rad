from pathlib import Path
import csv
import os
import chardet
import pandas as pd
import src.util.constants as const


def load_text_from_txt_file(file_path):
    filename = Path(file_path)
    encoding = find_encoding(filename)
    f = open(filename, encoding=encoding)
    data = f.read()
    f.close()
    return data.rstrip()


def find_encoding(file_path):
    filename = Path(file_path)
    f = open(filename, "rb")
    raw_data = f.read()
    result = chardet.detect(raw_data)
    char_enc = result['encoding']
    f.close()
    return char_enc


def get_all_txt_file_paths_from_dir(dir_path):
    file_paths = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir_path):
        for file in f:
            if '.txt' in file:
                file_paths.append(os.path.join(r, file))
    return file_paths


def load_english_corpus_from_dir(dir_path):
    all_english_file_paths = get_all_txt_file_paths_from_dir(dir_path)
    english_corpus = []
    for file_path in all_english_file_paths:
        text = load_text_from_txt_file(file_path)
        if 'pos' in file_path:
            english_corpus.append((text, const.POSITIVE))
        if 'neg' in file_path:
            english_corpus.append((text, const.NEGATIVE))
    return english_corpus


def load_serbian_corpus_from_csv_file(file_path):
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
    file_paths = get_all_txt_file_paths_from_dir(dir_path)
    data = ""
    for file_path in file_paths:
        s = load_text_from_txt_file(file_path)
        data += s
        data += "\n"
    return set(data.split())


def load_xlsx_file(file_path):
    xl = pd.ExcelFile(file_path)
    data_frame = xl.parse('Sheet1')
    return data_frame
