import re
from transliterate import translit


def is_cyrillic_text(text):
    return bool(re.search('[а-шА-Ш]', text))


def convert_word_to_latinic(word):
    """
    :param word: string
    :return: string translated to latinic
    """
    return translit(word, 'sr', reversed=True)


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


def convert_serbian_word_to_aurora(word):
	str = word
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
	return str