# web scraper. It gets data from site odmiana.net
import re
from pathlib import Path
import os
import requests
from bs4 import BeautifulSoup

from server.dict_initializers import init_polish_word_rzeczownik
from server.utils import get_polish_base_forms_from_json_file, save_polish_word_to_file, zip_nums_with_values

site_base = "http://odmiana.net/odmiana-przez-przypadki-rzeczownika-"
html_odmiana_net_dir = "html_odmiana_net/"
przypadki = ["mianownik", "dopełniacz", "celownik", "biernik", "narzędnik", "miejscownik", "wołacz"]

def fetch_html_for_word(word: str):
    fetch_html(site_base +word)

def fetch_html(url: str):
    page = requests.get(url)
    page.encoding = 'utf-8'
    filename = url.split('-')[-1] + ".html"
    with open(html_odmiana_net_dir + filename, 'wb') as f:
        f.write(page.text.encode('utf8'))

def load_html_file_for_word(word: str):
    with open(html_odmiana_net_dir + word + ".html", 'rb') as f:
        soup = BeautifulSoup(f, "lxml")
    return soup

def does_file_exist(word: str):
    filename = Path(html_odmiana_net_dir + word + ".html")
    return filename.is_file()

def get_soup_for_word(word: str):
    if not does_file_exist(word):
        fetch_html_for_word(word)
    return load_html_file_for_word(word)

def get_table(html):
    return html.find('table')


def do_next_word(word):
    if word not in get_polish_base_forms_from_json_file():
        html = get_soup_for_word(word)
        if not is_word_described(word, html):
            filename = html_odmiana_net_dir + word + ".html"
            os.remove(filename)
            return False
        polish_word = {}
        polish_word = do_declination(word, html)
        save_polish_word_to_file(polish_word)
        return True

def do_declination(word, html):
    polish_word = init_polish_word_rzeczownik(word)
    table = get_table(html)
    polish_word[word]['deklinacja'][0] = decl_l_poj(table)
    polish_word[word]['deklinacja'][1] = decl_l_mnog(table)
    return polish_word

def decl_l_mnog(table):
    return decl_liczba(table, 1)

def decl_l_poj(table):
    return decl_liczba(table, 0)

def decl_liczba(table, liczba):
    odmiana = [get_decl_for_przypadek_liczba(table, przypadek, liczba) for przypadek in przypadki]
    decl = zip_nums_with_values(odmiana)
    return decl

def get_decl_for_przypadek_liczba(table, przypadek_str, liczba):
    tr = table.find(string=re.compile(przypadek_str, re.IGNORECASE)).find_parent('tr')
    col = liczba + 1
    odmiana = tr.find_all('td')[col].get_text()
    if "," in odmiana:
        odmiany = odmiana.replace(" ", "").split(',')
        return odmiany
    else:
        return odmiana

def is_word_described(word: str, html):
    if not html.find(string=re.compile("Strona, której szukasz nie została odnaleziona.")):
       return True
    else:
        return False

def remove_html_for_word(word: str):
    filename = html_odmiana_net_dir + word + ".html"
    os.remove(filename)

# word = "chmura"
# do_next_word(word)