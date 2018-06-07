import json
import warnings

from server.lemko_words_and_variations import LemkoWordsAndVariations

czasy = {0: 'terazniejszy', 1: 'przeszly', 2: 'przyszly'}
rodzaje = {0: 'meski', 1: 'zenski', 2: 'nijaki'}
stopnie = {0: 'rowny', 1: 'wyzszy', 2: 'najwyzszy'}


def get_lemko_dict():
    lemko_dict = {}
    with open("data/lemko_words.json", "r", encoding="utf8") as file:
        lemko_dict = json.load(file)
    return lemko_dict


lemko_dict = get_lemko_dict()


def get_lemko_words(dict=lemko_dict):
    dict = get_lemko_dict()
    return [key.lower() for key in dict.keys()]


def get_nouns(dict=lemko_dict):
    return get_words_from_part_of_speech(0, dict=dict)


def get_verbs(dict=lemko_dict):
    return get_words_from_part_of_speech(1, dict=dict)


def get_adjectives(dict=lemko_dict):
    return get_words_from_part_of_speech(2, dict=dict)


def get_words_from_part_of_speech(part_of_speech, dict=lemko_dict):
    lem_words = get_lemko_words(dict)
    return [word for word in lem_words if dict[word]['czesc_mowy'] == part_of_speech]


def get_translations(words: []):
    translations = [get_translation(word) for word in words]
    return translations


def get_first_word_from_text(str_with_delim_comma: str):
    words = str_with_delim_comma.strip().split(",")
    return words[0]


def get_translation(lem_word: str):
    lemko_dict = get_lemko_dict()
    try:
        translation = lemko_dict[lem_word]['tlumaczenie']
        first_translation = get_first_word_from_text(translation)
        return first_translation
    except Exception:
        warnings.warn('Brak tłumaczenia dla słowa ' + str(lem_word))

# ld is instance of LemkoWordsAndVariations
def get_word_description(word: str, ld=None):
    if not ld:
        ld = LemkoWordsAndVariations()
    base_form = ld.get_base_form(word)
    # TODO błąd, bo pobieramy informację o słowie z lemko_dictionary.json,
    # a potem odnosimy się do lemko_words.json
    if base_form != '':
        try:
            czesc_mowy = lemko_dict[base_form]['czesc_mowy']
        except Exception:
            warnings.warn('Czesc mowy dla słowa ' + str(base_form) + ' nie jest ustalona.')
            czesc_mowy = -1
        description = {}
        if czesc_mowy == 0:
            description = get_rzeczownik_description(word, base_form)
        elif czesc_mowy == 1:
            description = get_czasownik_description(word, base_form)
        elif czesc_mowy == 2:
            description = get_przymiotnik_description(word, base_form)
        elif czesc_mowy == 6:
            description = get_przyslowek_description(base_form)
        else:
            description = {get_translation(base_form): {}}
            # todo
    else:
        warnings.warn('Brak opisu dla słowa ' + str(word))
        description = {get_translation(word): {}}
    return description


def get_przymiotnik_description(word, base_form):
    word_node = lemko_dict[base_form]
    polish_form = get_translation(base_form)
    description = {polish_form: {"czesc_mowy": 'przymiotnik', "formy": []}}
    for stopien_num in stopnie.keys():
        stopien_str = stopnie[stopien_num]
        for rodzaj_num in rodzaje.keys():
            rodzaj_str = rodzaje[rodzaj_num]
            try:
                for liczba_num, odmiany_node in word_node['deklinacja'][rodzaj_str][stopien_str].items():
                    if odmiany_node:
                        for odmiana_num, odmiana_val in odmiany_node.items():
                            if odmiana_val == word:
                                description[polish_form]['formy'].append(
                                    {'rodzaj': rodzaj_num, 'stopien': stopien_num, 'liczba': int(liczba_num),
                                     'przypadek': odmiana_num})
            except Exception:
                print('Brak danych')
                return description
    return description


def get_czasownik_description(word, base_form):
    word_node = lemko_dict[base_form]
    polish_form = get_translation(base_form)
    description = {polish_form: {"czesc_mowy": 'czasownik', 'formy': []}}
    czas_num = 0
    czas_str = czasy[czas_num]
    for osoba_num, odmiana in word_node['koniugacja'][czas_str].items():
        if odmiana == word:
            description[polish_form]['formy'].append({'czas': czas_num, 'osoba': int(osoba_num)})
    for czas_num in [1, 2]:
        czas_str = czasy[czas_num]
        for rodzaj_num in rodzaje.keys():
            rodzaj_str = rodzaje[rodzaj_num]
            for osoba_num, odmiana in word_node['koniugacja'][czas_str][rodzaj_str].items():
                if odmiana == word:
                    description[polish_form]['formy'].append(
                        {'czas': czas_num, 'osoba': int(osoba_num), 'rodzaj': rodzaj_num})
    return description


def get_przyslowek_description(base_form):
    polish_form = get_translation(base_form)
    description = {polish_form: {"czesc_mowy": 'przyslowek', 'tlumaczenie': ''}}
    return description


def get_rzeczownik_description(word: str, base_form):
    word_node = lemko_dict[base_form]
    polish_form = get_translation(base_form)
    description = {polish_form: {"czesc_mowy": 'rzeczownik', 'formy': []}}
    for przypadek_num, odmiana in word_node['deklinacja']['0'].items():
        if odmiana == word:
            description[polish_form]['formy'].append({'liczba': 0, 'przypadek': int(przypadek_num)})
    for przypadek_num, odmiana in word_node['deklinacja']['1'].items():
        if odmiana == word:
            description[polish_form]['formy'].append({'liczba': 1, 'przypadek': int(przypadek_num)})
    return description


def get_descriptions_for_words(words: []):
    word_descriptions = [get_word_description(word) for word in words]
    return word_descriptions


def get_words_according_to_specification(spec: {}):
    czesc_mowy = spec['czesc_mowy']
    # todo
    filter(lambda x: x['czesc_mowy'] == 0 and lemko_dict)

# word = "поле"
# print(get_word_description(word))
# print(get_descriptions_for_words([word, 'коровы', 'вертеп']))
