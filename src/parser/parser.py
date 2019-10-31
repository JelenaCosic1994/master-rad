import re
import nltk
from pathlib import Path
import csv
import os


class Parser:

    @staticmethod
    def get_words_from_sentence(sentence):
        return re.findall(r'\w+', sentence)

    @staticmethod
    def get_sentences_from_text(text):
        nltk.download('punkt')  # ovo je moralo prvi put da se pozove da se skine biblioteka
        return nltk.tokenize.sent_tokenize(text)

    @staticmethod
    def load_text_from_txt_file(file_path):
        filename = Path(file_path)
        f = open(filename, encoding="utf8")
        data = f.read()
        f.close()
        return data

    @staticmethod
    def get_all_txt_file_paths_from_dir(dir_path):
        file_paths = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(dir_path):
            for file in f:
                if '.txt' in file:
                    file_paths.append(os.path.join(r, file))
        return file_paths

    @staticmethod
    def load_text_list_from_csv_file(file_path):
        text_list = []
        with open(file_path, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                text_list.append(row[0])
                line_count += 1
        return text_list
