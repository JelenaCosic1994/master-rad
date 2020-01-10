from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
import src.util.loader as loader
import src.util.constants as const
import src.util.converter as converter

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def swn_polarity(text, file):
    """
    Function for calculating sentiment polarity: NEGATIVE or POSITIVE for given text
    :param text: string which represents text - film review
    :param file: file to write results
    :return: sentiment polarity for given text
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

            wn_tag = converter.penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            if word in stop_words:
                continue

            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue

            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue

            file.write("WORD " + word + "\t")
            file.write("FIRST SYNSET FOR WORD: " + str(synsets[0].name))
            swn_synset = swn.senti_synset(synsets[0].name())
            pos = swn_synset.pos_score()
            neg = swn_synset.neg_score()
            file.write("\nSENTIMENT: " + "positive: " + str(pos) + ", negative: " + str(neg) + "\n")

            if pos != neg or pos != 0:
                pos_score_sentence += pos
                neg_score_sentence += neg
                count_words += 1

        pos_avg_sentence, neg_avg_sentence = (pos_score_sentence / count_words, neg_score_sentence / count_words) if count_words != 0 else (0, 0)
        if pos_avg_sentence != neg_avg_sentence or pos_avg_sentence != 0:
            pos_score_text += pos_avg_sentence
            neg_score_text += neg_avg_sentence
            count_sentences += 1

    pos_avg_text, neg_avg_text = (pos_score_text / count_sentences, neg_score_text / count_sentences) if count_sentences != 0 else (0, 0)
    #TODO: suprotan slucaj proveriti kakve rezultate daje!!
    if pos_avg_text > neg_avg_text:
        return const.POSITIVE
    else:
        return const.NEGATIVE


def calc_percent_for_corpus(english_corpus):
    """
    For given corpus calculate tp, tn, fp, fn
    :param english_corpus: 
    :return:
    """
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    i = 1
    for t, rating in english_corpus:
        text = converter.remove_punctuation(t)
        #TODO: remove \\ and add slashes for Windows and Linux!!!!
        file = open("..\\..\\output_data\\english_corpus\\" + str(i) + "_" + rating + ".txt", "w", encoding='utf8')
        i += 1

        new_r = swn_polarity(text, file)
        file.write("\nNew Rating: " + new_r)
        file.close()

        if rating == const.POSITIVE:
            if new_r == const.POSITIVE:
                tp += 1
            if new_r == const.NEGATIVE:
                fn += 1
        if rating == const.NEGATIVE:
            if new_r == const.POSITIVE:
                fp += 1
            if new_r == const.NEGATIVE:
                tn += 1

    return tp, tn, fp, fn



english_corpus = loader.load_english_corpus("..\\..\\input_data\\txt_sentoken - all items")
precision_recall_file = open("..\\..\\output_data\\english_corpus\\precision_recall.txt", "w", encoding='utf8')

tp, tn, fp, fn = calc_percent_for_corpus(english_corpus)
#TODO: calculate accuracy also!!
precision = tp/(tp + fp)*100
recall = tp/(tp + fn)*100
f_measure = 2*precision*recall/(precision + recall)

print("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure))
precision_recall_file.write("precision: " + str(precision) + " recall: " + str(recall) + " f measure: " + str(f_measure))
precision_recall_file.close()
