import itertools
import re
import warnings
from pathlib import Path

import os

import requests
from bs4 import BeautifulSoup

from server import polish_word_generator_2_rzeczownik
from server.dict_initializers import init_polish_word_przymiotnik, init_polish_word_czasownik, init_polish_word_rzeczownik, \
    init_polish_word_przyslowek, init_polish_word_zaimek, init_polish_word_inny
from server.utils import get_polish_base_forms_from_json_file, save_polish_word_to_file, format_text

wiki_base = "https://pl.wiktionary.org/wiki/"
html_wiki_dir = "html_wiki/"
przyslowek_numer = 11
col_r_meski = 0
col_r_zenski = 2
col_r_nijaki = 3
col_meski_l_mnog = 4
col_zenski_l_mnog = 5
czas_terazniejszy = {"wiki": "czas teraźniejszy", "json": "terazniejszy"}
czas_przeszly = {"wiki": "czas przeszły", "json": "przeszly"}
czas_przyszly = {"wiki": "czas przyszły", "json": "przyszly"}
rodzaje = {0: 'meski', 1: 'zenski', 2: 'nijaki'}
przypadki = ["mianownik", "dopełniacz", "celownik", "biernik", "narzędnik", "miejscownik", "wołacz"]


def fetch_html_for_word(word: str):
    fetch_html(wiki_base + word)


def fetch_html(url: str):
    page = requests.get(url)
    filename = url.split('/')[-1] + ".html"
    with open(html_wiki_dir + filename, 'wb') as f:
        f.write(page.text.encode('utf8'))


def load_html_file_for_word(word: str):
    with open(html_wiki_dir + word + ".html", 'rb') as f:
        soup = BeautifulSoup(f, "lxml")
    return soup


def does_file_exist(word: str):
    filename = Path(html_wiki_dir + word + ".html")
    return filename.is_file()


def get_soup_for_word(word: str) -> BeautifulSoup:
    if not does_file_exist(word):
        fetch_html_for_word(word)
    return load_html_file_for_word(word)


def find_row_elements(row_title, table):
    elements = []
    for td in table.find(title=row_title).parent.parent.findAll('td')[1:]:
        if td.has_attr('colspan'):
            n = td['colspan']
            elements = list(itertools.chain(elements, [td.string] * int(n)))
        else:
            elements = list(itertools.chain(elements, [td.string]))
    return elements


def find_row_elements_for_czasownik(row_title, table, rodzaj_num=-1):
    elements = []
    try:
        if row_title == "czas teraźniejszy":
            tr = table.find(title=row_title).parent.parent
            elements = [td.get_text() for td in tr.findAll('td')]
        elif row_title == "czas przeszły":
            rodzaj_str = rodzaje[rodzaj_num]
            elements = get_texts_from_tr(table, rodzaj_str, row_title)
        elif row_title == "czas przyszły":
            table = table.find_next('table')
            rodzaj_str = rodzaje[rodzaj_num]
            elements = get_texts_from_tr(table, rodzaj_str, row_title)
    except Exception:
        warnings.warn('Nie znaleziono odmiany czasownika dla zadanego czasu')
        return []
    return elements


def get_texts_from_tr(table, rodzaj, czas):
    tr_meski = table.find(title=czas).parent.parent
    tr_zenski = tr_meski.find_next("tr")
    tr_nijaki = tr_zenski.find_next("tr")
    if rodzaj == 'nijaki':
        element = tr_nijaki.findAll('td')[2]
        if czas == "czas przeszły":
            elements = [element.get_text()]
        elif czas == "czas przyszły":
            elements = element.get_text().replace(',', '').splitlines()
        return elements

    if rodzaj == "zenski":
        tr = tr_zenski
    else:
        tr = tr_meski
    if czas == "czas przeszły":
        elements = [td.get_text() for td in tr.findAll('td')]
    elif czas == "czas przyszły":
        elements = [td.get_text().replace(',', '').splitlines() for td in tr.findAll('td')]
    return elements


