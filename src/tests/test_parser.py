import unittest
from src.parser.parser import Parser
from src.parser.loader import Loader


class MyTestCase(unittest.TestCase):

    def test_get_words_from_sentence(self):
        sentence1 = "Ja sam Jelena!"
        words_from_sentence_1 = Parser.get_words_from_sentence(sentence1)
        expected_words1 = ['Ja', 'sam', 'Jelena']
        self.assertEqual(expected_words1, words_from_sentence_1)

        sentence2 = "On upita: \"Kako se ti zoves\"?"
        words_from_sentence_2 = Parser.get_words_from_sentence(sentence2)
        expected_words2 = ['On', 'upita', 'Kako', 'se', 'ti', 'zoves']
        self.assertEqual(expected_words2, words_from_sentence_2)

    def test_get_sentences_from_text(self):
        text = "Ja sam Jelena! On upita: \"Kako se ti zoves\"?"
        sentences_from_text = Parser.get_sentences_from_text(text)
        expected_sentences = ['Ja sam Jelena!', 'On upita: \"Kako se ti zoves\"?']
        self.assertEqual(expected_sentences, sentences_from_text)

    def test_remove_stop_words_from_sentence(self):
        stop_words = Loader.load_stop_words("C:\\Users\\jeca\\Desktop\\master_rad\\StopWords")
        parser = Parser(stop_words)
        result = parser.remove_stop_words_from_sentence("Ja sam Ana i volim 45!")
        self.assertEqual(['Ana', 'volim'], result)

    def test_remove_stop_words_from_text(self):
        stop_words = Loader.load_stop_words("C:\\Users\\jeca\\Desktop\\master_rad\\StopWords")
        print(stop_words)
        parser = Parser(stop_words)
        result = parser.remove_stop_words_from_text("U životu sam pogledao mnogo loših filmova. Iz raznih razloga. "
                        "Vremenom sam se pomirio sa činjenicom da postoji dosta takvih I da obzirom na količinu otprilike "
                        "svaki četvrti na koji nabasam mora biti loš. Kako su prolazili kroz moj DVD plejer, shvatio sam da "
                        "I tu posotoji neka klasifikacija. Postoje manje loši, užasno loši, trash koji su čak i gledljivi, "
                        "bedno-patetični, oni gde je gluma kao u pozorištancetu Puž, gde je režija zeznula stvar, filmovi gde "
                        "scenario nema veze s mozgom, oni koji bi trebalo da su smešni a to nikako nisu, dosadni i predugi, "
                        "jadni a skupi, itd. Bilo je čak i nekih koji su kombinovali dva-tri ova elementa u sebi. ")
        self.assertEqual(['životu', 'pogledao', 'loših', 'filmova', 'raznih', 'razloga', 'Vremenom', 'pomirio', 'činjenicom',
                          'količinu', 'otprilike', 'četvrti', 'nabasam', 'loš', 'prolazili', 'DVD', 'plejer', 'shvatio',
                          'posotoji', 'klasifikacija', 'loši', 'užasno', 'loši', 'trash', 'gledljivi', 'bedno', 'patetični',
                          'gluma', 'pozorištancetu', 'Puž', 'režija', 'zeznula', 'stvar', 'filmovi', 'scenario', 'veze',
                          'mozgom', 'smešni', 'nisu', 'dosadni', 'predugi', 'jadni', 'skupi', 'kombinovali', 'elementa'], result)


if __name__ == '__main__':
    unittest.main()
