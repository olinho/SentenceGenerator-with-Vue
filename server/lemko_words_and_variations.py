import json


def flatten_list(l):
    return [el for sublist in l for el in sublist]


class LemkoWordsAndVariations:
    def __init__(self):
        self.dic = {}
        self.base_forms = []
        self.variations = []
        self.__load_dictionary()
        self.__load_base_forms()
        self.__load_variations()

    def __load_dictionary(self):
        with open("data/lemkos_dictionary.json", "r", encoding="utf8") as file:
            self.dic = json.load(file)

    def __load_base_forms(self):
        self.base_forms = list(self.dic.keys())

    def __load_variations(self):
        list_of_variations = list(self.dic.values())
        self.variations = flatten_list(list_of_variations)

    def get_base_form(self, word: str):
        for key, values in self.dic.items():
            if word == key or word in values:
                return key
        print('Baza nie posiada słowa ' + word)
        return ''