def declination_rzeczownik_first_column(table):
    return declination_rzeczownik(0, table)


def declination_rzeczownik_second_column(table):
    try:
        result = declination_rzeczownik(1, table)
    except:
        warnings.warn('Second column for this word is not set on wikipedia')
        result = {}
    return result


def declination_rzeczownik(liczba: int, table):
    decl = [find_row_elements(p, table)[liczba] for p in przypadki]
    decl_dict = zip_nums_with_values(decl)
    return decl_dict


def deklinacja_meski(table):
    return deklinacja_dla_rodzaju_num(col_r_meski, table)


def deklinacja_zenski(table):
    return deklinacja_dla_rodzaju_num(col_r_zenski, table)


def deklinacja_nijaki(table):
    return deklinacja_dla_rodzaju_num(col_r_nijaki, table)


def deklinacja_meski_l_mnoga(table):
    return deklinacja_dla_rodzaju_num(col_meski_l_mnog, table)


def deklinacja_zenski_l_mnoga(table):
    return deklinacja_dla_rodzaju_num(col_zenski_l_mnog, table)


def deklinacja_dla_rodzaju_num(rodzaj: int, table):
    decl = [find_row_elements(przypadki[i], table)[rodzaj] for i in range(0, 7)]
    return decl


def deklinacja_dla_rodzaju_str(rodzaj_str: str, table):
    rodzaje = {'meski': col_r_meski, 'zenski': col_r_zenski, 'nijaki': col_r_nijaki}
    return deklinacja_dla_rodzaju_num(rodzaje[rodzaj_str], table)


def do_next_word(word, polish_words={}):
    polish_words = get_polish_base_forms_from_json_file()
    if not word:
        print('Puste słowo')
        return 0
    if word not in polish_words:
        print('Pobieramy dane o słowie ' + word)
        html = get_soup_for_word(word)
        if not is_word_described(word, html):
            remove_html_for_word(word)
            return polish_word_generator_2_rzeczownik.do_next_word(word)
        table = get_table(html)
        czesc_mowy = get_word_czesc_mowy_from_wiki(word, html)
        if not table:
            remove_html_for_word(word)
            if czesc_mowy == "rzeczownik":
                return polish_word_generator_2_rzeczownik.do_next_word(word)
            else:
                polish_word = do_inny(word)
                save_polish_word_to_file(polish_word)
                return 0
        polish_word = {}
        if czesc_mowy == "przymiotnik":
            polish_word = do_przymiotnik(word, html)
        elif czesc_mowy == "czasownik":
            polish_word = do_czasownik(word, html)
        elif czesc_mowy == "rzeczownik":
            polish_word = do_rzeczownik(word, html)
        elif czesc_mowy == "liczebnik":
            polish_word = do_liczebnik(word, html)
        elif czesc_mowy == "przysłówek":
            polish_word = do_przyslowek(word, html)
        elif czesc_mowy == "zaimek":
            polish_word = do_zaimek(word)
        print(polish_word)
        if save_polish_word_to_file(polish_word):
            return True
    else:
        print('Już znam słowo ' + word)

def do_inny(word):
    polish_word = init_polish_word_inny(word)
    return polish_word

def do_zaimek(word):
    polish_word = init_polish_word_zaimek(word)
    return polish_word

def do_przyslowek(word, html: BeautifulSoup):
    polish_word = init_polish_word_przyslowek(word)
    polish_word[word]['stopnie'].update(przyslowek_stopniowanie(word, html))
    return polish_word


def przyslowek_stopniowanie(word: str, html):
    upd = {}
    try:
        st_wyzszy = html.find('span', title='stopień wyższy').parent.parent.nextSibling
        st_wyzszy = format_text(st_wyzszy)
        if st_wyzszy:
            upd[1] = st_wyzszy
        st_najwyzszy = html.find('span', title='stopień najwyższy').parent.parent.nextSibling
        st_najwyzszy = format_text(st_najwyzszy)
        if st_najwyzszy:
            upd[2] = st_najwyzszy
    except Exception:
        warnings.warn('Błąd w stopniowaniu przysłówka')
    return upd

