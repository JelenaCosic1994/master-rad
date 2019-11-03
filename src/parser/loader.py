from pathlib import Path
import csv
import os
import chardet


class Loader:

    @staticmethod
    def load_text_from_txt_file(file_path):
        filename = Path(file_path)
        encoding = Loader.find_encoding(filename)
        f = open(filename, encoding=encoding)
        data = f.read()
        f.close()
        return data.rstrip()

    @staticmethod
    def find_encoding(file_path):
        filename = Path(file_path)
        f = open(filename, "rb")
        raw_data = f.read()
        result = chardet.detect(raw_data)
        char_enc = result['encoding']
        f.close()
        return char_enc

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
        with open(file_path, encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row_passed = False
            for row in csv_reader:
                if not first_row_passed:
                    first_row_passed = True
                    continue
                text_list.append(row[0])
        return text_list

    @staticmethod
    def load_stop_words(dir_path):
        file_paths = Loader.get_all_txt_file_paths_from_dir(dir_path)
        data = ""
        for file_path in file_paths:
            s = Loader.load_text_from_txt_file(file_path)
            data += s
            data += "\n"
        return set(data.split())
