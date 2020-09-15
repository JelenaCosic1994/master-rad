import re
import string
from transliterate import translit
from nltk.corpus import wordnet as wn


def is_cyrillic_text(text):
    """
    Function for recognizing cyrillic serbian text
    :param text: some string
    :return: True if text is in cyrillic serbian language or False otherwise
    """
    return bool(re.search('[а-шА-Ш]', text))


def convert_text_to_latinic(word):
    """
    Function for converting cyrillic serbian word to latinic serbian word
    :param word: string which represents cyrillic serbian word
    :return: string translated to latinic serbian word
    """
    return translit(word, 'sr', reversed=True)


def convert_from_float_to_string(num_float):
    """
    Function for converting float number to string and concatenating zeros in begin of string
    if string has lenght smaller than 8 characters
    :param num_float: floar number
    :return: string number
    """
    try:
        int_num = int(num_float)
        num_string = str(int_num)
        if len(num_string) < 8:
            n = 8 - len(num_string)
            num_string = '0'*n + num_string
        return num_string
    except:
        return -1


def convert_serbian_word_to_aurora(word):
    """
    Function for converting serbian word to aurora
    :param word: serbian word in latinic
    :return: serbian word in aurora
    """
    aurora_str = word
    aurora_str = aurora_str.replace("š", "sx")
    aurora_str = aurora_str.replace("č", "cx")
    aurora_str = aurora_str.replace("ć", "cy")
    aurora_str = aurora_str.replace("đ", "dx")
    aurora_str = aurora_str.replace("ž", "zx")
    aurora_str = aurora_str.replace("Š", "sx")
    aurora_str = aurora_str.replace("Č", "cx")
    aurora_str = aurora_str.replace("Ć", "cy")
    aurora_str = aurora_str.replace("Đ", "dx")
    aurora_str = aurora_str.replace("Ž", "zx")
    return aurora_str


def penn_to_wn(tag):
    """
    Function for convert between the PennTreebank tags to simple Wordnet tags
    :param tag: result of pos_tag method
    :return: Wordnet tag
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


"""
@author: Marija Radovic
"""


def remove_punctuation(text):
    """
    Function for remove punctuation in text
    :param text: string which represents some text
    :return: string without punctuation
    """
    replacer = str.maketrans(dict.fromkeys(string.punctuation))
    text_1 = text.translate(replacer)
    clean_text = re.sub(r'[^\w\s]', '', text_1)
    return clean_text