def do_liczebnik(word, html):
    return do_rzeczownik(word, html)


def do_rzeczownik(word, html):
    polish_word = init_polish_word_rzeczownik(word)
    try:
        table_l_poj = get_table_l_poj_for_rzeczownik(html)
    except:
        warnings.warn('Failed fetching data for word ' + word)
        try:
            table_l_mnog = get_table_l_mnog_for_rzeczownik(html)
        except:
            warnings.warn('Failed fetching data for word ' + word)
            return polish_word

    table_l_mnog = get_table_l_mnog_for_rzeczownik(html)
    if table_l_poj == table_l_mnog or not table_l_mnog :
        polish_word = do_rzeczownik_for_one_table(polish_word, table_l_poj)
    else:
        polish_word = do_rzeczownik_for_two_tables(polish_word, table_l_poj, table_l_mnog)
    return polish_word


def do_rzeczownik_for_one_table(polish_word, table):
    word = get_word_from_dict_element(polish_word)
    polish_word[word]['deklinacja'][0] = declination_rzeczownik_first_column(table)
    polish_word[word]['deklinacja'][1] = declination_rzeczownik_second_column(table)
    return polish_word


def do_rzeczownik_for_two_tables(polish_word, table_poj, table_mnog):
    word = get_word_from_dict_element(polish_word)
    polish_word[word]['deklinacja'][0] = declination_rzeczownik_first_column(table_poj)
    polish_word[word]['deklinacja'][1] = declination_rzeczownik_first_column(table_mnog)
    return polish_word


def get_table_l_poj_for_rzeczownik(html):
    return html.find('th', text="liczba pojedyncza").find_parent('table')


def get_table_l_mnog_for_rzeczownik(html):
    try:
        return html.find('th', text="liczba mnoga").find_parent('table')
    except Exception:
        return None


def do_przymiotnik(word, html):
    table = get_table_rowny(html)
    table_wyzszy = get_table_wyzszy(html)
    table_najwyzszy = get_table_najwyzszy(html)
    polish_word = init_polish_word_przymiotnik(word)
    polish_word = do_declination_przymiotnik(polish_word, table, 'rowny')
    if table_wyzszy != None:
        polish_word = do_declination_przymiotnik(polish_word, table_wyzszy, 'wyzszy')
        if table_najwyzszy != None:
            polish_word = do_declination_przymiotnik(polish_word, table_najwyzszy, 'najwyzszy')
    return polish_word


def get_table_najwyzszy(soup):
    table = get_table_rowny(soup)
    if len(table.find_all('table')) < 1:
        return None
    else:
        return table.find_all('table')[1]


def get_table_wyzszy(soup):
    table = get_table_rowny(soup)
    if len(table.find_all('table')) == 0:
        return None
    else:
        return table.find_all('table')[0]


def get_table_rowny(soup):
    return get_table(soup)


def get_table(soup):
    table = soup.find("table", attrs={"class": "odmiana"})
    return table


def do_declination_przymiotnik(polish_word, table, stopien):
    polish_word = declination_przymiotnik_step('meski', table, 0, stopien, polish_word)
    polish_word = declination_przymiotnik_step('zenski', table, 0, stopien, polish_word)
    polish_word = declination_przymiotnik_step('nijaki', table, 0, stopien, polish_word)
    polish_word = declination_przymiotnik_step('meski', table, 1, stopien, polish_word)
    polish_word = declination_przymiotnik_step('zenski', table, 1, stopien, polish_word)
    return polish_word


def declination_przymiotnik_step(rodzaj_str: str, table, liczba, stopien, polish_word):
    if liczba == 1:
        if rodzaj_str == 'meski':
            conj = deklinacja_meski_l_mnoga(table)
        elif rodzaj_str == 'zenski':
            conj = deklinacja_zenski_l_mnoga(table)
    else:
        conj = deklinacja_dla_rodzaju_str(rodzaj_str, table)
    dict_conj = {liczba: zip_nums_with_values(conj)}
    word = get_word_from_dict_element(polish_word)
    polish_word[word]['deklinacja'][rodzaj_str][stopien].update(dict_conj)
    return polish_word


