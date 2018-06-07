import random
import warnings

from server.linguistic_converter import LinguisticConverterPl
from server.polish_json_file_worker import get_polish_dict, get_base_forms_for_czesc_mowy
from server.WordPattern import patterns, WordPattern
from server.utils import get_polish_base_forms_from_json_file, get_node_key

polish_base_forms = get_polish_base_forms_from_json_file()
polish_dict = get_polish_dict()


class PolishSentenceGenerator:
    def __init__(self):
        self.pattern_history = []
        self.pl_converter = LinguisticConverterPl()
        self.polish_dict = get_polish_dict()

    def append_pattern(self, pattern):
        self.pattern_history.append(pattern)
        return self

    def append_pattern_from_description(self, descr: {}, pattern_number=0):
        base_form = get_node_key(descr)
        if base_form == '':
            return -1
        else:
            form = descr[base_form]['formy'][pattern_number]
            czesc_mowy_str = descr[base_form]
            czesc_mowy_num = self.pl_converter.czesc_mowy_str_to_num(czesc_mowy_str)
            pattern = WordPattern({"czesc_mowy": czesc_mowy_num, "odmiana": form})
            self.append_pattern(pattern)
        return self

    def add_pattern_on_index(self, pattern: WordPattern, index=-1):
        if index == -1:
            self.append_pattern(pattern)
        elif index == 0:
            self.pattern_history = [pattern] + self.pattern_history
        else:
            self.pattern_history = self.pattern_history[0:index - 1] + [pattern] + self.pattern_history[index:]

    def search_words_for_pattern(self, pattern: WordPattern, n=1):
        czesc_mowy_num = pattern.get_czesc_mowy_num()
        words_for_czesc_mowy = get_base_forms_for_czesc_mowy(czesc_mowy=czesc_mowy_num)
        try:
            words_for_czesc_mowy = random.sample(words_for_czesc_mowy, n)
        except Exception:
            warnings.warn('d')
        description = pattern.get_odmiana_adjusted_to_polish_word_json()
        odmiana_node_name = pattern.get_odmiana_node_key_name()
        res = []
        i = 0
        # TODO rozdzielić na różne części mowy
        if czesc_mowy_num == 0:
            for base_word in words_for_czesc_mowy:
                try:
                    word_odmienione = self.polish_dict[base_word][odmiana_node_name][description['liczba']][description['przypadek']]
                    if word_odmienione != '':
                        res.append(word_odmienione)
                        i += 1
                        if i == n:
                            break
                except Exception:
                    warnings.warn('Brak odmiany dla zadanego opisu.')
                    continue
        elif czesc_mowy_num == 1:
            for base_word in words_for_czesc_mowy:
                try:
                    if description['czas'] == "terazniejszy":
                        word_odmienione = self.polish_dict[base_word][odmiana_node_name][description['czas']][description['osoba']]
                    else:
                        word_odmienione = self.polish_dict[base_word][odmiana_node_name][description['czas']][description['rodzaj']][description['osoba']]
                    if word_odmienione != '':
                        res.append(word_odmienione)
                        i += 1
                        if i == n:
                            break
                except Exception:
                    warnings.warn('Brak odmiany dla zadanego opisu.')
                    continue
        elif czesc_mowy_num == 2:
            for base_word in words_for_czesc_mowy:
                try:
                    word_odmienione = self.polish_dict[base_word][odmiana_node_name][description['rodzaj']][description['stopien']][description['liczba']][description['przypadek']]
                    if word_odmienione != '':
                        res.append(word_odmienione)
                        i += 1
                        if i == n:
                            break
                except Exception:
                    warnings.warn('Brak odmiany dla zadanego opisu.')
                    continue
        elif czesc_mowy_num == -1:
            num_of_words = len(words_for_czesc_mowy)
            if num_of_words > n:
                indx_list = random.sample(range(num_of_words), n)
                res = [words_for_czesc_mowy[indx] for indx in indx_list]
            else:
                res = words_for_czesc_mowy
        else:
            num_of_words = len(words_for_czesc_mowy)
            if num_of_words > n:
                indx_list = random.sample(range(num_of_words), n)
                res = [words_for_czesc_mowy[indx] for indx in indx_list]
            else:
                res = words_for_czesc_mowy
        return res


psg = PolishSentenceGenerator()
# p1 = WordPattern({"czesc_mowy": 0, "odmiana": {"liczba": 0, "przypadek": 2}})
# print(WordPattern(p1).get_examples())
# psg.append_pattern({"czesc_mowy": 0, "odmiana": {"liczba": 0, "przypadek": 2}})\
#     .append_pattern({"czesc_mowy": 1, "odmiana": {"czas": 1, "rodzaj": 0,  "osoba": 2}})

for p in patterns[0]:
    psg.append_pattern(p)

# TODO - błędy przy pobieraniu słów. Pobiera również formy bazowe, gdy nie ma zadanego tłumaczenia
# TODO chcemy uniknąć takich przypadków i ograniczyć się do słów, dla których faktycznie istnieje tłumaczenie
p2 = WordPattern({'czesc_mowy': 0, "odmiana": {'rodzaj': 1, 'liczba': 0, 'przypadek': 4}})
p3 = WordPattern({'czesc_mowy': 1, "odmiana": {'czas': 0, 'osoba': 2, 'rodzaj': 0}})
print(p3)
print(psg.search_words_for_pattern(p3))
print(p2)
print(psg.search_words_for_pattern(p2))

list_of_patterns = patterns[1]
out = []

for p in patterns[1]:
    print(psg.search_words_for_pattern(p))
