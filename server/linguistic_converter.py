import warnings

from server.dictionary import Word
from server.utils import get_node_key, get_node_val


class LinguisticConverterPl:
    def __init__(self):
        self.czesc_mowy = {}
        self.rodzaj = {}
        self.przypadek = {}
        self.liczba = {}
        self.osoba = {}
        self.czas = {}
        self.column_names = {}
        # nazwa klucza w węźle z odmianą dla zadanego słowa w pliku polish_words.json
        self.pl_odmiana_name = {}

        self.define_przypadki()
        self.define_liczby()
        self.define_osoby()
        self.define_czasy()
        self.define_rodzaje()
        self.define_czesci_mowy()
        self.define_column_names()
        self.define_pl_odmiana_name()

    def get_pl_odmiana_name(self, czesc_mowy: str):
        odmiany_keys = list(self.pl_odmiana_name.keys())
        if czesc_mowy in odmiany_keys:
            return self.pl_odmiana_name[czesc_mowy]
        else:
            warnings.warn('Nieznana część mowy ' + str(czesc_mowy))

    def define_pl_odmiana_name(self):
        self.pl_odmiana_name["rzeczownik"] = "deklinacja"
        self.pl_odmiana_name["czasownik"] = "koniugacja"
        self.pl_odmiana_name["przymiotnik"] = "koniugacja"
        self.pl_odmiana_name["liczebnik"] = ""
        self.pl_odmiana_name["zaimek"] = ""
        self.pl_odmiana_name["przysłówek"] = ""
        self.pl_odmiana_name["przysłówek"] = ""
        self.pl_odmiana_name["wykrzyknik"] = ""
        self.pl_odmiana_name["przyimek"] = ""
        self.pl_odmiana_name["liczebnik"] = ""


    def get_column_name_for_attribute(self, attr: str):
        return self.column_names[attr]

    def get_liczba(self, word: Word):
        attr_in_raw_form = word.get_number()
        attr_converted = self.liczba[attr_in_raw_form]
        return attr_converted

    def define_column_names(self):
        self.column_names['przypadek'] = 'grammatical_case'
        self.column_names[
            'rodzaj'] = 'T.grammatical_gender'  ## dodane T. tak będziemy nazywać tabelę 'terms' podczas zapytań. Ta kolumna znajduje sie również w drugiej tabeli, dlatego niezbędne jest rozróżnienie
        self.column_names['czesc_mowy'] = 'grammatical_part_of_speech'
        self.column_names['osoba'] = 'grammatical_person'
        self.column_names['czas'] = 'grammatical_tense'
        self.column_names['liczba'] = 'grammatical_number'

    def czesc_mowy_str_to_num(self, czesc_mowy_str: str):
        n = len(self.czesc_mowy)
        for i in list(range(n)):
            if self.czesc_mowy[i] == czesc_mowy_str:
                return i
        return -1

    # reformat to fill requirements of polish_words.json
    def adjust_val_in_property_to_polish_words_json(self, attr):
        attr_key = get_node_key(attr)
        property = self.get_property_for_name(attr_key)
        if property == self.czesc_mowy:
            return self.conv_val_in_property_to_num(attr)
        elif property in [self.liczba, self.przypadek, self.osoba]:
            return self.conv_val_in_property_to_num(attr, as_str=True)
        elif property in [self.rodzaj, self.czas]:
            return self.conv_val_in_property_to_str(attr)
        else:
            warnings.warn('Nieznane property ' + str(attr))
            return None

    # last parametr indicate if convert value to str, ex. 1 -> "1"
    def conv_val_in_property_to_num(self, attr: {}, as_str=False):
        conv_attr_val = -1
        attr_key = get_node_key(attr)
        attr_val = get_node_val(attr)
        property = self.get_property_for_name(attr_key)
        property_available_num_list = list(property.keys())
        property_available_str_list = list(property.values())
        if attr_val in property_available_num_list:
            conv_attr_val = attr_val
        elif attr_val in property_available_str_list:
            for n in range(len(property_available_str_list)):
                if property[n] == attr_val:
                    conv_attr_val = n
                    break
        else:
            warnings.warn('Niedozwolona wartość ' + str(attr_val) + ' dla atrubutu ' + str(attr_key))
        if as_str:
            conv_attr_val = str(conv_attr_val)
        return {attr_key: conv_attr_val}

    # attr for example: {'czesc_mowy': "rzeczownik"}
    def conv_val_in_property_to_str(self, attr: {}):
        conv_attr_val = -1
        attr_key = get_node_key(attr)
        attr_val = get_node_val(attr)
        property = self.get_property_for_name(attr_key)
        property_available_num_list = list(property.keys())
        property_available_str_list = list(property.values())
        if attr_val in property_available_str_list:
            conv_attr_val = attr_val
        elif attr_val in property_available_num_list:
            conv_attr_val = property[attr_val]
        else:
            warnings.warn('Niedozwolona wartość ' + str(attr_val) + ' dla atrubutu ' + str(attr_key))
        return {attr_key: conv_attr_val}

    def get_property_for_name(self, attr: str):
        if attr == 'przypadek':
            return self.przypadek
        elif attr == 'rodzaj':
            return self.rodzaj
        elif attr == 'czesc_mowy':
            return self.czesc_mowy
        elif attr == 'osoba':
            return self.osoba
        elif attr == 'czas':
            return self.czas
        elif attr == 'liczba':
            return self.liczba
        else:
            warnings.warn('Nieznane property ' + str(attr))
            return None

    def get_czesci_mowy_mapper(self):
        return self.czesc_mowy

    def define_czesci_mowy(self):
        self.czesc_mowy[0] = "rzeczownik"
        self.czesc_mowy[1] = "czasownik"  # odmiana przez liczby, osoby, strony, czasy,
        self.czesc_mowy[2] = "przymiotnik"  # odmiana przez przypadki, liczby, rodzaje
        self.czesc_mowy[3] = "liczebnik"
        self.czesc_mowy[4] = "zaimek"
        self.czesc_mowy[6] = "przysłówek"
        self.czesc_mowy[7] = "przysłówek"
        self.czesc_mowy[10] = "wykrzyknik"  # ach, och, hej, oj, aj
        self.czesc_mowy[11] = "przyimek"  # nad, wśród, ponad, pod, z
        self.czesc_mowy[12] = "liczebnik"
        self.czesc_mowy[-1] = "inna"

    def define_czasy(self):
        self.czas[0] = "terazniejszy"
        self.czas[1] = "przeszly"
        self.czas[2] = "przyszly"

    def define_rodzaje(self):
        self.rodzaj[0] = "meski"
        self.rodzaj[1] = "zenski"
        self.rodzaj[2] = "nijaki"

    def define_osoby(self):
        self.osoba[0] = "ja"
        self.osoba[1] = "ty"
        self.osoba[2] = "on"
        self.osoba[3] = "ona"
        self.osoba[4] = "ono"
        self.osoba[5] = "my"
        self.osoba[6] = "wy"
        self.osoba[7] = "oni"

    def define_przypadki(self):
        self.przypadek[0] = "mianownik"
        self.przypadek[1] = "dopełniacz"
        self.przypadek[2] = "celownik"
        self.przypadek[3] = "biernik"
        self.przypadek[4] = "narzędnik"
        self.przypadek[5] = "miejscownik"
        self.przypadek[6] = "wołacz"

    def define_liczby(self):
        self.liczba[0] = 'pojedyncza'
        self.liczba[1] = 'mnoga'


