import re, string
from transliterate import translit
from nltk.tokenize.punkt import PunktSentenceTokenizer


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


def split_text_to_sentences(text):
    tokenizer = PunktSentenceTokenizer()

    tokenizer._params.abbrev_types.add('mr')
    tokenizer._params.abbrev_types.add('dr')
    tokenizer._params.abbrev_types.add('td')
    tokenizer._params.abbrev_types.add('tj')

    text = text.replace('...', '.')
    text = text.replace('.)', ')')
    clean_sentences = tokenizer.tokenize(text)
    return clean_sentences


def remove_punctuation(text):
    replacer = str.maketrans(dict.fromkeys(string.punctuation))
    text_1 = text.translate(replacer)
    text_2 = re.sub(r'[^\w\s]', '', text_1)

    return text_2