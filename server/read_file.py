import json
import random

from server.utils import polish_json_filename, lemko_json_filename


def get_json_file():
    with open(lemko_json_filename, "r", encoding="utf8") as file:
        lemkos_dict = json.load(file)
    rand_keys = random.sample(list(lemkos_dict.keys()), 2000)
    new_dic = {}
    for key in rand_keys:
        new_dic[key] = lemkos_dict[key]
    return new_dic


def get_polish_words_json():
    with open(polish_json_filename, "r", encoding="utf8") as file:
        polish_dict = json.load(file)
    return polish_dict
