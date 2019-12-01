import unittest
import src.parser.loader as loader


class MyTestCase(unittest.TestCase):

    def test_load_text_from_txt(self):
        data = loader.load_text_from_txt_file("..\\..\\input_data\\text.txt")
        expected_text = "U životu sam pogledao mnogo loših filmova. Iz raznih razloga. " \
                        "Vremenom sam se pomirio sa činjenicom da postoji dosta takvih I da obzirom na količinu otprilike " \
                        "svaki četvrti na koji nabasam mora biti loš. Kako su prolazili kroz moj DVD plejer, shvatio sam da " \
                        "I tu posotoji neka klasifikacija. Postoje manje loši, užasno loši, trash koji su čak i gledljivi, " \
                        "bedno-patetični, oni gde je gluma kao u pozorištancetu Puž, gde je režija zeznula stvar, filmovi gde " \
                        "scenario nema veze s mozgom, oni koji bi trebalo da su smešni a to nikako nisu, dosadni i predugi, " \
                        "jadni a skupi, itd. Bilo je čak i nekih koji su kombinovali dva-tri ova elementa u sebi. " \
                        "Stari mudraci su mi pričali da će se jednom pojaviti jedan film koji će sadržati apsolutno " \
                        "SVE elemente lošeg filma u sebi. One film to rule them all! Film koji će biti toliko loš da će " \
                        "svi biti zaprepašćeni. Kada sam počeo da gledam Freelancers pomislio sam da to ne može biti TAJ film. " \
                        "Ipak je kako-tako solidno počeo, imao čak i poneku ok scenu, par dobrih riba i što je najbitnije – legende " \
                        "u svom kastingu koje su mi garantovale neku stopu kvaliteta. Međutim kako je odmicao, sve više lampica se palilo, " \
                        "sve više tajnih elemenata očajnosti filma se pojavljivalo. 50 Cent je produbljivao značenje reči „loša gluma“ " \
                        "i onda u epskom finalu, u poslednjih recimo 20 minuta filma, Freelancers je pokazao svoje pravo lice – " \
                        "to je bio TAJ film, najgori koji sam ikada gledao, veličanstven u svojoj bedi. Scena u džipu sa De Nirom i Fiftijem " \
                        "i uopšte zaplet koji je do nje doveo je nešto što mora da se vidi, čisto da bi shvatili o čemu pričam. " \
                        "Možda, samo možda, ovaj film ne bi bio uzvišeno najgori da su među glumcima neki običnosi (dobio bi 3,4 kokice)," \
                        " ali kada vidite na omotu da su se ovom ostvarenju pridružile filmske legende kao što su Robert De Niro i Forest Vitaker," \
                        " svakako imena koja bi ušla u skoro svačije spiskove 10 najboljih glumaca, onda ovaj užas mnogo dobija na težini." \
                        " Uporno tražim informacije da li su u nekim kockarskim dugovima ili ih Fifti drži u šaci zbog nekog orgijanja sa ne znam " \
                        "kakvim životinjama. Jer to su jedini legitimni razlozi da učestvuju u ovakvom filmu. Bez obzira što čak i ima nekoliko" \
                        " pozitivnih strana teret razočarenja je preveliki – dobija 0 kokica, jer ovo će se teško ponoviti. Proverite."
        self.assertEqual(expected_text, data)

    def test_load_text_list_from_csv_file(self):
        text_list = loader.load_text_list_from_csv_file("..\\..\\input_data\\SerbMR-3C.csv")
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
            "što su me uopšte zainteresovali za dalju kinematografiju….", text_list[2])

    def test_get_all_txt_file_paths_from_dir(self):
        txt_file_paths = loader.get_all_txt_file_paths_from_dir("..\\..\\input_data\\txt_sentoken")
        self.assertEqual("..\\..\\input_data\\txt_sentoken\\neg\\cv000_29416.txt", txt_file_paths[0])

    def test_find_encoding(self):
        file_path = "..\\..\\input_data\\StopWords\\stopwordsSRB 1.txt"
        result = loader.find_encoding(file_path)
        self.assertEqual('UTF-16', result)


if __name__ == '__main__':
    unittest.main()
