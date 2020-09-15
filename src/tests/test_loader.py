import unittest
import src.util.loader as loader
import os


class MyTestCase(unittest.TestCase):

    def test_load_text_from_txt(self):
        data = loader.load_text_from_txt_file(".." + os.sep + ".." + os.sep + "input_data" + os.sep + "text.txt")
        expected_text = "Petoro ljudi zarobljeno je u zaglavljenom liftu, s tim što je neko od njih ubica," \
                        " a možda i nešto još gore... Ono što počinje kao film u maniru kakvog updateovanog Hitchcocka " \
                        "završava se kao tipični Shyamalan - infantilna smeša natprirodnog trilera/horora i melodrame, " \
                        "gde je sve sa svime i svako sa svakim u nekakvoj vezi Da je Đavo iz naslova više od potencijalne " \
                        "metafore biva nam vrlo brzo predočeno iz vizure jednog od čuvara u zgradi koji postaje svojevrsni " \
                        "(suvišni) vodič kroz film kao i medijum, da nam preko njega scenarista izloži deo koncepta koji " \
                        "nije mogao ubedljivije da provuče kroz dešavanja. Posmatrano kao jedan mali visokokonceptualizovani " \
                        "triler u kome je svako na neki način sumnjiv, Đavo uspeva da drži pažnju i tenziju na onom elementarnom" \
                        " nivou naše zapitanosti: šta će sledeće da se desi, ko će (i kako) sledeći da umre, i najzad, ko je ubica?" \
                        " Ovaj recept sa „deset malih crnaca' (samo u liftu) pružio je priliku za nekoliko zanimljivih scena i John " \
                        "Erick Dowdle (Karantin) uspeva da dešavanja (a posebno nedešavanja) učini gledljivim i da uz pomoć sjajnog " \
                        "direktora fotografije (Tak Fujimoto - Kad jaganjci utihnu, Šesto čulo...) sve to začini s nekoliko vrtoglavih" \
                        " kadrova zlokobnog oblakodera. Međutim, čemu sve to ako se u pakovanju nalazi tek jedna razvučena epizoda" \
                        " Zone sumraka? I to zaboravljiva i ispod proseka. Đavo je prvi film u horor serijalu Night Chronicles. " \
                        "M. Night Shyamalan (producent i idejni tvorac) zamislio je da u svakom novom filmu drugi autor razradi" \
                        " neku od njegovih ideja. Dakle, u osnovi to i jeste zamišljeno kao nešto nalik na Zonu sumraka u formatu" \
                        " celovečernjeg filma, i Shyamalan kao da je poslušao vapaje publike i distancirao se od sopstvenih ideja," \
                        " prepuštajući njihovu dalju razradu drugima umesto da izigrava kompletnog autora. Sasvim dobar koncept " \
                        "koji će možda uspeti da profunkcioniše, ali ovaj prvi korak ostavio je za sobom zamrljane tragove koji" \
                        " i previše podsećaju na Shyamalanova nedavna posrtanja. Dobra režija, uglavnom solidni i nepoznati glumci" \
                        " u nebitnim ulogama (od poznatih lica tu su Bojana Novaković i Matt Craven u epizodici), muzika koja " \
                        "potcrtava svaki trenutak napetosti (i pokušava da veštački stvori još koji), odlična fotografija... " \
                        "Ali, u osnovi svega nalazi se slaba priča, naivno i pomalo didaktički vođena i uz rasplet koji je " \
                        "interesantniji u onom površnom i u kontekstu ovog filma nebitnom smislu - ko je ubica? " \
                        "Poenta, tj. njen pokušaj, čini se, nalazi se u odgovoru na pitanje zašto, a to se ovde svodi " \
                        "na parafrazu završetka filma Znaci i glasi: misteriozni su putevi božji, odnosno, u ovom slučaju, đavolji."
        self.assertEqual(expected_text, data)

    def test_load_serbian_corpus(self):
        text_list = loader.load_serbian_corpus(".." + os.sep + ".." + os.sep + "input_data" + os.sep + "serb-all-2.csv")
        text, rating = text_list[2]
        self.assertEqual(
            "“Ulični Psi” je jedan od onih filmova koji svedoče da je originalna ideja znatno naprednija od ogromnog "
            "i bogatog projekta zasnovanog na već viđenoj radnji. Ovaj nisko budžetni film je zaista fantastično ostvarenje,"
            " odrađeno u najminimalnijim uslovima. Ovaj nasilni krimi triler je definitivno ostvarenje koje je Kventinu Tarantinu "
            "(Quentin Tarantino) otvorilo sva vrata za dalji tok njegove karijere, kao i film od kojeg je stekao poverenje i poštovanje "
            "kod šire publike i kritičara. Film je oskudan u svoji lokacijskim mestima snimanja. “Ulični Psi” su jedno minimalističko ostvarenje,"
            " zasnovano na odličnom scenariju, fantastičnim dijalozima, kao i sjajnoj montaži. Najsjanija tačka ovog filma jesu dijalozi. "
            "Oni su neverovatno originalni, interesantni, komični i kod skoro svakog gledaoca postaju vrlo citarani u stvarnom životu. "
            "Ono što se meni posebno sviđa kod filma je način na koji ga je Tarantino realizovao. Bez ikakvih kliše i nepotrebnih Holivudskih "
            "zapleta, groznih faktora romanse. Kventin priča jednu sasvim jednostavnu priču, u pravolinijskom smeru, ne daveći publiku nepotrebnim "
            "segmentima i informacijama. Film na jedan iskren način oslikava narav i psihologiju ovih kriminalaca, kojima na jedan sumnjiv način "
            "se planirana pljačka zakomplikuje. Projekat iako poseduje “Flashback“, prilično je lak za pratiti. Baš zbog tog svog nelinearnog stila "
            "uspeva da napravi kvalitetan zaplet, i da vas drži u neizvesnosti do samog kraja. Priča iako jeste kvalitetna i dopadljiva, mnogo više "
            "se projekat fokusira na upoznavanje i prezentovanje svojih bogatih likova. Svaki lik dobija svoju kratku pozadinsku priču, i time stvara "
            "utisak da je film sastavljen iz rezova nekih drugih projekata, čineći ga mnogo bogatijim. Ne vredi posebno pominjati nikoga iz glumačke ekipe,"
            " ovo su pravi profesionalci, puni harizme i šamra, koji u tom momentu, kada su prihvatili ovaj proizvod, nisu bili ni na samom početku svoje "
            "trenutne popularnosti. Toliko su ubedljivi i surovi, da sama pomisao da se nađete sa njima u istoj prostoriji je zbilja zabrinjavajuća. "
            "“Ulični Psi” je jedan vrlo nasilan film, neke scene su dosta surove, možda i teške za svariti, ali način na koji je stvarnost oslikana i "
            "mentalni sklop ovakvih pojedinaca je mnogo iznad toga. Film ni u jednom mementu ne glorifikuje nasilje, niti životni stil kriminalaca, "
            "on pored toga nosi poruku, koja svedoči da određeni postupci nose određene posledice. Ovo je jedan od meni dražih filmova, i među onima "
            "što su me uopšte zainteresovali za dalju kinematografiju….", text)
        self.assertEqual("POSITIVE", rating)

    def test_load_english_corpus(self):
        text_list = loader.load_english_corpus(
            ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "txt_sentoken - all items")
        text, rating = text_list[2]

        self.assertEqual("it is movies like these that make a jaded movie viewer thankful for the invention of the timex indiglo watch . \n"
                         "based on the late 1960's television show by the same name , the mod squad tells the tale of three reformed criminals under the employ of the police to go undercover . \n"
                         "however , things go wrong as evidence gets stolen and they are immediately under suspicion . \n"
                         "of course , the ads make it seem like so much more . \n"
                         "quick cuts , cool music , claire dane's nice hair and cute outfits , car chases , stuff blowing up , and the like . \n"
                         "sounds like a cool movie , does it not ? \n"
                         "after the first fifteen minutes , it quickly becomes apparent that it is not . \n"
                         "the mod squad is certainly a slick looking production , complete with nice hair and costumes , but that simply isn't enough . \n"
                         "the film is best described as a cross between an hour-long cop show and a music video , both stretched out into the span of an hour and a half . \n"
                         "and with it comes every single clich ? . \n"
                         "it doesn't really matter that the film is based on a television show , as most of the plot elements have been recycled from everything we've already seen . \n"
                         "the characters and acting is nothing spectacular , sometimes even bordering on wooden . \n"
                         "claire danes and omar epps deliver their lines as if they are bored , which really transfers onto the audience . \n"
                         "the only one to escape relatively unscathed is giovanni ribisi , who plays the resident crazy man , ultimately being the only thing worth watching . \n"
                         "unfortunately , even he's not enough to save this convoluted mess , as all the characters don't do much apart from occupying screen time . \n"
                         "with the young cast , cool clothes , nice hair , and hip soundtrack , it appears that the film is geared towards the teenage mindset . \n"
                         "despite an american 'r' rating ( which the content does not justify ) , the film is way too juvenile for the older mindset . \n"
                         "information on the characters is literally spoon-fed to the audience ( would it be that hard to show us instead of telling us ? ) , dialogue is poorly written , and the plot is extremely predictable . \n"
                         "the way the film progresses , you likely won't even care if the heroes are in any jeopardy , because you'll know they aren't . \n"
                         "basing the show on a 1960's television show that nobody remembers is of questionable wisdom , especially when one considers the target audience and the fact that the number of memorable films based on television shows can be counted on one hand ( even one that's missing a finger or two ) . \n"
                         "the number of times that i checked my watch ( six ) is a clear indication that this film is not one of them . \n"
                         "it is clear that the film is nothing more than an attempt to cash in on the teenage spending dollar , judging from the rash of really awful teen-flicks that we've been seeing as of late . \n"
                         "avoid this film at all costs .", text)
        self.assertEqual("NEGATIVE", rating)

    def test_load_stop_words(self):
        dir_path = ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "StopWords"
        result_set = loader.load_stop_words(dir_path)
        self.assertEqual(2007, len(result_set))

    def test_get_all_txt_file_paths_from_dir(self):
        txt_file_paths = loader.get_all_txt_file_paths_from_dir(".." + os.sep + ".." + os.sep + "input_data" + os.sep + "txt_sentoken - all items")
        self.assertEqual(".." + os.sep + ".." + os.sep + "input_data" + os.sep + "txt_sentoken - all items" + os.sep + "neg" + os.sep + "cv000_29416.txt", txt_file_paths[0])

    def test_find_encoding(self):
        file_path = ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "StopWords" + os.sep + "stopwordsSRB 1.txt"
        result = loader.find_encoding(file_path)
        self.assertEqual('UTF-16', result)

    def test_load_xlsx_file(self):
        file_path = ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "wnen.xlsx"
        result = loader.load_xlsx_file(file_path, 1)
        self.assertEqual(117659, len(result))

    def test_load_text_dictionary(self):
        file_path = ".." + os.sep + ".." + os.sep + "input_data" + os.sep + "dictionary"
        result_data_pos = loader.load_text_dictionary(1, file_path, True)
        self.assertEqual(('Braća', 'A:aem', 'Braća'), result_data_pos[0])

        result_data_neutr = loader.load_text_dictionary(982, file_path, True)
        self.assertEqual(('film', 'N:m', 'film'), result_data_neutr[15])

        result_data_neg = loader.load_text_dictionary(1698, file_path, True)
        self.assertEqual(('Day', 'A:aem', 'Day'), result_data_neg[5])

        result_data_pos_2 = loader.load_text_dictionary(154, file_path, False)
        self.assertEqual(('je', 'PRO', 'ona'), result_data_pos_2[9])

        result_data_neg_2 = loader.load_text_dictionary(898, file_path, False)
        self.assertEqual(('nova', 'A:aef', 'nov'), result_data_neg_2[3])


if __name__ == '__main__':
    unittest.main()
