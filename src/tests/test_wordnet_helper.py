import unittest
from unittest.mock import Mock

from src.util.wordnet_helper import WordNetHelper
import src.util.loader as loader
import src.util.constants as const
import os


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.english_wordnet = loader.load_xlsx_file(".." + os.sep + ".." + os.sep + "input_data" + os.sep + "wnen.xlsx",
                                                    1)
        cls.serbian_wordnet_original = loader.load_xlsx_file(
            ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "sentiments_original.xlsx", 2)
        cls.serbian_wordnet_changed = loader.load_xlsx_file(
            ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "sentiments_with_replaced_items.xlsx", 2)
        cls.serbian_wordnet_deleted = loader.load_xlsx_file(
            ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "sentiments_without_items.xlsx", 2)
        cls.serbian_stop_words = loader.load_stop_words(
            ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "StopWords")

        cls.wordnetHelper = WordNetHelper(cls.english_wordnet, cls.serbian_wordnet_original,
                                          cls.serbian_wordnet_changed, cls.serbian_wordnet_deleted,
                                          cls.serbian_stop_words, ".." + os.sep + "input_data" + os.sep + "dictionary")

    def test_get_score_for_english_word(self):
        pos_score, neg_score = self.wordnetHelper.get_score_for_english_word('able', 'a')
        self.assertEqual(0.15625, pos_score)
        self.assertEqual(0, neg_score)

        pos_score, neg_score = self.wordnetHelper.get_score_for_english_word('able', 'n')
        self.assertEqual(-1, pos_score)
        self.assertEqual(-1, neg_score)

        pos_score, neg_score = self.wordnetHelper.get_score_for_english_word('the', 'n')
        self.assertEqual(-1, pos_score)
        self.assertEqual(-1, neg_score)

    def test_get_score_for_serbian_word(self):
        pos_score, neg_score, desc = self.wordnetHelper.get_score_for_serbian_word('senzacija', 'o', False)
        self.assertEqual(0.125, pos_score)
        self.assertEqual(0.250, neg_score)

        pos_score, neg_score, desc = self.wordnetHelper.get_score_for_serbian_word('senzacija', 'c', False)
        self.assertEqual(0.250, pos_score)
        self.assertEqual(0.125, neg_score)

        pos_score, neg_score, desc = self.wordnetHelper.get_score_for_serbian_word('senzacija', 'd', False)
        self.assertEqual(-1, pos_score)
        self.assertEqual(-1, neg_score)

        pos_score, neg_score, desc = self.wordnetHelper.get_score_for_serbian_word('senzacija', 'o', True)
        self.assertEqual(0.125, pos_score)
        self.assertEqual(0.250, neg_score)

        pos_score, neg_score, desc = self.wordnetHelper.get_score_for_serbian_word('senzacija', 'c', True)
        self.assertEqual(0.250, pos_score)
        self.assertEqual(0.125, neg_score)

        pos_score, neg_score, desc = self.wordnetHelper.get_score_for_serbian_word('senzacija', 'd', True)
        self.assertEqual(-1, pos_score)
        self.assertEqual(-1, neg_score)

    def test_clear_serbian_text(self):
        data_text = [('Braća', 'A:aem', 'Braća'), ('Koen', 'N:m', 'Koen'), ('(', 'PUNCT', '('), ('Coen', 'N:m', 'Coen'),
                     ('brothers', 'N:m', 'brothers'), (')', 'PUNCT', ')'), ('iako', 'CONJ', 'iako'),
                     ('poznati', 'V:m', 'poznati'),
                     ('po', 'PREP', 'po'), ('trilerima', 'N:m', 'triler'), (',', 'PUNCT', ','),
                     ('oprobali', 'V:m', 'oprobati'),
                     ('su', 'N:m', 'su'), ('se', 'PAR', 'se'), ('više', 'ADV', 'više'), ('puta', 'ADV', 'puta'),
                     ('i', 'CONJ', 'i'),
                     ('u', 'PREP', 'u'), ('komedija', 'N:f', 'komedija'), (',', 'PUNCT', ','), ('i', 'CONJ', 'i'),
                     ('postigli', 'V:m', 'postignuti'),
                     ('potpuni', 'A:aem', 'potpun'), ('uspeh', 'N:m', 'uspeh'), ('.', 'SENT', '.'),
                     ('Ovaj', 'PRO', 'ovaj'), ('film', 'N:m', 'film'),
                     (',', 'PUNCT', ','), ('pošto', 'CONJ', 'pošto'), ('je', 'PRO', 'ona'), ('kada', 'CONJ', 'kada'),
                     ('se', 'PAR', 'se'),
                     ('pojavio', 'V:m', 'pojaviti'), ('bio', 'V:m', 'biti'), ('vrlo', 'ADV', 'vrlo'),
                     ('loše', 'ADV', 'loše'),
                     ('prihvaćen', 'V:m', 'prihvatiti'), (',', 'PUNCT', ','), ('nije', 'A:aem', 'nije'),
                     ('nažalost', 'ADV', 'nažalost'),
                     ('uspeo', 'V:m', 'uspeti'), ('da', 'CONJ', 'da'), ('zablista', 'V:m', 'zablista'),
                     ('po', 'PREP', 'po'),
                     ('američkim', 'A:aem', 'američki'), ('bioskopima', 'N:m', 'bioskop'), (',', 'PUNCT', ','),
                     ('ali', 'CONJ', 'ali'),
                     ('je', 'PRO', 'ona'), ('zato', 'ADV', 'zato'), ('bio', 'V:m', 'biti'), ('prava', 'N:n', 'pravo'),
                     ('senzacija', 'N:f', 'senzacija'), ('kad', 'CONJ', 'kad'), ('se', 'PAR', 'se'),
                     ('pojavio', 'V:m', 'pojaviti'),
                     ('na', 'PREP', 'na'), ('DVD', 'N:f', 'DVD'), ('-', 'PUNCT', '-'), ('u', 'PREP', 'u'),
                     ('i', 'CONJ', 'i'),
                     ('na', 'PREP', 'na'), ('osnovu', 'N:f', 'osnova'), ('toga', 'PRO', 'taj'), (',', 'PUNCT', ','),
                     ('postao', 'V:m', 'postati'), ('jedan', 'NUM', 'jedan'), ('od', 'PREP', 'od'),
                     ('glavnih', 'A:aen', 'glavnih'),
                     ('naslova', 'N:m', 'naslov'), ('u', 'PREP', 'u'), ('kolekciji', 'N:f', 'kolekcija'),
                     ('svakog', 'PRO', 'svaki'),
                     ('pravog', 'A:aem', 'prav'), ('filmofila', 'N:m', 'filmofil'), ('.', 'SENT', '.'),
                     ('„', 'A:aem', '„'),
                     ('The', 'INT', 'The'), ('Big', 'N:m', 'Big'), ('Lebowski', 'A:aem', 'Lebowski'), ('“', 'N:m', '“'),
                     ('definitvno', 'A:aen', 'definitvno'), ('moj', 'PRO', 'moj'), ('omiljeni', 'A:aem', 'omiljen'),
                     ('film', 'N:m', 'film'), ('i', 'CONJ', 'i'), ('jedino', 'A:aen', 'jedini'),
                     ('ostvarenje', 'N:n', 'ostvarenje'),
                     ('koje', 'PRO', 'koji'), ('zaista', 'PAR', 'zaista'), ('uvek', 'ADV', 'uvek'),
                     ('iznova', 'ADV', 'iznova'),
                     ('i', 'CONJ', 'i'), ('iznova', 'ADV', 'iznova'), ('mogu', 'N:m', 'Mog'), ('da', 'CONJ', 'da'),
                     ('gledam', 'N:m', 'gledam'), ('.', 'SENT', '.'), ('On', 'PRO', 'on'),
                     ('predstavlja', 'N:n', 'predstavlja'),
                     ('odu', 'N:f', 'oda'), ('životnom', 'A:aem', 'životan'), ('stilu', 'N:n', 'stilo'),
                     ('jednog', 'NUM', 'jedan'),
                     ('pacifiste', 'N:m', 'pacifista'), ('.', 'SENT', '.'), ('„', 'A:aem', '„'), ('The', 'INT', 'The'),
                     ('Big', 'N:m', 'Big'), ('Lewbowski', 'A:aem', 'Lewbowski'), ('“', 'N:m', '“'),
                     ('je', 'PRO', 'ona'),
                     ('klasična', 'A:aem', 'klasičan'), ('priča', 'N:f', 'priča'), ('prevare', 'N:f', 'prevara'),
                     (',', 'PUNCT', ','), ('kriminala', 'N:m', 'kriminal'), ('i', 'CONJ', 'i'),
                     ('spletkarenja', 'N:n', 'spletkarenje'),
                     ('viđena', 'A:aen', 'viđen'), ('kroz', 'PREP', 'kroz'), ('oči', 'N:f', 'oči'),
                     ('skromnog', 'A:aem', 'skroman'),
                     ('čoveka', 'N:m', 'čovek'), (',', 'PUNCT', ','), ('tačnije', 'ADV', 'tačnije'),
                     ('jednostavne', 'A:aef', 'jednostavan'),
                     ('individue', 'N:f', 'individua'), ('sa', 'PREP', 'sa'), ('vrlo', 'ADV', 'vrlo'),
                     ('malo', 'ADV', 'malo'),
                     ('prohteva', 'N:m', 'prohtev'), (',', 'PUNCT', ','), ('želja', 'N:f', 'želja'), ('i', 'CONJ', 'i'),
                     ('ambicija', 'N:f', 'ambicija'), ('.', 'SENT', '.'), ('Žanr', 'N:m', 'Žanr'),
                     ('ovog', 'PRO', 'ovaj'),
                     ('filma', 'N:m', 'film'), ('nije', 'V:m', 'nije'), ('lako', 'ADV', 'lako'),
                     ('odrediti', 'A:aem', 'odrediti'),
                     ('–', 'N:m', '–'), ('može', 'A:aem', 'može'), ('se', 'PAR', 'se'), ('reći', 'V:m', 'reći'),
                     ('da', 'CONJ', 'da'),
                     ('je', 'PRO', 'ona'), ('komedija', 'N:f', 'komedija'), ('zbog', 'PREP', 'zbog'),
                     ('svog', 'PRO', 'svoj'),
                     ('izuzetno', 'ADV', 'izuzetno'), ('originalnog', 'A:aen', 'originalan'),
                     ('humorističkog', 'A:aen', 'humoristički'),
                     ('sadržaja', 'N:m', 'sadržaj'), ('.', 'SENT', '.'), ('Bogat', 'A:aem', 'bogat'),
                     ('fantastičnim', 'A:aem', 'fantastičan'),
                     ('likovima', 'N:m', 'lik'), ('i', 'CONJ', 'i'), ('još', 'ADV', 'još'),
                     ('boljim', 'A:bem', 'dobar'),
                     ('dijalozima', 'N:m', 'dijalog'), (',', 'PUNCT', ','), ('koji', 'PRO', 'koji'),
                     ('iako', 'CONJ', 'iako'),
                     ('su', 'N:m', 'su'), ('se', 'PAR', 'se'), ('transformisali', 'V:m', 'transformisati'),
                     ('u', 'PREP', 'u'),
                     ('besmrtne', 'A:aef', 'besmrtan'), ('citate', 'N:m', 'citat'), ('koji', 'PRO', 'koji'),
                     ('se', 'PAR', 'se'),
                     ('koriste', 'N:m', 'koriste'), ('u', 'PREP', 'u'), ('svakodnevnom', 'A:aef', 'svakodnevan'),
                     ('životu', 'N:m', 'život'),
                     (',', 'PUNCT', ','), ('„', 'N:m', '„'), ('The', 'INT', 'The'), ('Big', 'N:m', 'Big'),
                     ('Lebowski', 'A:aem', 'Lebowski'),
                     ('“', 'N:m', '“'), ('i', 'CONJ', 'i'), ('pored', 'PREP', 'pored'), ('ovih', 'PRO', 'ovaj'),
                     ('sada', 'ADV', 'sada'),
                     ('već', 'CONJ', 'već'), ('navedenih', 'A:aen', 'naveden'), ('segmenata', 'N:m', 'segment'),
                     ('ima', 'V:m', 'ima'),
                     ('još', 'ADV', 'još'), ('toliko', 'ADV', 'toliko'), ('mnogo', 'ADV', 'mnogo'),
                     ('toga', 'PRO', 'taj'),
                     ('da', 'CONJ', 'da'), ('ponudi', 'N:f', 'ponuda'), ('.', 'SENT', '.'), ('Gluma', 'N:f', 'gluma'),
                     ('u', 'PREP', 'u'),
                     ('ovom', 'PRO', 'ovaj'), ('filmu', 'N:m', 'film'), ('je', 'PRO', 'ona'),
                     ('zaista', 'PAR', 'zaista'),
                     ('neponovljiva', 'A:aef', 'neponovljiv'), ('.', 'SENT', '.'),
                     ('Definitvni', 'A:aem', 'Definitvni'),
                     ('vrh', 'N:m', 'vrh'), ('karijere', 'N:f', 'karijera'), ('za', 'PREP', 'za'),
                     ('Džefa', 'N:m', 'Džef'),
                     ('Bridžesa', 'N:m', 'Bridžesa'), ('(', 'PUNCT', '('), ('Jeff', 'N:m', 'Jeff'),
                     ('Bridges', 'N:m', 'Bridges'),
                     (')', 'PUNCT', ')'), ('i', 'CONJ', 'i'), ('Džona', 'N:m', 'Džon'), ('Gudmana', 'N:m', 'Gudman'),
                     ('(', 'PUNCT', '('), ('John', 'N:m', 'John'), ('Goodman', 'N:m', 'Goodman'), (')', 'PUNCT', ')'),
                     ('.', 'SENT', '.'), ('Iako', 'CONJ', 'iako'), ('su', 'N:m', 'su'), ('obojica', 'N:f', 'obojica'),
                     ('vrhunska', 'A:aef', 'vrhunski'), ('klasa', 'N:f', 'klasa'), ('glumaca', 'N:m', 'glumac'),
                     (',', 'PUNCT', ','), ('sa', 'PREP', 'sa'), ('izvanrednim', 'A:aef', 'izvanredan'),
                     ('karijerama', 'N:f', 'karijera'),
                     (',', 'PUNCT', ','), ('nikada', 'ADV', 'nikada'), ('nisu', 'N:m', 'nisu'),
                     ('uspeli', 'V:m', 'uspeti'),
                     ('da', 'CONJ', 'da'), ('se', 'PAR', 'se'), ('udalje', 'N:m', 'udalje'), ('od', 'PREP', 'od'),
                     ('ovih', 'PRO', 'ovaj'), ('kultnih', 'A:aen', 'kultnih'), ('likova', 'N:n', 'likovo'),
                     (',', 'PUNCT', ','),
                     ('a', 'CONJ', 'a'), ('otuda', 'ADV', 'otuda'), ('i', 'CONJ', 'i'), ('Bridžesu', 'N:m', 'Bridžesu'),
                     ('nadimak', 'N:m', 'nadimak'), ('koji', 'PRO', 'koji'), ('ga', 'PRO', 'on'),
                     ('prati', 'N:f', 'prati'),
                     ('već', 'CONJ', 'već'), ('deceniju', 'N:f', 'decenija'), ('i', 'CONJ', 'i'),
                     ('pratiće', 'N:f', 'pratiće'),
                     ('ga', 'PRO', 'on'), ('ceo', 'A:aem', 'ceo'), ('život', 'N:m', 'život'), ('–', 'N:m', '–'),
                     ('The', 'INT', 'The'),
                     ('Dude', 'N:f', 'Duda'), ('.', 'SENT', '.'), ('Cela', 'A:aef', 'ceo'),
                     ('glumačka', 'A:aef', 'glumački'),
                     ('ekipa', 'N:f', 'ekipa'), ('je', 'PRO', 'ona'), ('izuzetnog', 'A:aem', 'izuzetan'),
                     ('kvaliteta', 'N:m', 'kvalitet'),
                     ('.', 'SENT', '.'), ('Tu', 'PRO', 'taj'), ('stoje', 'N:f', 'stoja'), ('još', 'ADV', 'još'),
                     ('imena', 'N:n', 'ime'),
                     ('kao', 'CONJ', 'kao'), ('što', 'CONJ', 'što'), ('su', 'N:m', 'su'), ('Stiv', 'N:m', 'Stiv'),
                     ('Bušemi', 'N:m', 'Bušemi'),
                     ('(', 'PUNCT', '('), ('Steve', 'N:m', 'Steva'), ('Buscemi', 'N:m', 'Buscemi'), (')', 'PUNCT', ')'),
                     (',', 'PUNCT', ','),
                     ('Džon', 'N:m', 'Džon'), ('Torturo', 'N:f', 'tortura'), ('(', 'PUNCT', '('),
                     ('John', 'N:m', 'John'),
                     ('Turturro', 'N:m', 'Turturro'), (')', 'PUNCT', ')'), (',', 'PUNCT', ','),
                     ('Džulijana', 'N:f', 'Džulijana'),
                     ('Mur', 'N:m', 'Mur'), ('(', 'PUNCT', '('), ('Julianne', 'N:f', 'Julianne'),
                     ('Moore', 'N:m', 'Moore'), (')', 'PUNCT', ')'),
                     ('i', 'CONJ', 'i'), ('Filip', 'N:m', 'Filip'), ('Sejmur', 'N:m', 'Sejmur'),
                     ('Hofman', 'N:m', 'Hofman'), ('(', 'PUNCT', '('),
                     ('Philip', 'N:m', 'Philip'), ('Seymour', 'N:m', 'Seymour'), ('Hoffman', 'N:m', 'Hoffman'),
                     (')', 'PUNCT', ')'),
                     ('.', 'SENT', '.'), ('Svako', 'PRO', 'svaki'), ('je', 'PRO', 'ona'), ('zaista', 'PAR', 'zaista'),
                     ('uradio', 'V:m', 'uraditi'),
                     ('i', 'CONJ', 'i'), ('više', 'ADV', 'više'), ('što', 'CONJ', 'što'), ('se', 'PAR', 'se'),
                     ('od', 'PREP', 'od'),
                     ('njih', 'PRO', 'ona'), ('moglo', 'V:n', 'moći'), ('očekivati', 'A:aem', 'očekivati'),
                     (',', 'PUNCT', ','),
                     ('a', 'CONJ', 'a'), ('pogotovo', 'ADV', 'pogotovo'), ('Torturo', 'N:f', 'tortura'),
                     ('koje', 'PRO', 'koji'),
                     ('je', 'PRO', 'ona'), ('ovde', 'ADV', 'ovde'), ('stvario', 'V:m', 'stvario'),
                     ('jednog', 'NUM', 'jedan'),
                     ('od', 'PREP', 'od'), ('najzabavnijih', 'A:cef', 'zabavan'), ('epizodnih', 'A:aen', 'epizodan'),
                     ('likova', 'N:n', 'likovo'), ('u', 'PREP', 'u'), ('svim', 'PRO', 'sav'),
                     ('filmovima', 'N:m', 'film'),
                     ('ikada', 'ADV', 'ikada'), ('.', 'SENT', '.'), ('Po', 'PREP', 'po'), ('mom', 'PRO', 'moj'),
                     ('mišljenju', 'N:n', 'mišljenje'), (',', 'PUNCT', ','), ('„', 'N:m', '„'),
                     ('The', 'INT', 'The'), ('Big', 'N:m', 'Big'), ('Lebowski', 'A:aem', 'Lebowski'), ('“', 'N:m', '“'),
                     ('je', 'PRO', 'ona'), ('jedno', 'NUM', 'jedan'), ('od', 'PREP', 'od'),
                     ('najvećih', 'A:cen', 'velik'),
                     ('dostignuća', 'N:n', 'dostignuće'), ('u', 'PREP', 'u'), ('modernoj', 'A:aef', 'moderan'),
                     ('kinematografiji', 'N:f', 'kinematografija'), ('.', 'SENT', '.'), ('Ovaj', 'PRO', 'ovaj'),
                     ('projekat', 'N:m', 'projekt'), ('će', 'V:n', 'će'), ('vas', 'PRO', 'vi'),
                     ('nasmejati', 'N:m', 'nasmejati'),
                     (',', 'PUNCT', ','), ('zbuniti', 'N:m', 'zbuniti'), ('i', 'CONJ', 'i'),
                     ('zadiviti', 'N:m', 'zadiviti'),
                     (',', 'PUNCT', ','), ('i', 'CONJ', 'i'), ('on', 'PRO', 'on'), ('se', 'PAR', 'se'),
                     ('sa', 'PREP', 'sa'),
                     ('razlogom', 'N:m', 'razlog'), ('smatra', 'N:f', 'smatra'), ('za', 'PREP', 'za'),
                     ('jednu', 'NUM', 'jedan'),
                     ('od', 'PREP', 'od'), ('najcenjenijih', 'A:cen', 'cenjen'), ('komedija', 'N:f', 'komedija'),
                     ('od', 'PREP', 'od'),
                     ('strane', 'N:f', 'strana'), ('većine', 'N:f', 'većina'), ('kritičara', 'N:m', 'kritičar'),
                     ('.', 'SENT', '.')]
        loader.load_text_dictionary = Mock(return_value=(data_text, '1_pos.tt'))
        clean_text, opis, filename = self.wordnetHelper.clear_serbian_text(1, False)
        result_clean_text = ['braća', 'koen', 'coen', 'brothers', 'poznati', 'triler', 'oprobati', 'komedija',
                             'postignuti', 'potpun', 'uspeh',
                             'film', 'pojaviti', 'vrlo', 'loše', 'prihvatiti', 'nije', 'nažalost', 'uspeti', 'zablista',
                             'američki', 'bioskop',
                             'pravo', 'senzacija', 'pojaviti', 'dvd', 'osnova', 'glavnih', 'naslov', 'kolekcija',
                             'prav', 'filmofil', '„', 'big',
                             'lebowski', '“', 'definitvno', 'omiljen', 'film', 'ostvarenje', 'gledam', 'predstavlja',
                             'oda', 'životan', 'stilo',
                             'pacifista', '„', 'big', 'lewbowski', '“', 'klasičan', 'priča', 'prevara', 'kriminal',
                             'spletkarenje', 'viđen',
                             'oči', 'skroman', 'čovek', 'tačnije', 'jednostavan', 'individua', 'vrlo', 'prohtev',
                             'želja', 'ambicija', 'žanr',
                             'film', 'nije', 'odrediti', '–', 'reći', 'komedija', 'originalan', 'humoristički',
                             'sadržaj', 'bogat', 'fantastičan',
                             'lik', 'dobar', 'dijalog', 'transformisati', 'besmrtan', 'citat', 'koriste', 'svakodnevan',
                             'život', '„', 'big', 'lebowski',
                             '“', 'naveden', 'segment', 'ponuda', 'gluma', 'film', 'neponovljiv', 'definitvni',
                             'karijera', 'džef', 'bridžesa', 'jeff', 'bridges',
                             'džon', 'gudman', 'john', 'goodman', 'obojica', 'vrhunski', 'klasa', 'glumac',
                             'izvanredan', 'karijera', 'nisu', 'uspeti',
                             'udalje', 'kultnih', 'likovo', 'otuda', 'bridžesu', 'nadimak', 'prati', 'pratiće', 'život',
                             '–', 'duda', 'ceo', 'glumački', 'ekipa',
                             'izuzetan', 'kvalitet', 'stoja', 'stiv', 'bušemi', 'steva', 'buscemi', 'džon', 'tortura',
                             'john', 'turturro', 'džulijana',
                             'mur', 'julianne', 'moore', 'filip', 'sejmur', 'hofman', 'philip', 'seymour', 'hoffman',
                             'uraditi', 'očekivati', 'pogotovo', 'tortura',
                             'stvario', 'zabavan', 'epizodan', 'likovo', 'film', 'mišljenje', '„', 'big', 'lebowski',
                             '“', 'velik', 'dostignuće', 'moderan',
                             'kinematografija', 'projekt', 'nasmejati', 'zbuniti', 'zadiviti', 'razlog', 'smatra',
                             'cenjen', 'komedija', 'strana', 'većina', 'kritičar']
        self.assertEqual(result_clean_text, clean_text)
        self.assertEqual('1_pos.tt', filename)

    def test_clear_english_text(self):
        text = "plot : two teen couples go to a church party , drink and then drive . " \
               "they get into an accident . " \
               "one of the guys dies , but his girlfriend continues to see him in her life , and has nightmares ." \
               "what's the deal ? " \
               "watch the movie and \" sorta \" find out . . . " \
               "critique : a mind-fuck movie for the teen generation that touches on a very cool idea , but presents it in a very bad package . " \
               "which is what makes this review an even harder one to write , since i generally applaud films which attempt to break the mold ," \
               " mess with your head and such ( lost highway & memento ) , but there are good and bad ways of making all types of films , and these folks just didn't snag this one correctly ." \
               "they seem to have taken this pretty neat concept , but executed it terribly . " \
               "so what are the problems with the movie ? " \
               "well , its main problem is that it's simply too jumbled . " \
               "it starts off \" normal \" but then downshifts into this \" fantasy \" world in which you , as an audience member , have no idea what's going on . " \
               "there are dreams , there are characters coming back from the dead , there are others who look like the dead , there are strange apparitions , " \
               "there are disappearances , there are a looooot of chase scenes , there are tons of weird things that happen , and most of it is simply not explained ." \
               "now i personally don't mind trying to unravel a film every now and then , but when all it does is give me the same clue over and over again , i get kind of fed up after a while , which is this film's biggest problem ." \
               "it's obviously got this big secret to hide , but it seems to want to hide it completely until its final five minutes . " \
               "and do they make things entertaining , thrilling or even engaging , in the meantime ? not really . " \
               "the sad part is that the arrow and i both dig on flicks like this , so we actually figured most of it out by the half-way point , " \
               "so all of the strangeness after that did start to make a little bit of sense , but it still didn't the make the film all that more entertaining ." \
               "i guess the bottom line with movies like this is that you should always make sure that the audience is \" into it \" even before they are given the secret password to enter your world of understanding ." \
               "i mean , showing melissa sagemiller running away from visions for about 20 minutes throughout the movie is just plain lazy ! ! " \
               "okay , we get it . . . there are people chasing her and we don't know who they are . " \
               "do we really need to see it over and over again ? how about giving us different scenes offering further insight into all of the strangeness going down in the movie ? " \
               "apparently , the studio took this film away from its director and chopped it up themselves , and it shows . " \
               "there might've been a pretty decent teen mind-fuck movie in here somewhere , but i guess \" the suits \" decided that turning it into a music video with little edge , would make more sense ." \
               "the actors are pretty good for the most part , although wes bentley just seemed to be playing the exact same character that he did in american beauty , only in a new neighborhood ." \
               "but my biggest kudos go out to sagemiller , who holds her own throughout the entire film , and actually has you feeling her character's unraveling ." \
               "overall , the film doesn't stick because it doesn't entertain , it's confusing , it rarely excites and it feels pretty redundant for most of its runtime , despite a pretty cool ending and explanation to all of the craziness that came before it ." \
               "oh , and by the way , this is not a horror or teen slasher flick . . . it's just packaged to look that way because someone is apparently assuming that the genre is still hot with the kids . " \
               "it also wrapped production two years ago and has been sitting on the shelves ever since . whatever . . . skip it ! " \
               "where's joblo coming from ? a nightmare of elm street 3 ( 7/10 ) - blair witch 2 ( 7/10 ) - the crow " \
               "( 9/10 ) - the crow : salvation ( 4/10 ) - lost highway ( 10/10 ) - memento ( 10/10 ) - the others ( 9/10 ) - stir of echoes ( 8/10 ) "
        clear_english_text = self.wordnetHelper.clear_english_text(text)
        result_text = [('plot', 'n'), ('teen', 'n'), ('couple', 'n'), ('church', 'n'), ('party', 'n'), ('drink', 'n'),
                       ('drive', 'n'),
                       ('accident', 'n'), ('guy', 'n'), ('girlfriend', 'n'), ('life', 'n'), ('nightmare', 'n'),
                       ('deal', 'n'), ('movie', 'n'),
                       ('sorta', 'a'), ('critique', 'n'), ('mind-fuck', 'a'), ('movie', 'n'), ('teen', 'a'),
                       ('generation', 'n'), ('cool', 'a'), ('idea', 'n'), ('bad', 'a'), ('package', 'n'),
                       ('review', 'n'), ('even', 'r'), ('hard', 'r'), ('generally', 'r'), ('film', 'n'),
                       ('mold', 'n'), ('mess', 'n'), ('head', 'n'), ('highway', 'n'), ('memento', 'n'),
                       ('good', 'a'), ('bad', 'a'), ('way', 'n'), ('type', 'n'), ('film', 'n'), ('folk', 'n'),
                       ("n't", 'r'), ('correctly', 'r'), ('pretty', 'r'), ('neat', 'a'), ('concept', 'n'),
                       ('terribly', 'r'), ('problem', 'n'), ('movie', 'n'), ('well', 'r'), ('main', 'a'),
                       ('problem', 'n'), ('simply', 'r'), ('normal', 'a'), ('fantasy', 'a'), ('world', 'n'),
                       ('audience', 'n'), ('member', 'n'), ('idea', 'n'), ('dream', 'n'), ('character', 'n'),
                       ('back', 'r'), ('dead', 'a'), ('others', 'n'), ('dead', 'a'), ('strange', 'a'),
                       ('apparition', 'n'),
                       ('disappearance', 'n'), ('looooot', 'n'), ('chase', 'n'), ('scene', 'n'), ('ton', 'n'),
                       ('weird', 'a'), ('thing', 'n'), ('simply', 'r'), ('personally', 'r'), ("n't", 'r'),
                       ('film', 'n'), ('clue', 'n'), ('kind', 'n'), ('film', 'n'), ('big', 'a'), ('problem', 'n'),
                       ('.it', 'n'), ('obviously', 'r'), ('big', 'a'), ('secret', 'n'), ('completely', 'r'),
                       ('final', 'a'),
                       ('minute', 'n'), ('thing', 'n'), ('even', 'r'), ('meantime', 'n'), ('really', 'r'), ('sad', 'a'),
                       ('part', 'n'), ('arrow', 'n'), ('dig', 'n'), ('flick', 'n'), ('actually', 'r'),
                       ('half-way', 'a'),
                       ('point', 'n'), ('strangeness', 'n'), ('little', 'a'), ('bit', 'n'), ('sense', 'n'),
                       ('still', 'r'),
                       ("n't", 'r'), ('film', 'n'), ('entertaining', 'a'), ('.i', 'n'), ('guess', 'n'), ('bottom', 'a'),
                       ('line', 'n'), ('movie', 'n'), ('always', 'r'), ('sure', 'a'), ('audience', 'n'), ('even', 'r'),
                       ('secret', 'a'), ('password', 'n'), ('world', 'n'), ('.i', 'a'), ('mean', 'n'), ('melissa', 'a'),
                       ('sagemiller', 'n'), ('away', 'r'), ('vision', 'n'), ('minute', 'n'), ('movie', 'n'),
                       ('plain', 'a'),
                       ('lazy', 'a'), ('okay', 'n'), ('people', 'n'), ("n't", 'r'), ('really', 'r'), ('different', 'a'),
                       ('scene', 'n'), ('insight', 'n'), ('strangeness', 'n'), ('movie', 'n'), ('apparently', 'r'),
                       ('studio', 'n'), ('film', 'n'), ('away', 'r'), ('director', 'n'), ('pretty', 'a'),
                       ('decent', 'a'),
                       ('teen', 'a'), ('mind-fuck', 'a'), ('movie', 'n'), ('somewhere', 'r'), ('suit', 'n'),
                       ('music', 'n'),
                       ('video', 'n'), ('little', 'a'), ('edge', 'n'), ('sense', 'n'), ('.the', 'n'), ('actor', 'n'),
                       ('pretty', 'r'), ('good', 'a'), ('part', 'n'), ('wes', 'a'), ('bentley', 'n'), ('exact', 'a'),
                       ('character', 'n'), ('american', 'a'), ('beauty', 'n'), ('new', 'a'), ('neighborhood', 'n'),
                       ('.but', 'n'), ('big', 'a'), ('kudos', 'n'), ('entire', 'a'), ('film', 'n'), ('actually', 'r'),
                       ('character', 'n'), ('unraveling', 'a'), ('.overall', 'n'), ('film', 'n'), ("n't", 'r'),
                       ("n't", 'r'), ('rarely', 'r'), ('pretty', 'a'), ('redundant', 'n'), ('runtime', 'n'),
                       ('pretty', 'a'), ('cool', 'n'), ('explanation', 'n'), ('craziness', 'n'), ('.oh', 'n'),
                       ('way', 'n'), ('horror', 'n'), ('teen', 'a'), ('slasher', 'a'), ('flick', 'n'), ('way', 'n'),
                       ('someone', 'n'), ('apparently', 'r'), ('genre', 'n'), ('still', 'r'), ('hot', 'a'),
                       ('kid', 'n'),
                       ('also', 'r'), ('production', 'n'), ('year', 'n'), ('ago', 'r'), ('shelf', 'n'), ('ever', 'r'),
                       ('whatever', 'n'), ('joblo', 'n'), ('nightmare', 'n'), ('elm', 'a'), ('street', 'n'),
                       ('blair', 'n'),
                       ('witch', 'n'), ('crow', 'n'), ('crow', 'n'), ('salvation', 'n'), ('highway', 'n'),
                       ('memento', 'n'),
                       ('others', 'n'), ('stir', 'n'), ('echo', 'n')]
        self.assertEqual(result_text, clear_english_text)

    def test_get_score_for_text(self):
        text_english = "plot : two teen couples go to a church party , drink and then drive . " \
                       "they get into an accident . " \
                       "one of the guys dies , but his girlfriend continues to see him in her life , and has nightmares ." \
                       "what's the deal ? " \
                       "watch the movie and \" sorta \" find out . . . " \
                       "critique : a mind-fuck movie for the teen generation that touches on a very cool idea , but presents it in a very bad package . " \
                       "which is what makes this review an even harder one to write , since i generally applaud films which attempt to break the mold ," \
                       " mess with your head and such ( lost highway & memento ) , but there are good and bad ways of making all types of films , and these folks just didn't snag this one correctly ." \
                       "they seem to have taken this pretty neat concept , but executed it terribly . " \
                       "so what are the problems with the movie ? " \
                       "well , its main problem is that it's simply too jumbled . " \
                       "it starts off \" normal \" but then downshifts into this \" fantasy \" world in which you , as an audience member , have no idea what's going on . " \
                       "there are dreams , there are characters coming back from the dead , there are others who look like the dead , there are strange apparitions , " \
                       "there are disappearances , there are a looooot of chase scenes , there are tons of weird things that happen , and most of it is simply not explained ." \
                       "now i personally don't mind trying to unravel a film every now and then , but when all it does is give me the same clue over and over again , i get kind of fed up after a while , which is this film's biggest problem ." \
                       "it's obviously got this big secret to hide , but it seems to want to hide it completely until its final five minutes . " \
                       "and do they make things entertaining , thrilling or even engaging , in the meantime ? not really . " \
                       "the sad part is that the arrow and i both dig on flicks like this , so we actually figured most of it out by the half-way point , " \
                       "so all of the strangeness after that did start to make a little bit of sense , but it still didn't the make the film all that more entertaining ." \
                       "i guess the bottom line with movies like this is that you should always make sure that the audience is \" into it \" even before they are given the secret password to enter your world of understanding ." \
                       "i mean , showing melissa sagemiller running away from visions for about 20 minutes throughout the movie is just plain lazy ! ! " \
                       "okay , we get it . . . there are people chasing her and we don't know who they are . " \
                       "do we really need to see it over and over again ? how about giving us different scenes offering further insight into all of the strangeness going down in the movie ? " \
                       "apparently , the studio took this film away from its director and chopped it up themselves , and it shows . " \
                       "there might've been a pretty decent teen mind-fuck movie in here somewhere , but i guess \" the suits \" decided that turning it into a music video with little edge , would make more sense ." \
                       "the actors are pretty good for the most part , although wes bentley just seemed to be playing the exact same character that he did in american beauty , only in a new neighborhood ." \
                       "but my biggest kudos go out to sagemiller , who holds her own throughout the entire film , and actually has you feeling her character's unraveling ." \
                       "overall , the film doesn't stick because it doesn't entertain , it's confusing , it rarely excites and it feels pretty redundant for most of its runtime , despite a pretty cool ending and explanation to all of the craziness that came before it ." \
                       "oh , and by the way , this is not a horror or teen slasher flick . . . it's just packaged to look that way because someone is apparently assuming that the genre is still hot with the kids . " \
                       "it also wrapped production two years ago and has been sitting on the shelves ever since . whatever . . . skip it ! " \
                       "where's joblo coming from ? a nightmare of elm street 3 ( 7/10 ) - blair witch 2 ( 7/10 ) - the crow " \
                       "( 9/10 ) - the crow : salvation ( 4/10 ) - lost highway ( 10/10 ) - memento ( 10/10 ) - the others ( 9/10 ) - stir of echoes ( 8/10 ) "
        pos_score_text, neg_score_text, count_words, full_text = self.wordnetHelper.get_score_for_text(1, text_english,
                                                                                                       True, False)
        self.assertEqual(19.23979521295697, pos_score_text)
        self.assertEqual(17.52865682112006, neg_score_text)
        self.assertEqual(125, count_words)

        file_log = open(".." + os.sep + ".." + os.sep + "output_data" + os.sep + "sentimenti_log_test.txt", "w",
                        encoding='utf8')
        set_words = set()
        data_text = [('Braća', 'A:aem', 'Braća'), ('Koen', 'N:m', 'Koen'), ('(', 'PUNCT', '('), ('Coen', 'N:m', 'Coen'),
                     ('brothers', 'N:m', 'brothers'), (')', 'PUNCT', ')'), ('iako', 'CONJ', 'iako'),
                     ('poznati', 'V:m', 'poznati'),
                     ('po', 'PREP', 'po'), ('trilerima', 'N:m', 'triler'), (',', 'PUNCT', ','),
                     ('oprobali', 'V:m', 'oprobati'),
                     ('su', 'N:m', 'su'), ('se', 'PAR', 'se'), ('više', 'ADV', 'više'), ('puta', 'ADV', 'puta'),
                     ('i', 'CONJ', 'i'),
                     ('u', 'PREP', 'u'), ('komedija', 'N:f', 'komedija'), (',', 'PUNCT', ','), ('i', 'CONJ', 'i'),
                     ('postigli', 'V:m', 'postignuti'),
                     ('potpuni', 'A:aem', 'potpun'), ('uspeh', 'N:m', 'uspeh'), ('.', 'SENT', '.'),
                     ('Ovaj', 'PRO', 'ovaj'), ('film', 'N:m', 'film'),
                     (',', 'PUNCT', ','), ('pošto', 'CONJ', 'pošto'), ('je', 'PRO', 'ona'), ('kada', 'CONJ', 'kada'),
                     ('se', 'PAR', 'se'),
                     ('pojavio', 'V:m', 'pojaviti'), ('bio', 'V:m', 'biti'), ('vrlo', 'ADV', 'vrlo'),
                     ('loše', 'ADV', 'loše'),
                     ('prihvaćen', 'V:m', 'prihvatiti'), (',', 'PUNCT', ','), ('nije', 'A:aem', 'nije'),
                     ('nažalost', 'ADV', 'nažalost'),
                     ('uspeo', 'V:m', 'uspeti'), ('da', 'CONJ', 'da'), ('zablista', 'V:m', 'zablista'),
                     ('po', 'PREP', 'po'),
                     ('američkim', 'A:aem', 'američki'), ('bioskopima', 'N:m', 'bioskop'), (',', 'PUNCT', ','),
                     ('ali', 'CONJ', 'ali'),
                     ('je', 'PRO', 'ona'), ('zato', 'ADV', 'zato'), ('bio', 'V:m', 'biti'), ('prava', 'N:n', 'pravo'),
                     ('senzacija', 'N:f', 'senzacija'), ('kad', 'CONJ', 'kad'), ('se', 'PAR', 'se'),
                     ('pojavio', 'V:m', 'pojaviti'),
                     ('na', 'PREP', 'na'), ('DVD', 'N:f', 'DVD'), ('-', 'PUNCT', '-'), ('u', 'PREP', 'u'),
                     ('i', 'CONJ', 'i'),
                     ('na', 'PREP', 'na'), ('osnovu', 'N:f', 'osnova'), ('toga', 'PRO', 'taj'), (',', 'PUNCT', ','),
                     ('postao', 'V:m', 'postati'), ('jedan', 'NUM', 'jedan'), ('od', 'PREP', 'od'),
                     ('glavnih', 'A:aen', 'glavnih'),
                     ('naslova', 'N:m', 'naslov'), ('u', 'PREP', 'u'), ('kolekciji', 'N:f', 'kolekcija'),
                     ('svakog', 'PRO', 'svaki'),
                     ('pravog', 'A:aem', 'prav'), ('filmofila', 'N:m', 'filmofil'), ('.', 'SENT', '.'),
                     ('„', 'A:aem', '„'),
                     ('The', 'INT', 'The'), ('Big', 'N:m', 'Big'), ('Lebowski', 'A:aem', 'Lebowski'), ('“', 'N:m', '“'),
                     ('definitvno', 'A:aen', 'definitvno'), ('moj', 'PRO', 'moj'), ('omiljeni', 'A:aem', 'omiljen'),
                     ('film', 'N:m', 'film'), ('i', 'CONJ', 'i'), ('jedino', 'A:aen', 'jedini'),
                     ('ostvarenje', 'N:n', 'ostvarenje'),
                     ('koje', 'PRO', 'koji'), ('zaista', 'PAR', 'zaista'), ('uvek', 'ADV', 'uvek'),
                     ('iznova', 'ADV', 'iznova'),
                     ('i', 'CONJ', 'i'), ('iznova', 'ADV', 'iznova'), ('mogu', 'N:m', 'Mog'), ('da', 'CONJ', 'da'),
                     ('gledam', 'N:m', 'gledam'), ('.', 'SENT', '.'), ('On', 'PRO', 'on'),
                     ('predstavlja', 'N:n', 'predstavlja'),
                     ('odu', 'N:f', 'oda'), ('životnom', 'A:aem', 'životan'), ('stilu', 'N:n', 'stilo'),
                     ('jednog', 'NUM', 'jedan'),
                     ('pacifiste', 'N:m', 'pacifista'), ('.', 'SENT', '.'), ('„', 'A:aem', '„'), ('The', 'INT', 'The'),
                     ('Big', 'N:m', 'Big'), ('Lewbowski', 'A:aem', 'Lewbowski'), ('“', 'N:m', '“'),
                     ('je', 'PRO', 'ona'),
                     ('klasična', 'A:aem', 'klasičan'), ('priča', 'N:f', 'priča'), ('prevare', 'N:f', 'prevara'),
                     (',', 'PUNCT', ','), ('kriminala', 'N:m', 'kriminal'), ('i', 'CONJ', 'i'),
                     ('spletkarenja', 'N:n', 'spletkarenje'),
                     ('viđena', 'A:aen', 'viđen'), ('kroz', 'PREP', 'kroz'), ('oči', 'N:f', 'oči'),
                     ('skromnog', 'A:aem', 'skroman'),
                     ('čoveka', 'N:m', 'čovek'), (',', 'PUNCT', ','), ('tačnije', 'ADV', 'tačnije'),
                     ('jednostavne', 'A:aef', 'jednostavan'),
                     ('individue', 'N:f', 'individua'), ('sa', 'PREP', 'sa'), ('vrlo', 'ADV', 'vrlo'),
                     ('malo', 'ADV', 'malo'),
                     ('prohteva', 'N:m', 'prohtev'), (',', 'PUNCT', ','), ('želja', 'N:f', 'želja'), ('i', 'CONJ', 'i'),
                     ('ambicija', 'N:f', 'ambicija'), ('.', 'SENT', '.'), ('Žanr', 'N:m', 'Žanr'),
                     ('ovog', 'PRO', 'ovaj'),
                     ('filma', 'N:m', 'film'), ('nije', 'V:m', 'nije'), ('lako', 'ADV', 'lako'),
                     ('odrediti', 'A:aem', 'odrediti'),
                     ('–', 'N:m', '–'), ('može', 'A:aem', 'može'), ('se', 'PAR', 'se'), ('reći', 'V:m', 'reći'),
                     ('da', 'CONJ', 'da'),
                     ('je', 'PRO', 'ona'), ('komedija', 'N:f', 'komedija'), ('zbog', 'PREP', 'zbog'),
                     ('svog', 'PRO', 'svoj'),
                     ('izuzetno', 'ADV', 'izuzetno'), ('originalnog', 'A:aen', 'originalan'),
                     ('humorističkog', 'A:aen', 'humoristički'),
                     ('sadržaja', 'N:m', 'sadržaj'), ('.', 'SENT', '.'), ('Bogat', 'A:aem', 'bogat'),
                     ('fantastičnim', 'A:aem', 'fantastičan'),
                     ('likovima', 'N:m', 'lik'), ('i', 'CONJ', 'i'), ('još', 'ADV', 'još'),
                     ('boljim', 'A:bem', 'dobar'),
                     ('dijalozima', 'N:m', 'dijalog'), (',', 'PUNCT', ','), ('koji', 'PRO', 'koji'),
                     ('iako', 'CONJ', 'iako'),
                     ('su', 'N:m', 'su'), ('se', 'PAR', 'se'), ('transformisali', 'V:m', 'transformisati'),
                     ('u', 'PREP', 'u'),
                     ('besmrtne', 'A:aef', 'besmrtan'), ('citate', 'N:m', 'citat'), ('koji', 'PRO', 'koji'),
                     ('se', 'PAR', 'se'),
                     ('koriste', 'N:m', 'koriste'), ('u', 'PREP', 'u'), ('svakodnevnom', 'A:aef', 'svakodnevan'),
                     ('životu', 'N:m', 'život'),
                     (',', 'PUNCT', ','), ('„', 'N:m', '„'), ('The', 'INT', 'The'), ('Big', 'N:m', 'Big'),
                     ('Lebowski', 'A:aem', 'Lebowski'),
                     ('“', 'N:m', '“'), ('i', 'CONJ', 'i'), ('pored', 'PREP', 'pored'), ('ovih', 'PRO', 'ovaj'),
                     ('sada', 'ADV', 'sada'),
                     ('već', 'CONJ', 'već'), ('navedenih', 'A:aen', 'naveden'), ('segmenata', 'N:m', 'segment'),
                     ('ima', 'V:m', 'ima'),
                     ('još', 'ADV', 'još'), ('toliko', 'ADV', 'toliko'), ('mnogo', 'ADV', 'mnogo'),
                     ('toga', 'PRO', 'taj'),
                     ('da', 'CONJ', 'da'), ('ponudi', 'N:f', 'ponuda'), ('.', 'SENT', '.'), ('Gluma', 'N:f', 'gluma'),
                     ('u', 'PREP', 'u'),
                     ('ovom', 'PRO', 'ovaj'), ('filmu', 'N:m', 'film'), ('je', 'PRO', 'ona'),
                     ('zaista', 'PAR', 'zaista'),
                     ('neponovljiva', 'A:aef', 'neponovljiv'), ('.', 'SENT', '.'),
                     ('Definitvni', 'A:aem', 'Definitvni'),
                     ('vrh', 'N:m', 'vrh'), ('karijere', 'N:f', 'karijera'), ('za', 'PREP', 'za'),
                     ('Džefa', 'N:m', 'Džef'),
                     ('Bridžesa', 'N:m', 'Bridžesa'), ('(', 'PUNCT', '('), ('Jeff', 'N:m', 'Jeff'),
                     ('Bridges', 'N:m', 'Bridges'),
                     (')', 'PUNCT', ')'), ('i', 'CONJ', 'i'), ('Džona', 'N:m', 'Džon'), ('Gudmana', 'N:m', 'Gudman'),
                     ('(', 'PUNCT', '('), ('John', 'N:m', 'John'), ('Goodman', 'N:m', 'Goodman'), (')', 'PUNCT', ')'),
                     ('.', 'SENT', '.'), ('Iako', 'CONJ', 'iako'), ('su', 'N:m', 'su'), ('obojica', 'N:f', 'obojica'),
                     ('vrhunska', 'A:aef', 'vrhunski'), ('klasa', 'N:f', 'klasa'), ('glumaca', 'N:m', 'glumac'),
                     (',', 'PUNCT', ','), ('sa', 'PREP', 'sa'), ('izvanrednim', 'A:aef', 'izvanredan'),
                     ('karijerama', 'N:f', 'karijera'),
                     (',', 'PUNCT', ','), ('nikada', 'ADV', 'nikada'), ('nisu', 'N:m', 'nisu'),
                     ('uspeli', 'V:m', 'uspeti'),
                     ('da', 'CONJ', 'da'), ('se', 'PAR', 'se'), ('udalje', 'N:m', 'udalje'), ('od', 'PREP', 'od'),
                     ('ovih', 'PRO', 'ovaj'), ('kultnih', 'A:aen', 'kultnih'), ('likova', 'N:n', 'likovo'),
                     (',', 'PUNCT', ','),
                     ('a', 'CONJ', 'a'), ('otuda', 'ADV', 'otuda'), ('i', 'CONJ', 'i'), ('Bridžesu', 'N:m', 'Bridžesu'),
                     ('nadimak', 'N:m', 'nadimak'), ('koji', 'PRO', 'koji'), ('ga', 'PRO', 'on'),
                     ('prati', 'N:f', 'prati'),
                     ('već', 'CONJ', 'već'), ('deceniju', 'N:f', 'decenija'), ('i', 'CONJ', 'i'),
                     ('pratiće', 'N:f', 'pratiće'),
                     ('ga', 'PRO', 'on'), ('ceo', 'A:aem', 'ceo'), ('život', 'N:m', 'život'), ('–', 'N:m', '–'),
                     ('The', 'INT', 'The'),
                     ('Dude', 'N:f', 'Duda'), ('.', 'SENT', '.'), ('Cela', 'A:aef', 'ceo'),
                     ('glumačka', 'A:aef', 'glumački'),
                     ('ekipa', 'N:f', 'ekipa'), ('je', 'PRO', 'ona'), ('izuzetnog', 'A:aem', 'izuzetan'),
                     ('kvaliteta', 'N:m', 'kvalitet'),
                     ('.', 'SENT', '.'), ('Tu', 'PRO', 'taj'), ('stoje', 'N:f', 'stoja'), ('još', 'ADV', 'još'),
                     ('imena', 'N:n', 'ime'),
                     ('kao', 'CONJ', 'kao'), ('što', 'CONJ', 'što'), ('su', 'N:m', 'su'), ('Stiv', 'N:m', 'Stiv'),
                     ('Bušemi', 'N:m', 'Bušemi'),
                     ('(', 'PUNCT', '('), ('Steve', 'N:m', 'Steva'), ('Buscemi', 'N:m', 'Buscemi'), (')', 'PUNCT', ')'),
                     (',', 'PUNCT', ','),
                     ('Džon', 'N:m', 'Džon'), ('Torturo', 'N:f', 'tortura'), ('(', 'PUNCT', '('),
                     ('John', 'N:m', 'John'),
                     ('Turturro', 'N:m', 'Turturro'), (')', 'PUNCT', ')'), (',', 'PUNCT', ','),
                     ('Džulijana', 'N:f', 'Džulijana'),
                     ('Mur', 'N:m', 'Mur'), ('(', 'PUNCT', '('), ('Julianne', 'N:f', 'Julianne'),
                     ('Moore', 'N:m', 'Moore'), (')', 'PUNCT', ')'),
                     ('i', 'CONJ', 'i'), ('Filip', 'N:m', 'Filip'), ('Sejmur', 'N:m', 'Sejmur'),
                     ('Hofman', 'N:m', 'Hofman'), ('(', 'PUNCT', '('),
                     ('Philip', 'N:m', 'Philip'), ('Seymour', 'N:m', 'Seymour'), ('Hoffman', 'N:m', 'Hoffman'),
                     (')', 'PUNCT', ')'),
                     ('.', 'SENT', '.'), ('Svako', 'PRO', 'svaki'), ('je', 'PRO', 'ona'), ('zaista', 'PAR', 'zaista'),
                     ('uradio', 'V:m', 'uraditi'),
                     ('i', 'CONJ', 'i'), ('više', 'ADV', 'više'), ('što', 'CONJ', 'što'), ('se', 'PAR', 'se'),
                     ('od', 'PREP', 'od'),
                     ('njih', 'PRO', 'ona'), ('moglo', 'V:n', 'moći'), ('očekivati', 'A:aem', 'očekivati'),
                     (',', 'PUNCT', ','),
                     ('a', 'CONJ', 'a'), ('pogotovo', 'ADV', 'pogotovo'), ('Torturo', 'N:f', 'tortura'),
                     ('koje', 'PRO', 'koji'),
                     ('je', 'PRO', 'ona'), ('ovde', 'ADV', 'ovde'), ('stvario', 'V:m', 'stvario'),
                     ('jednog', 'NUM', 'jedan'),
                     ('od', 'PREP', 'od'), ('najzabavnijih', 'A:cef', 'zabavan'), ('epizodnih', 'A:aen', 'epizodan'),
                     ('likova', 'N:n', 'likovo'), ('u', 'PREP', 'u'), ('svim', 'PRO', 'sav'),
                     ('filmovima', 'N:m', 'film'),
                     ('ikada', 'ADV', 'ikada'), ('.', 'SENT', '.'), ('Po', 'PREP', 'po'), ('mom', 'PRO', 'moj'),
                     ('mišljenju', 'N:n', 'mišljenje'), (',', 'PUNCT', ','), ('„', 'N:m', '„'),
                     ('The', 'INT', 'The'), ('Big', 'N:m', 'Big'), ('Lebowski', 'A:aem', 'Lebowski'), ('“', 'N:m', '“'),
                     ('je', 'PRO', 'ona'), ('jedno', 'NUM', 'jedan'), ('od', 'PREP', 'od'),
                     ('najvećih', 'A:cen', 'velik'),
                     ('dostignuća', 'N:n', 'dostignuće'), ('u', 'PREP', 'u'), ('modernoj', 'A:aef', 'moderan'),
                     ('kinematografiji', 'N:f', 'kinematografija'), ('.', 'SENT', '.'), ('Ovaj', 'PRO', 'ovaj'),
                     ('projekat', 'N:m', 'projekt'), ('će', 'V:n', 'će'), ('vas', 'PRO', 'vi'),
                     ('nasmejati', 'N:m', 'nasmejati'),
                     (',', 'PUNCT', ','), ('zbuniti', 'N:m', 'zbuniti'), ('i', 'CONJ', 'i'),
                     ('zadiviti', 'N:m', 'zadiviti'),
                     (',', 'PUNCT', ','), ('i', 'CONJ', 'i'), ('on', 'PRO', 'on'), ('se', 'PAR', 'se'),
                     ('sa', 'PREP', 'sa'),
                     ('razlogom', 'N:m', 'razlog'), ('smatra', 'N:f', 'smatra'), ('za', 'PREP', 'za'),
                     ('jednu', 'NUM', 'jedan'),
                     ('od', 'PREP', 'od'), ('najcenjenijih', 'A:cen', 'cenjen'), ('komedija', 'N:f', 'komedija'),
                     ('od', 'PREP', 'od'),
                     ('strane', 'N:f', 'strana'), ('većine', 'N:f', 'većina'), ('kritičara', 'N:m', 'kritičar'),
                     ('.', 'SENT', '.')]
        loader.load_text_dictionary = Mock(return_value=(data_text, '1_pos.tt'))
        result_clean_text = ['braća', 'koen', 'coen', 'brothers', 'poznati', 'triler', 'oprobati', 'komedija',
                             'postignuti', 'potpun', 'uspeh',
                             'film', 'pojaviti', 'vrlo', 'loše', 'prihvatiti', 'nije', 'nažalost', 'uspeti', 'zablista',
                             'američki', 'bioskop',
                             'pravo', 'senzacija', 'pojaviti', 'dvd', 'osnova', 'glavnih', 'naslov', 'kolekcija',
                             'prav', 'filmofil', '„', 'big',
                             'lebowski', '“', 'definitvno', 'omiljen', 'film', 'ostvarenje', 'gledam', 'predstavlja',
                             'oda', 'životan', 'stilo',
                             'pacifista', '„', 'big', 'lewbowski', '“', 'klasičan', 'priča', 'prevara', 'kriminal',
                             'spletkarenje', 'viđen',
                             'oči', 'skroman', 'čovek', 'tačnije', 'jednostavan', 'individua', 'vrlo', 'prohtev',
                             'želja', 'ambicija', 'žanr',
                             'film', 'nije', 'odrediti', '–', 'reći', 'komedija', 'originalan', 'humoristički',
                             'sadržaj', 'bogat', 'fantastičan',
                             'lik', 'dobar', 'dijalog', 'transformisati', 'besmrtan', 'citat', 'koriste', 'svakodnevan',
                             'život', '„', 'big', 'lebowski',
                             '“', 'naveden', 'segment', 'ponuda', 'gluma', 'film', 'neponovljiv', 'definitvni',
                             'karijera', 'džef', 'bridžesa', 'jeff', 'bridges',
                             'džon', 'gudman', 'john', 'goodman', 'obojica', 'vrhunski', 'klasa', 'glumac',
                             'izvanredan', 'karijera', 'nisu', 'uspeti',
                             'udalje', 'kultnih', 'likovo', 'otuda', 'bridžesu', 'nadimak', 'prati', 'pratiće', 'život',
                             '–', 'duda', 'ceo', 'glumački', 'ekipa',
                             'izuzetan', 'kvalitet', 'stoja', 'stiv', 'bušemi', 'steva', 'buscemi', 'džon', 'tortura',
                             'john', 'turturro', 'džulijana',
                             'mur', 'julianne', 'moore', 'filip', 'sejmur', 'hofman', 'philip', 'seymour', 'hoffman',
                             'uraditi', 'očekivati', 'pogotovo', 'tortura',
                             'stvario', 'zabavan', 'epizodan', 'likovo', 'film', 'mišljenje', '„', 'big', 'lebowski',
                             '“', 'velik', 'dostignuće', 'moderan',
                             'kinematografija', 'projekt', 'nasmejati', 'zbuniti', 'zadiviti', 'razlog', 'smatra',
                             'cenjen', 'komedija', 'strana', 'većina', 'kritičar']
        self.wordnetHelper.clear_serbian_text = Mock(return_value=(result_clean_text, '', '1_pos.tt'))
        pos_score_text, neg_score_text, count_words, full_text = self.wordnetHelper.get_score_for_text(1, '', False,
                                                                                                       True, 'o', False,
                                                                                                       file_log,
                                                                                                       set_words)
        self.assertEqual(6.616713333333333, pos_score_text)
        self.assertEqual(2.667046666666667, neg_score_text)
        self.assertEqual(31, count_words)

        pos_score_text, neg_score_text, count_words, full_text = self.wordnetHelper.get_score_for_text(1, '', False,
                                                                                                       True, 'c', False,
                                                                                                       file_log,
                                                                                                       set_words)
        self.assertEqual(8.116963333333333, pos_score_text)
        self.assertEqual(1.1667966666666667, neg_score_text)
        self.assertEqual(31, count_words)

    def test_swn_polarity_english(self):
        self.wordnetHelper.get_score_for_text = Mock(return_value=(19.23979521295697, 17.52865682112006, 125, ''))
        text_english = "plot : two teen couples go to a church party , drink and then drive . " \
                       "they get into an accident . " \
                       "one of the guys dies , but his girlfriend continues to see him in her life , and has nightmares ." \
                       "what's the deal ? " \
                       "watch the movie and \" sorta \" find out . . . " \
                       "critique : a mind-fuck movie for the teen generation that touches on a very cool idea , but presents it in a very bad package . " \
                       "which is what makes this review an even harder one to write , since i generally applaud films which attempt to break the mold ," \
                       " mess with your head and such ( lost highway & memento ) , but there are good and bad ways of making all types of films , and these folks just didn't snag this one correctly ." \
                       "they seem to have taken this pretty neat concept , but executed it terribly . " \
                       "so what are the problems with the movie ? " \
                       "well , its main problem is that it's simply too jumbled . " \
                       "it starts off \" normal \" but then downshifts into this \" fantasy \" world in which you , as an audience member , have no idea what's going on . " \
                       "there are dreams , there are characters coming back from the dead , there are others who look like the dead , there are strange apparitions , " \
                       "there are disappearances , there are a looooot of chase scenes , there are tons of weird things that happen , and most of it is simply not explained ." \
                       "now i personally don't mind trying to unravel a film every now and then , but when all it does is give me the same clue over and over again , i get kind of fed up after a while , which is this film's biggest problem ." \
                       "it's obviously got this big secret to hide , but it seems to want to hide it completely until its final five minutes . " \
                       "and do they make things entertaining , thrilling or even engaging , in the meantime ? not really . " \
                       "the sad part is that the arrow and i both dig on flicks like this , so we actually figured most of it out by the half-way point , " \
                       "so all of the strangeness after that did start to make a little bit of sense , but it still didn't the make the film all that more entertaining ." \
                       "i guess the bottom line with movies like this is that you should always make sure that the audience is \" into it \" even before they are given the secret password to enter your world of understanding ." \
                       "i mean , showing melissa sagemiller running away from visions for about 20 minutes throughout the movie is just plain lazy ! ! " \
                       "okay , we get it . . . there are people chasing her and we don't know who they are . " \
                       "do we really need to see it over and over again ? how about giving us different scenes offering further insight into all of the strangeness going down in the movie ? " \
                       "apparently , the studio took this film away from its director and chopped it up themselves , and it shows . " \
                       "there might've been a pretty decent teen mind-fuck movie in here somewhere , but i guess \" the suits \" decided that turning it into a music video with little edge , would make more sense ." \
                       "the actors are pretty good for the most part , although wes bentley just seemed to be playing the exact same character that he did in american beauty , only in a new neighborhood ." \
                       "but my biggest kudos go out to sagemiller , who holds her own throughout the entire film , and actually has you feeling her character's unraveling ." \
                       "overall , the film doesn't stick because it doesn't entertain , it's confusing , it rarely excites and it feels pretty redundant for most of its runtime , despite a pretty cool ending and explanation to all of the craziness that came before it ." \
                       "oh , and by the way , this is not a horror or teen slasher flick . . . it's just packaged to look that way because someone is apparently assuming that the genre is still hot with the kids . " \
                       "it also wrapped production two years ago and has been sitting on the shelves ever since . whatever . . . skip it ! " \
                       "where's joblo coming from ? a nightmare of elm street 3 ( 7/10 ) - blair witch 2 ( 7/10 ) - the crow " \
                       "( 9/10 ) - the crow : salvation ( 4/10 ) - lost highway ( 10/10 ) - memento ( 10/10 ) - the others ( 9/10 ) - stir of echoes ( 8/10 ) "
        result_class, full_text = self.wordnetHelper.swn_polarity(1, text_english, True, False)
        self.assertEqual(const.POSITIVE, result_class)

    def test_swn_polarity_serbian(self):
        file_log = open(".." + os.sep + ".." + os.sep + "output_data" + os.sep + "sentimenti_log_test.txt", "w",
                        encoding='utf8')
        set_words = set()
        self.wordnetHelper.get_score_for_text = Mock(return_value=(8.116963333333333, 1.1667966666666667, 31, ''))
        result_class, full_text = self.wordnetHelper.swn_polarity(1, '', False, True, 'c', False, file_log, set_words,
                                                                  0.05)
        self.assertEqual(const.POSITIVE, result_class)


if __name__ == '__main__':
    unittest.main()
