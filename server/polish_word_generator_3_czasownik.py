# **********************************
# na tej stronie jest wiele błędów,
# słowa są generowane przypuszczalnie wedle wzoru, a nie z bazy
# z tego względu nie korzystamy z tego pliku
# **********************************

# word scrapper for verbs
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from server.dict_initializers import init_polish_word_czasownik
from server.utils import get_polish_base_forms_from_json_file, zip_nums_with_values, get_values_from_index

site_base = "http://aztekium.pl/osoby.py?tekst="
html_odmiana_net_dir = "html_odmiana_czasownikow/"

def fetch_html_for_word(word: str):
    fetch_html(site_base + word)

def fetch_html(url: str):
    page = requests.get(url)
    page.encoding = 'utf-8'
    filename = url.split('=')[-1] + ".html"
    with open(html_odmiana_net_dir + filename, 'wb') as f:
        f.write(page.text.encode('utf8'))

def load_html_file_for_word(word: str):
    with open(html_odmiana_net_dir + word + ".html", 'rb') as f:
        soup = BeautifulSoup(f, "lxml")
    return soup

def does_file_exist(word: str):
    filename = Path(html_odmiana_net_dir + word + ".html")
    return filename.is_file()

def get_soup_for_word(word: str, reload=False):
    if not does_file_exist(word) or reload:
        print('Pobieramy dane o słowie ' + word + ' ze strony ' + site_base + word)
        fetch_html_for_word(word)
    return load_html_file_for_word(word)

def get_form(html):
    return html.find('form')



def is_word_described(word: str, html):
    if not html.find(string=re.compile("Nie podano bezokolicznika!")):
       return True
    else:
        return False

def get_word_variations(word: str, reload=False):
    html = get_soup_for_word(word, reload)
    cells = html.find_all("td", {'bgcolor': "#e0e0e0"})
    variations = []
    for cell in cells:
        if cell.find("b"):
            variations.append(cell.find("b").text)
        else:
            variations.append('')
    return variations

def do_czasownik(word, reload=False):
    if is_word_described(word, get_soup_for_word(word)):
        print('Kompletujemy dane o czasowniku z użyciem strony ' + site_base + word)
        polish_word = init_polish_word_czasownik(word)
        variations = get_word_variations(word, reload)
        update = do_conj_przeszly(variations)
        polish_word = update_polish_word_czasownik(polish_word, update)
        update = do_conj_terazniejszy(variations)
        polish_word = update_polish_word_czasownik(polish_word, update)
        update = do_conj_przyszly(variations)
        polish_word = update_polish_word_czasownik(polish_word, update)
        print(polish_word)
        return polish_word
    else:
        print('Nie ma takiego słowa na stronie.')

def update_polish_word_czasownik(polish_word: {}, new_node: {}):
    word = get_word_from_dict_element(polish_word)
    polish_word[word]['koniugacja'].update(new_node)
    return polish_word

def get_word_from_dict_element(word_as_dict: {}):
    return list(word_as_dict.keys())[0]

def do_conj_przyszly(variations: []):
    if len(variations) == 28:
        words = variations[22:28]
        update = {'przyszly': zip_nums_with_values(words)}
    else:
        words = get_conj_przyszly_meski(variations)
        conj_meski = zip_nums_with_values(words)
        words = get_conj_przyszly_zenski(variations)
        conj_zenski = zip_nums_with_values(words)
        words = get_conj_przyszly_nijaki(variations)
        conj_nijaki = zip_nums_with_values(words)
        update = {'przyszly': {'meski': conj_meski, 'zenski': conj_zenski, 'nijaki': conj_nijaki}}
    return update

def get_conj_przyszly_nijaki(variations: []):
    indx = [24, 27, 30, 33, 35, 37]
    return get_values_from_index(variations, indx)

def get_conj_przyszly_zenski(variations: []):
    indx = [23, 26, 29, 32, 35, 37]
    return get_values_from_index(variations, indx)

def get_conj_przyszly_meski(variations: []):
    indx = [22, 25, 28, 31, 34, 36]
    return get_values_from_index(variations, indx)

def do_conj_terazniejszy(variations: []):
    words = variations[16:22]
    update = {'terazniejszy': zip_nums_with_values(words)}
    return update

def do_conj_przeszly(variations: []):
    words = get_conj_przeszly_meski(variations)
    conj_meski = zip_nums_with_values(words)
    words = get_conj_przeszly_zenski(variations)
    conj_zenski = zip_nums_with_values(words)
    words = get_conj_przeszly_nijaki(variations)
    conj_nijaki = zip_nums_with_values(words)
    update = {'przeszly': {'meski': conj_meski, 'zenski': conj_zenski, 'nijaki': conj_nijaki}}
    return update

def get_conj_przeszly_nijaki(variations: []):
    indx = [2, 5, 8, 11, 13, 15]
    return get_values_from_index(variations, indx)

def get_conj_przeszly_zenski(variations: []):
    indx = [1, 4, 7, 10, 13, 15]
    return get_values_from_index(variations, indx)

def get_conj_przeszly_meski(variations: []):
    indx = [0,3,6,9,12,14]
    return get_values_from_index(variations, indx)



def save_data_in_file(lemko_word):
    if lemko_word != {}:
        with open("data/polish_words.json", "r", encoding="utf8") as file:
            lemko_dict = json.load(file)
        lemko_dict.update(lemko_word)
        with open('data/polish_words.json', 'wb') as file:
            file.write(json.dumps(lemko_dict, indent=2, sort_keys=True, ensure_ascii=False).encode('utf8'))


def do_next_word(word, reload=False):
    if word not in get_polish_base_forms_from_json_file() or reload:
        polish_word = do_czasownik(word, reload)
        save_data_in_file(polish_word)
        return 0
    else:
        print('Słowo `' + word + '` jest już w bazie.')


word = "grzać"
do_next_word(word)