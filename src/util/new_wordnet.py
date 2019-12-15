from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag
import src.util.loader as loader

lemmatizer = WordNetLemmatizer()


def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
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


def swn_polarity(text: str) -> str:
    """
    Return a sentiment polarity: negative or positive for given text
    :param text: string which represent text
    """

    raw_sentences = sent_tokenize(text)
    count_sentences = 0
    pos_score_text = 0
    neg_score_text = 0
    for raw_sentence in raw_sentences:
        tagged_sentence = pos_tag(word_tokenize(raw_sentence))

        count_words = 0
        pos_score_sentence = 0
        neg_score_sentence = 0
        for word, tag in tagged_sentence:

            wn_tag = penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue

            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue

            swn_synset = swn.senti_synset(synsets[0].name())
            pos = swn_synset.pos_score()
            neg = swn_synset.neg_score()
            if pos != neg:
                pos_score_sentence += pos
                neg_score_sentence += neg
                count_words += 1

        pos_avg_sentence, neg_avg_sentence = (pos_score_sentence / count_words, neg_score_sentence / count_words) if count_words != 0 else (0, 0)
        if pos_avg_sentence != neg_avg_sentence:
            pos_score_text += pos_avg_sentence
            neg_score_text += neg_avg_sentence
            count_sentences += 1

    pos_avg_text, neg_avg_text = (pos_score_text / count_sentences, neg_score_text / count_sentences) if count_sentences != 0 else (0, 0)
    if pos_avg_text > neg_avg_text:
        return 'POSITIVE'
    else:
        return 'NEGATIVE'


def calc_percent_for_corpus(english_corpus: list) -> tuple:
    """
    For given corpus calculate precision and recall for positive and negative reviews
    :param english_corpus: 
    :return: tuple (precision_p, precision_n, recall_p, recall_n)
    """
    true_positive_p = 0
    true_positive_n = 0
    all_positive = 0
    all_negative = 0
    map_size = len(english_corpus)

    for text, rating in english_corpus:
        new_r = swn_polarity(text)

        if new_r == 'POSITIVE':
            all_positive += 1
        if new_r == 'NEGATIVE':
            all_negative += 1

        if new_r == rating:
            if rating == 'POSITIVE':
                true_positive_p += 1
            if rating == 'NEGATIVE':
                true_positive_n += 1

    return true_positive_p/all_positive * 100, true_positive_n/all_negative * 100, 2*true_positive_p / map_size * 100, 2*true_positive_n / map_size * 100


english_corpus = loader.load_english_corpus_from_dir("..\\..\\input_data\\txt_sentoken - all items")
precision_p, precision_n, recall_p, recall_n = calc_percent_for_corpus(english_corpus)
print("Precision for positive: " + str(precision_p) + ", recall for positive: " + str(recall_p) + ", f measure: " + str( 2*(precision_p*recall_p)/(precision_p + recall_p)) + "\n")
print("Precision for negative: " + str(precision_n) + ", recall for negative: " + str(recall_n) + ", f measure: " + str( 2*(precision_n*recall_n)/(precision_n + recall_n)) + "\n")
