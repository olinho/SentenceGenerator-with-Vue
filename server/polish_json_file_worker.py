import json
import warnings

from server.utils import is_node_set, get_node_key, polish_json_filename

czasy = {0: 'terazniejszy', 1: 'przeszly', 2: 'przyszly'}
rodzaje = {0: 'meski', 1: 'zenski', 2: 'nijaki'}
stopnie = {0: 'rowny', 1: 'wyzszy', 2: 'najwyzszy'}


def get_polish_dict():
    with open(polish_json_filename, "r", encoding="utf8") as file:
        polish_dict = json.load(file)
    return polish_dict


polish_dict = get_polish_dict()


def get_polish_base_forms(p_dict=polish_dict):
    polish_dict = get_polish_dict()
    return [key.lower() for key in p_dict.keys()]


def get_polish_word(base_form: str):
    polish_dict = get_polish_dict()

    for key, value in polish_dict.items():
        if list(key)[0] == base_form:
            return {base_form: value}
    return {base_form: {}}


def get_odmiany_based_on_description(description: {}):
    polish_dict = get_polish_dict()
    polish_form = get_word_from_description(description)
    # when word is empty - because of lack of polish translation
    if not polish_form:
        warnings.warn('Nieznane tłumaczenie')
        return ['']
    czesc_mowy = ''
    if len(list(description[polish_form])) > 0:
        czesc_mowy = description[polish_form]['czesc_mowy']
    odmiany = []
    try:
        if czesc_mowy == "rzeczownik" or czesc_mowy == 0:
            odmiany = get_odmiany_based_on_rzeczownik_description(description)
        elif czesc_mowy == "czasownik" or czesc_mowy == 1:
            odmiany = get_odmiany_based_on_czasownik_description(description)
        elif czesc_mowy == "przymiotnik" or czesc_mowy == 2:
            odmiany = get_odmiany_based_on_przymiotnik_description(description)
    except:
        warnings.warn('Not set details for word ' + str(polish_form))
    if len(odmiany) == 0:
        odmiany = [polish_form]
    return odmiany


def get_odmiany_based_on_rzeczownik_description(description: {}):
    odmiany = []
    polish_form = get_word_from_description(description)
    for descr in description[polish_form]['formy']:
        odmiana = ''
        if descr == '':
            break
        liczba = str(descr['liczba'])
        przypadek_num = str(descr['przypadek'])
        odmiana = polish_dict[polish_form]['deklinacja'][liczba][przypadek_num]
        odmiany.append(odmiana)
    return odmiany


def get_odmiany_based_on_czasownik_description(description: {}):
    odmiany = []
    polish_form = get_word_from_description(description)
    for descr in description[polish_form]['formy']:
        odmiana = ''
        if descr == '':
            break
        czas_num = descr['czas']
        czas_str = czasy[czas_num]
        osoba_num = str(descr['osoba'])
        # dla czasu terazniejszego jest tylko jeden rodzaj, więc go pomijamy w zmiennej description
        if czas_num == 0:
            if is_node_set(polish_dict[polish_form]['koniugacja'][czas_str]):
                odmiana = polish_dict[polish_form]['koniugacja'][czas_str][str(osoba_num)]
                print(odmiana)
        else:
            rodzaj_num = descr['rodzaj']
            rodzaj_str = rodzaje[rodzaj_num]
            if is_node_set(polish_dict[polish_form]['koniugacja'][czas_str][rodzaj_str]):
                odmiana = polish_dict[polish_form]['koniugacja'][czas_str][rodzaj_str][str(osoba_num)]
                if type(odmiana) is list:
                    odmiana = odmiana[0]
        if odmiana:
            odmiany.append(odmiana)
    return odmiany


def get_odmiany_based_on_przymiotnik_description(description: {}):
    odmiany = []
    polish_form = get_word_from_description(description)
    for descr in description[polish_form]['formy']:
        if descr == '':
            break
        # default value stopien=rowny
        if descr['stopien'] == None:
            stopien_num = 0
        else:
            stopien_num = descr['stopien']
        rodzaj_num = descr['rodzaj']
        liczba_num = descr['liczba']
        przypadek_num = descr['przypadek']
        rodzaj_str = rodzaje[rodzaj_num]
        stopien_str = stopnie[stopien_num]
        liczba_str = str(liczba_num)
        przypadek_str = str(przypadek_num)
        res = polish_dict[polish_form]['deklinacja'][rodzaj_str][stopien_str][liczba_str][przypadek_str]
        odmiana = get_one_element(res)
        odmiany.append(odmiana)
    return odmiany


# if all elements set num_of_elements = -1
def get_base_forms_for_czesc_mowy(czesc_mowy: int, num_of_elements=10):
    words = []
    n = 0
    for word, descr in polish_dict.items():
        if get_czesc_mowy_from_descr(descr) == czesc_mowy:
            words.append(word)
            n += 1
            if n == num_of_elements:
                break
    return words


def get_czesc_mowy_from_descr(descr: {}):
    if "czesc_mowy" in descr:
        return descr["czesc_mowy"]
    else:
        warnings.warn('Czesc mowy nie jest ustawiona w opisie.')
        return ""


# return first element from list or just element
def get_one_element(arr):
    if type(arr) is list:
        odmiana = arr[0]
    else:
        return arr


def get_word_from_description(dict_el: {}):
    return list(dict_el.keys())[0]


# descr = {'jechać': {'czesc_mowy': 'czasownik', 'formy': [{'czas': 1, 'osoba': 5}]}}
descr = {'zajęty': {'czesc_mowy': 'przymiotnik', 'formy': [{'rodzaj': 0, 'stopien': 0, 'liczba': 0, 'przypadek': 3}]}}
# print(get_odmiany_based_on_description(descr))