def do_czasownik(word, html):
    polish_word = init_polish_word_czasownik(word)
    table = get_table(html)
    update = do_conj_czasownik_terazniejszy(table)
    polish_word = update_polish_word_czasownik(polish_word, update)
    update = do_conj_czasownik_przeszly(table)
    polish_word = update_polish_word_czasownik(polish_word, update)
    update = do_conj_czasownik_przyszly(table)
    polish_word = update_polish_word_czasownik(polish_word, update)
    return polish_word


def update_polish_word_czasownik(polish_word: {}, new_node: {}):
    word = get_word_from_dict_element(polish_word)
    polish_word[word]['koniugacja'].update(new_node)
    return polish_word


def do_conj_czasownik_terazniejszy(table):
    conj = do_conj_czasownik(czas_terazniejszy['wiki'], table)
    update = {'terazniejszy': conj}
    return update


def do_conj_czasownik_przeszly(table):
    conj_meski = do_conj_czasownik(czas_przeszly['wiki'], table, 0)
    conj_zenski = do_conj_czasownik(czas_przeszly['wiki'], table, 1)
    conj_nijaki = do_conj_czasownik(czas_przeszly['wiki'], table, 2)
    update = {'przeszly': {'meski': conj_meski, 'zenski': conj_zenski, 'nijaki': conj_nijaki}}
    return update


def do_conj_czasownik_przyszly(table):
    conj_meski = do_conj_czasownik(czas_przyszly['wiki'], table, 0)
    conj_zenski = do_conj_czasownik(czas_przyszly['wiki'], table, 1)
    conj_nijaki = do_conj_czasownik(czas_przyszly['wiki'], table, 2)
    update = {'przyszly': {'meski': conj_meski, 'zenski': conj_zenski, 'nijaki': conj_nijaki}}
    return update


def do_conj_czasownik(czas, table, rodzaj=-1):
    odmiana = find_row_elements_for_czasownik(czas, table, rodzaj)
    conj = zip_nums_with_values(odmiana)
    return conj


def zip_nums_with_values(values):
    n = len(values) + 1
    return dict(list(zip(range(0, n), values)))


def get_word_czesc_mowy_from_wiki(word: str, html):
    if not is_word_described(word, html):
        return 0
    description = ""
    description = html.find("span", text="znaczenia:").find_next("p").text
    # description = " ".join([el.text for el in html.find_all("p")])
    if description.find("przymiotnik") != -1 and description.find("czasownik") != -1:
        return "przymiotnik"
    elif description.find("rzeczownik") != -1:
        return "rzeczownik"
    elif description.find("przymiotnik") != -1:
        return "przymiotnik"
    elif description.find("czasownik") != -1:
        return "czasownik"
    elif description.find("zaimek") != -1:
        return "zaimek"
    elif description.find("spójnik") != -1:
        return "spójnik"
    elif description.find("liczebnik") != -1:
        return "liczebnik"
    elif description.find("przysłówek") != -1:
        return "przysłówek"
    else:
        return "inny"


def is_word_described(word: str, html):
    if html.find(string=re.compile("W Wikisłowniku nie ma jeszcze hasła")):
        return False
    else:
        print('Słowo ' + word + ' jest w wikisłowniku.')
        return True


def get_word_from_dict_element(word_as_dict: {}):
    return list(word_as_dict.keys())[0]


def remove_html_for_word(word: str):
    filename = html_wiki_dir + word + ".html"
    os.remove(filename)


def do_next_words(words: []):
    try:
        polish_words = get_polish_base_forms_from_json_file()
        for word in words:
            try:
                do_next_word(word, polish_words)
            except Exception:
                warnings.warn('Nie udało się dodać opisu dla słowa ' + str(word))
        return True
    except Exception:
        warnings.warn('Executing do_next_words raisе an exception')
        return False

# word = "moja"
# print(do_next_words())
