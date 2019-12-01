import re
from src.entity.word import Word
from transliterate import translit


def is_cyrillic_text(text):
    return bool(re.search('[а-шА-Ш]', text))


def convert_sentence_to_latinic(sentence):
    words = sentence.get_words()
    result_words = []
    for word in words:
        word = Word(translit(word.get_data(), 'sr', reversed=True))
        result_words.append(word)
    sentence.set_words(result_words)


def convert_from_float_to_string(num_float):
    try:
        int_num = int(num_float)
        num_string = str(int_num)
        if len(num_string) < 8:
            n = 8 - len(num_string)
            num_string = '0'*n + num_string
        return num_string
    except:
        return -1  # TODO check if this is correct


def convert_serbian_words_to_aurora(serbian_wn_map):
    for key in serbian_wn_map.keys():
        for i in range(len(serbian_wn_map[key])):
            str = serbian_wn_map[key][i]
            str = str.replace("š", "sx")
            str = str.replace("č", "cx")
            str = str.replace("ć", "cy")
            str = str.replace("đ", "dx")
            str = str.replace("ž", "zx")
            str = str.replace("Š", "sx")
            str = str.replace("Č", "cx")
            str = str.replace("Ć", "cy")
            str = str.replace("Đ", "dx")
            str = str.replace("Ž", "zx")
            serbian_wn_map[key][i] = str  # TODO check if it works without this line


