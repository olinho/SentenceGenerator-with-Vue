from server.linguistic_converter import LinguisticConverterPl
from server.polish_json_file_worker import get_odmiany_based_on_description, get_polish_base_forms, \
    get_base_forms_for_czesc_mowy
from server.utils import get_node_val, is_node_set


class WordPattern:
    def __init__(self, pattern):
        self.__ling_conv = LinguisticConverterPl()
        self.__node_odmiana_name_uniformed = "odmiana"
        self.__node_odmiana_name = ""
        self.__czesc_mowy_num = -1
        self.__odmiana = {}
        self.polish_base_forms = get_polish_base_forms()
        if isinstance(pattern, WordPattern):
            self.init_for_WordPattern(pattern)
        elif isinstance(pattern, dict):
            self.init_for_dict(pattern)
        self.convert_czesc_mowy_val_to_num()
        self.__set_node_odmiana_name()

    def init_for_WordPattern(self, pattern):
        self.__czesc_mowy_num = pattern.get_czesc_mowy_num()
        self.__odmiana = pattern.get_odmiana()

    def init_for_dict(self, pattern: {}):
        self.__czesc_mowy_num = pattern['czesc_mowy']
        odmiana_node_name_from_descr = self.__get_odmiana_node_key_name_for_input_pattern(pattern)
        self.__odmiana = pattern[odmiana_node_name_from_descr]

    def __set_node_odmiana_name(self):
        czesc_mowy_str = self.get_czesc_mowy_str()
        self.__node_odmiana_name = self.__ling_conv.get_pl_odmiana_name(czesc_mowy_str)

    def get_czesc_mowy_str(self):
        attr = self.__ling_conv.conv_val_in_property_to_str({"czesc_mowy": self.__czesc_mowy_num})
        attr_val = get_node_val(attr)
        return attr_val

    def get_odmiana_node_key_name(self):
        return self.__node_odmiana_name

    def get_examples(self, n=1):
        res = {}
        i = 0
        words_for_czesc_mowy = get_base_forms_for_czesc_mowy(czesc_mowy=self.get_czesc_mowy_num())
        for polish_word in words_for_czesc_mowy:
            description = {polish_word: self.as_dict()}
            odmiany = get_odmiany_based_on_description(description)
            if len(odmiany) > 0:
                odmiana = odmiany[0]
                if odmiana != '':
                    res[polish_word] = odmiana
                    i += 1
                    if i == n:
                        break
        return res

    # to ensure transparency of name of node odmiana
    # if you set for example "form": {...}
    # this function will convert it to "odmiana": {}
    def __get_odmiana_node_key_name_for_input_pattern(self, pattern: {}):
        for key in list(pattern.keys()):
            if key != "czesc_mowy":
                return key

    def convert_czesc_mowy_val_to_num(self):
        if isinstance(self.__czesc_mowy_num, str):
            attr = self.__ling_conv.conv_val_in_property_to_num({"czesc_mowy": self.__czesc_mowy_num})
            self.__czesc_mowy_num = get_node_val(attr)

    def get_czesc_mowy_num(self):
        return self.__czesc_mowy_num

    def get_odmiana(self):
        return self.__odmiana

    # get description with values as strings
    # ex. {'czesc_mowy': 'rzeczownik', 'odmiana': {'rodzaj': 'nijaki'}
    def get_odmiana_str_valued(self):
        conv_odmiana = self.get_odmiana()
        for attr_key, attr_val in list(self.get_odmiana().items()):
            attr = {attr_key: attr_val}
            conv_attr = self.__ling_conv.conv_val_in_property_to_str(attr)
            conv_attr_val = get_node_val(conv_attr)
            conv_odmiana[attr_key] = conv_attr_val
        return conv_odmiana

    def get_odmiana_adjusted_to_polish_word_json(self):
        odmiana = self.get_odmiana()
        if not is_node_set(odmiana):
            return {}
        for attr_key, attr_val in list(self.get_odmiana().items()):
            attr = {attr_key: attr_val}
            conv_attr = self.__ling_conv.adjust_val_in_property_to_polish_words_json(attr)
            conv_attr_val = get_node_val(conv_attr)
            odmiana[attr_key] = conv_attr_val
        return odmiana

    def get_descr_adjusted_to_polish_word_json(self):
        conv_odmiana = self.get_odmiana_adjusted_to_polish_word_json()
        return {"czesc_mowy": self.__czesc_mowy_num, self.__node_odmiana_name: conv_odmiana}

    def as_dict(self):
        return dict({"czesc_mowy": self.__czesc_mowy_num, self.__node_odmiana_name: self.__odmiana})

    def __get__(self, instance, owner):
        return self

    def __repr__(self):
        return str(self.as_dict())


patterns = [
    # człowiek widzi bandurę
    [
        WordPattern({'czesc_mowy': 0, "odmiana": {'rodzaj': 0, 'liczba': 0, 'przypadek': 0}}),
        WordPattern({'czesc_mowy': 1, "odmiana": {'czas': 0, 'osoba': 2}}),
        WordPattern({'czesc_mowy': 0, "odmiana": {'rodzaj': 1, 'liczba': 0, 'przypadek': 4}})
    ],
    # kot biegnie po ulicy
    [
        WordPattern({'czesc_mowy': 0, "odmiana": {'rodzaj': 0, 'liczba': 0, 'przypadek': 0}}),
        WordPattern({'czesc_mowy': 1, "odmiana": {'czas': 0, 'osoba': 2}}),
        WordPattern({'czesc_mowy': 11, "odmiana": {}}),
        WordPattern({'czesc_mowy': 0, "odmiana": {'liczba': 0, 'przypadek': 1}})
    ]
]

# p1 = WordPattern({'czesc_mowy': 0, "odmiana": {'rodzaj': 0, 'liczba': 1, 'przypadek': 0}})
# print(p1)
# print(p1.get_czesc_mowy_str())
# print(p1.get_odmiana())
# print(p1.get_odmiana_str_valued())
# print(p1.get_descr_adjusted_to_polish_word_json())
