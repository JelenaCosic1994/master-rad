import unittest
from src.parser.parser import Parser
import src.parser.loader as loader


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
        stop_words = loader.load_stop_words("..\\..\\input_data\\StopWords")
        parser = Parser(stop_words)
        result = parser.remove_stop_words_from_sentence("Ja sam Ana i volim 45!")
        self.assertEqual(['Ana', 'volim'], result)

    def test_remove_stop_words_from_text(self):
        stop_words = loader.load_stop_words("..\\..\\input_data\\StopWords")
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

    def test_is_cyrillic_text(self):
        input_string_true = "Чика Ђорђе жваће шљиве, његова ћерка Љиљана једе џем!"
        result_1 = Parser.is_cyrillic_text(input_string_true)
        self.assertTrue(result_1)

        input_string_false = "Čika Đorđe žvaće šljive, njegova ćerka Ljiljana jede džem!"
        result_2 = Parser.is_cyrillic_text(input_string_false)
        self.assertFalse(result_2)

        input_string_combined = "Чика Đorđe жваће šljive, његова ćerka Љиљана jede џем!"
        result_3 = Parser.is_cyrillic_text(input_string_combined)
        self.assertTrue(result_3)

        input_string_from_file_1 = loader.load_text_from_txt_file("..\\..\\input_data\\cyrillic_text.txt")
        result_4 = Parser.is_cyrillic_text(input_string_from_file_1)
        self.assertTrue(result_4)

        input_string_from_file_2 = loader.load_text_from_txt_file("..\\..\\input_data\\text.txt")
        result_5 = Parser.is_cyrillic_text(input_string_from_file_2)
        self.assertFalse(result_5)

    def test_translate_from_cyrillic_to_latinic(self):
        result_1 = Parser.convert_from_cyrillic_to_latinic("Чика Ђорђе жваће шљиве, његова ћерка Љиљана једе џем!")
        self.assertEqual("Čika Đorđe žvaće šljive, njegova ćerka Ljiljana jede džem!", result_1)

        text = loader.load_text_from_txt_file("..\\..\\input_data\\cyrillic_text.txt")
        result_2 = Parser.convert_from_cyrillic_to_latinic(text)
        self.assertEqual("A šta ste očekivali? NAPOMENA: Kako me je @timjohnbyford obavestio verzija filma koja se prikazuje "
                         "u našim bioskopima je na bošnjačkom/srpskom/jeziku koji razumemo. Verzija filma koji sam ja gledao "
                         "(VOD rip sa neta) je na engleskom. Dakle, film nije nahovan na engleski preko pomenutih jezika, "
                         "već glumci sve replike, sa svojim matičnim akcentima, izgovaraju na engleskom. Što znači da je "
                         "Anđelina praktično snimila dva filma, ali i da su glumci imali nezahvalan profesionalan zadatak- "
                         "da ono što im je povereno ne samo glume na jeziku koji im nije blizak, već i da dvaput, a na različite načine, "
                         "iz sebe crpe emocije i kreativnu energiju za potrebe postavljenog zadatka. S obzirom na prirodu ovog filma "
                         "i obilan broj teških scena pretpostavljam da to nije bilo nimalo lako. Naslućujem da je puki razlog za ovo "
                         "plaćeno cimanje to što se američka publika gadi na titlove koliko i Srbi na suživot sa Šiptarima. "
                         "U svom prikazu filma ja ću probati da se ne bavim stvarima koje ste već čuli sa svih mogućih strana,"
                         " sem u slučaju kada diskutujem sa njima. Mnogi su filmu zamerili da je scenario loš i da je loša priča "
                         "loše vođena nikuda. S obzirom da je Anđelina Zemlju krvi i meda zamislila kao ljubavnu priču između Muslimanke "
                         "i Srbina tokom rata u Bosni, ovaj film formalno, ali dosta labavo, ispunjava tu nameru. Jedino što je njihov "
                         "odnos sve sem ljubavni. Uvodna sekvenca nam pokazuje Ajlu koja se sprema za izlazak, potom njen boravak u klubu"
                         " sa Danijelom, i sve se to završava, simbolično, eksplozijom koja tu romansu prekida. Ne znamo zašto "
                         "(zašto Danijel nije pobegao sa Ajlom negde, zašto je nije sklonio na sigurno, ako je toliko voli?...),"
                         " ne znamo ni koliko je ova romansa trajala (što bi trebalo da obezbedi uverljivost ostatka filma), "
                         "a ne znamo ni koliko su se njih dvoje voleli (da li im je ovo bio neki prvi dejt ili je trebalo da se "
                         "uzmu za mesec dana?). Nestrpljiva Anđelina već skače u kovitlac rata gde srpski paravojnici organizovano"
                         " odvode Muslimanke u nekakav logor (gde će ove biti mešavina džoj divižna i posluge). Tamo Danijel u "
                         "edukativnom pokušaju silovanja prepoznaje Ajlu tek malo pre nego što joj ga je zavukao. Iole neretardiran"
                         " gledalac ovde mora da se zbuni volumenom i kvalitetom njihovog odnosa pre ovog susreta. A tek će onim što sledi."
                         " Nakon toga, kako rat odmiče, Danijel će prvo skrivajući od svojih ratnih drugova krišom da brine o njoj,"
                         " da bi na kraju, kada se rat već primakne svom kraju, ona postala \"ekskluzivno njegova\", ali i predmet"
                         " ozbiljnih primedbi na račun čistote njegovog srpstva. Mi ćemo u međuvremenu saznati kakva je "
                         "stravična sudbina zadesila Ajlinu sestru (srpski paravojnici su njenu bebu bacili kroz prozor, "
                         "jer je glasno plakala), ali i to da je Danijel sin izvesnog Nebojše (Šerbedžija) koji je "
                         "osmišljen kao neki prototip generala Mladića, kao i da je njemu \"uniforma\" u krvi, a samim tim i sve"
                         " \"obaveze\" koje sa njom idu. Anđelinin film naizmenična je mešavina prikaza bezumnog terora srpskih "
                         "paravojnih formacija nad muslimanskim življem i melodramskih, arthausičnih, erotizovanih druženja Danijela"
                         " i Ajle u intimi njegove sve veće sobe. Nikakve prave drame, razvoja priče ili likova tu nema, "
                         "film jednostavno daje inserte iz hronološkog razvoja rata koji su na žlebovima različitih perioda "
                         "obično propraćeni nekim televizijskim ili radijskim prenosom koji, pre svega, inostranom gledaocu "
                         "daje presek situacije tj razvoja rata. Slike nasilja paravojnih formacija bile su najčešći i najveći"
                         " predmet (srpske) kritike. Srpski paravojnici siluju po ciči zimi već posle dvanaest minuta od početka"
                         " filma, ubrzo potom baciće bebu kroz prozor zgrade, ubijati civile koje isteruju iz njihovih domova, "
                         "koristiće otete žene kao živi štit u borbi protiv muslimanske vojske, iživljavaće se na najrazličitije "
                         "načine nad otetim Muslimankama, snajperima će gađati civile po Sarajevu... U Anđelininom nizu svih ovih"
                         " zala nema nikakve naročite gradacije, a sem u liku Danijela i donekle njegovog oca Nebojše nema ni nikakve "
                         "individualizacije ovih zlikovaca. Srpski zločini su kao nemački zločini u \"partizanskim filmovima\", "
                         "jedna difolt aktivnost koja se ne dovodi u pitanje i samim tim kod gledaoca ne proizvodi onu vrstu "
                         "zgražavanja i ljutine koju bi trebalo. Jedan od poslednjih susreta \"Nebojšine ekipe\" odvija se"
                         " u nekoj staroj vili sa visokim plafonima i sve izgleda kao replika nekog \"fajnal solušn dogovora\" "
                         "nacističke ekipe. Kao komentar i paralela to funkcioniše, ali jednodimenzionalnost u prikazivanju "
                         "srpske paravojske šteti filmskoj priči, uverljivosti ispričanog, a samim tim i svim onim željenim "
                         "konsekvencama, pre svega nacionalnom, srpskom preispitivanju. Ni ljubavna priča nije ništa bolja. "
                         "Ja sam se u nekom trenutku ponadao da će Anđelina stvar tako postaviti da dvoje ljudi koji su imali "
                         "nekakvu romansicu pre rata (ili se on baš ložio na nju) u vihoru rata počinje da, silom prilika, svoj "
                         "odnos doživljava kao bitniji i fatalnij nego što on zaista jeste, svako iz svojih pobuda- ona da se spasi,"
                         " a on da olakša savest. I da to na kraju kulminira trenutkom u kome se oni možda zaista zaljubljuju jedno u drugo,"
                         " ali tada je već prekasno za sve. Nažalost, ništa se od toga ne desi. Čak šta, Anđelina u nekim momentima oblikuje "
                         "tu priču prilično konfuzno i kontradiktorno (on ne zna da je ona imala izloženu sliku u lokalnom muzeju- pa kad "
                         "je onda slika tamo postavljena, ako ih je rat zatekao zajedno?...). Ako se Ajlina emocionlna i svaka druga"
                         " konfuznost još i može tumačiti kao očekivana ženska reakcija na jezive događaje, Danijel nije ništa drugo"
                         " nego psiho. On nije momak kome je rat nemio, a kako nam Anđelina kasnije kaže- on je u ratnim haranjima "
                         "čak nadmašio oca. A opet s druge strane mi ne vidimo ni šta je to u njemu što ga tera na zverstva, niti "
                         "gde se to on lično istakao. U njegovoj vezanosti za Ajlu ima previše neobjašnjene promaje tj sve se može"
                         " objasniti samo time da je on psihopata. Njegova lična kapitulacija na kraju filma nikako ne proizilazi iz lika, "
                         "već je pamfletska poruka same rediteljke \"šta su srpski paravojnici morali da urade\" na kraju (rata)."
                         " No, kako je i ona iznuđena i taj momenat deluje jezivo isforsirano i nema snagu da zatvori film. "
                         "Anđelina nije donela neki \"svoj\" pogled na rat, a naročito ne na onaj u Bosni. Osim ako povremeno "
                         "bujanje boja u totalima (nebo) i establišment kadrovima (zgrade) ne računate kao relevantan autorski "
                         "doprinos. S obzirom da je U zemlji krvi i meda, prema njenim rečima, trebalo da bude film koji "
                         "(kroz ljubavnu priču) prikazuje stradanje Muslimanki (a samim tim i svih žena) u ovom ratu, tim "
                         "ženama ona se nije pozabavila koliko zaslužuju. Sem Ajle i njene sestre (koja nije bila u logoru)"
                         " mi jedva da imamo izdiferencirano još neki ženski lik, njene patnje ili sudbinu. A paradoksalno,"
                         " prikazana nam je baš ona koja je, oprostite mi na cinizmu, u tom ratu uživala primijum tretman s "
                         "obzirom na okolnosti. Ono što mene buni jeste kako, recimo, Šerbedžija, koji je, navodno, i nekakav "
                         "Anđelinin prijatelj, po čitanju scenarija nije našao za shodno da joj ukaže na evidentne mane istog. "
                         "Konačno i njemu je poverena uloga flispapir tankog srpskog vorlorda koji je i u nekim jadnijim ekranizacijama"
                         " bosanskog rata bio bolje elaboriran od ovoga. A pitam se zašto su glave u pesak zabili i ostali srpski i"
                         " bosanski glumci koji su svakako bolje i više od Anđeline znali i šta se dešavalo i kako ono što je ona "
                         "zamislila može filmu (a ne srpskoj publici ili nekoj drugoj) da se obije o glavu. Ne kažem da je to bila "
                         "njihova obaveza, ali s obzirom na ambicije filma, beskrajno osetljivu tematiku i potencijalne konsekvence "
                         "(nije li nas Anđelinin film opet malo zaratio, a?), možda se moglo malo pomučiti zarad uspešnijeg ostvarenja "
                         "višeg cilja. U zemlji krvi i meda je film sa mnogo krvi i bez imalo meda, ali ono što je još bitnije- on "
                         "fundamentalno odbacuje ideju da se oni \"smiješano najlakše piju\".", result_2)


if __name__ == '__main__':
    unittest.main()