class LinguisticConverterEng:
    def __init__(self):
        self.part_of_speech = {}  # rzecz, przym, itd.
        self.gender = {}  # rodzaj
        self.case = {}  # przypadki
        self.person = {}
        self.tense = {}  # czas
        self.number = {}  # l.poj, l.mnog

        self.define_part_of_speech()
        self.define_gender()
        self.define_case()
        self.define_person()
        self.define_tense()
        self.define_number()

    def get_number(self, word: Word):
        attr_in_raw_form = word.get_number()
        attr_converted = self.pl_number[attr_in_raw_form]
        return attr_converted

    def define_part_of_speech(self):
        self.part_of_speech[0] = "noun"
        self.part_of_speech[1] = "verb"
        self.part_of_speech[2] = "adjective"
        self.part_of_speech[3] = "numeral"  # liczebnik
        self.part_of_speech[4] = "pronoun"  # zaimek
        self.part_of_speech[6] = "adverb"  # przysłówek

    def define_gender(self):
        self.gender[0] = "masculine"
        self.gender[1] = "feminine"
        self.gender[2] = "neuter"

    # grammatical_case
    def define_case(self):
        self.case[0] = "nominative"  # mianownik
        self.case[1] = "genitive"  # dopełniacz
        self.case[2] = "dative"  # celownik
        self.case[3] = "accusative"  # biernik
        self.case[4] = "instrumental"  # narzędnik
        self.case[5] = "locative"  # miejscownik
        self.case[6] = "vocative"  # wołacz

    def define_person(self):
        self.person[0] = "I"
        self.person[1] = "You"
        self.person[2] = "He"
        self.person[3] = "She"
        self.person[4] = "It"
        self.person[5] = "We"
        self.person[6] = "You"
        self.person[7] = "They"

    def define_tense(self):
        self.tense[0] = "present"
        self.tense[1] = "past"
        self.tense[2] = "future"

    def define_number(self):
        self.number[0] = 'singuar'
        self.number[1] = 'plural'
