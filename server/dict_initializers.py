def init_polish_word_czasownik(word: str):
    polish_word = {word: init_czasownik_conjugation_form()}
    set_czesc_mowy_for_polish_word(polish_word, 1)
    return polish_word


def init_polish_word_rzeczownik(word: str):
    polish_word = {word: init_rzeczownik_declination_form()}
    set_czesc_mowy_for_polish_word(polish_word, 0)
    return polish_word


def init_polish_word_przymiotnik(word: str):
    polish_word = {word: init_przymiotnik_declination_form()}
    set_czesc_mowy_for_polish_word(polish_word, 2)
    return polish_word


# stopień wskazuje dla którego stopnia zadane jest słowo
def init_polish_word_przyslowek(word: str, stopien=0):
    polish_word = {word: init_przyslowek_odmiana()}
    set_czesc_mowy_for_polish_word(polish_word, 11)
    upd = {stopien: word}
    polish_word[word]['stopnie'].update(upd)
    return polish_word


def init_polish_word_inny(word: str):
    polish_word = {word: {}}
    set_czesc_mowy_for_polish_word(polish_word, -1)
    return polish_word


def init_polish_word_zaimek(word: str):
    polish_word = {word: {}}
    set_czesc_mowy_for_polish_word(polish_word, 4)
    return polish_word


# num - czesc_mowy
# zmieniamy wartość obiektu, dlatego nie musimy nic zwracać.
# po wyjściu z funkcji zmienna polish_word będzie po prostu zaktualizowana
def set_czesc_mowy_for_polish_word(polish_word: dict, num: int):
    word = list(polish_word.keys())[0]
    print(word)
    polish_word[word].update(get_czesc_mowy_node(num))


def get_czesc_mowy_node(num: int):
    return {"czesc_mowy": num}


def init_przyslowek_odmiana():
    return {'stopnie': {0: '', 1: '', 2: ''}}


def init_czasownik_conjugation_form():
    # czas, dla liczby poj(0), czas przeszły rodzaje męski, żeński, nijaki
    return {'koniugacja':
                {'terazniejszy': {},
                 'przeszly':
                     {'meski': {},
                      'zenski': {},
                      'nijaki': {}
                      },
                 'przyszly':
                     {'meski': {},
                      'zenski': {},
                      'nijaki': {}}
                 }
            }


def init_przymiotnik_declination_form():
    return {"deklinacja": {'meski': {'rowny': {0: {}, 1: {}}, 'wyzszy': {0: {}, 1: {}}, 'najwyzszy': {0: {}, 1: {}}},
                           'zenski': {'rowny': {0: {}, 1: {}}, 'wyzszy': {0: {}, 1: {}}, 'najwyzszy': {0: {}, 1: {}}},
                           'nijaki': {'rowny': {0: {}, 1: {}}, 'wyzszy': {0: {}, 1: {}}, 'najwyzszy': {0: {}, 1: {}}}
                           }}


def init_rzeczownik_declination_form():
    return {"deklinacja": {0: {}, 1: {}}}
