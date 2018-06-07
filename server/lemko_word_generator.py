import warnings

from server import polish_word_generator, lemko_json_file_worker
from server.dict_initializers import init_czasownik_conjugation_form, init_przymiotnik_declination_form
from server.lemko_words_and_variations import LemkoWordsAndVariations
from server.psql_worker import PsqlWorker
from server.utils import format_text, get_words, remove_none, save_lemko_word_to_file

czasy = {0: 'terazniejszy', 1: 'przeszly', 2: 'przyszly'}
rodzaje = {0: 'meski', 1: 'zenski', 2: 'nijaki'}
osoby = {'on': {'db': 2, 'wiki': 2}, 'ona': {'db': 3, 'wiki': 2}, 'on': {'db': 4, 'wiki': 2},
         'my': {'db': 5, 'wiki': 3}, 'wy': {'db': 6, 'wiki': 4}, 'oni': {'db': '7', 'wiki': 5}}
osoba_db_to_wiki = {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5}
stopnie = {0: 'rowny', 1: 'wyzszy', 2: 'najwyzszy'}

db = PsqlWorker()
ld = LemkoWordsAndVariations()


def do_next_words(words: []):
    done_words = []
    for word in words:
        if do_next_word(word):
            done_words.append(word)
    return done_words

def do_next_word(word: str):
    word = format_text(word)
    if word in lemko_json_file_worker.get_lemko_words():
        print('Уж знам слово "' + word + '"')
        return True
    details = db.get_word_details(word)

    node_decl = {}
    node_conj = {}
    node_rest = {}
    node = {}
    try:
        gramm_part_of_speech = details['grammatical_part_of_speech']
    except Exception:
        warnings.warn('Nieznana część mowy dla słowa ' + str(word))
        gramm_part_of_speech = -1

    node_rest = {"tlumaczenie": "", "czesc_mowy": ""}
    node_rest['tlumaczenie'] = format_text(details['polish_translation'])
    node_rest['czesc_mowy'] = details['grammatical_part_of_speech']
    node_word = format_text(details['base_form'])
    if gramm_part_of_speech == 0:
        node_rest['rodzaj'] = details['grammatical_gender']

    node[node_word] = node_rest

    if gramm_part_of_speech == 0:
        decl = db.get_noun_declination(word)
        node_decl = {"deklinacja": {0: {}, 1: {}}}
        for el in decl:
            node_decl['deklinacja'][el['grammatical_number']][el['grammatical_case']] = el['word']

    if gramm_part_of_speech == 1:
        node_conj = init_czasownik_conjugation_form()
        czas_num = 0
        czas_str = czasy[czas_num]
        conj = get_czasownik_conj_czas_rodzaj(czas_num, word)
        node_conj['koniugacja'][czas_str].update(conj)
        for czas_num in [1, 2]:
            for rodzaj_num in [0, 1, 2]:
                conj = get_czasownik_conj_czas_rodzaj(czas_num=czas_num, word=word, rodzaj_num=rodzaj_num)
                czas_str = czasy[czas_num]
                rodzaj_str = rodzaje[rodzaj_num]
                node_conj['koniugacja'][czas_str][rodzaj_str].update(conj)

    if gramm_part_of_speech == 2:
        decl = db.get_adjective_declination(word)
        node_decl = init_przymiotnik_declination_form()
        for el in decl:
            gramm_gender = el['grammatical_gender']
            rodzaj = rodzaje[gramm_gender]
            if rodzaj is None:
                rodzaj = 'nijaki'
            stopien_num = el['grammatical_comparison']
            stopien_str = stopnie[stopien_num]
            if stopien_str is None:
                stopien_str = stopnie[0]
            node_decl['deklinacja'][rodzaj][stopien_str][el['grammatical_number']][el['grammatical_case']] = el['word']

    if node_decl != {}:
        node[node_word].update(node_decl)
    if node_conj != {}:
        node[node_word].update(node_conj)
    print(node)
    if save_lemko_word_to_file(node):
        return True
    else:
        return False


# filter elements which tense and person fill the requirement.
# map results to get pairs: (person, word)
# convert to dict
def get_czasownik_conj_czas_rodzaj(czas_num, word, rodzaj_num=0):
    if czas_num == 0:
        rodzaj_num = 0
    if rodzaj_num == 1:
        osoby_legalne = [3]
    elif rodzaj_num == 2:
        osoby_legalne = [4]
    else:
        osoby_legalne = [0, 1, 2, 5, 6, 7]
    czas_str = czasy[czas_num]
    rodzaj_str = rodzaje[rodzaj_num]
    new_node = {}
    conj = db.get_verb_conjugation(word)
    filtered_nodes = filter(lambda x: x['grammatical_tense'] == czas_num and x['grammatical_person'] in osoby_legalne,
                            conj)
    odmiany = map(lambda x: (osoba_db_to_wiki[x['grammatical_person']], x['word']), filtered_nodes)
    new_node = dict(odmiany)
    return new_node


def get_czasownik_conj_meski_dla_czasu(czas_num, word: str):
    return get_czasownik_conj_czas_rodzaj(czas_num, word, 0)


def get_czasownik_conj_zenski_dla_czasu(czas_num, word: str):
    return get_czasownik_conj_czas_rodzaj(czas_num, word, 1)


def get_czasownik_conj_nijaki_dla_czasu(czas_num, word: str):
    return get_czasownik_conj_czas_rodzaj(czas_num, word, 2)


def get_czasownik_conj_meski_dla_czasu_2(czas_num, word: str):
    conj = db.get_verb_conjugation(word)
    odmiany = {}
    for el in conj:
        czas = el['grammatical_tense']
        czas_str = czasy[czas]
        osoba_num_db = el['grammatical_person']
        print(osoba_num_db)
        if osoba_num_db not in [3, 4] and czas == czas_num:
            osoba_num_wiki = osoba_db_to_wiki[osoba_num_db]
            odmiany[osoba_num_wiki] = el['word']
    return odmiany


def show_details(word: str):
    details = db.get_word_details(word)
    print(details)
    part_of_speech = details['grammatical_part_of_speech']
    if part_of_speech == 0:
        decl = db.get_noun_declination(word)
        print(decl)
    elif part_of_speech == 1:
        conj = db.get_verb_conjugation(word)
        print(conj)
    elif part_of_speech == 2:
        decl = db.get_adjective_declination(word)
        print(decl)


# add next words, get from db, sorted by name
def add_next_words_to_json(limit=10):
    done_words = []
    words = db.get_new_words(lemko_json_file_worker.get_lemko_words(), limit=limit)
    for word in words:
        print('Word ' + word)
        try:
            if do_next_word(word):
                done_words.append(word)
        except Exception as e:
            print(e)
    print(done_words)
    return done_words


def fill_the_json(words):
    known_words = lemko_json_file_worker.get_lemko_words()
    unknown_words = [word for word in words if word not in known_words]
    for word in unknown_words:
        print('Word ' + word)
        try:
            do_next_word(word)
        except Exception as e:
            print(e)


# get words from sentence and add unknown to lemko_words.json
def update_lemko_words_json_for_sentence(sent):
    # TODO
    # base_forms_in_sent = get_base_forms_from_lemko_json_file(sent)
    base_forms_in_sent = get_base_forms_from_dictionary(sent)
    # TODO
    # filtered_base_forms = words which are in all_words_variations and are not in lemko_json_file
    filtered_base_forms = remove_none(base_forms_in_sent)
    fill_the_json(filtered_base_forms)
    return True


# get list of words from sentence in base forms
def get_base_forms_from_dictionary(sent: str):
    words_in_sent = get_words(sent)
    return [ld.get_base_form(word) for word in words_in_sent]


# get list of words from sentence in base forms
def get_base_forms_from_db(sent: str):
    words_in_sent = get_words(sent)
    return [db.get_base_form_for_word(word) for word in words_in_sent]


def has_sentence_unknown_word(sent: str):
    base_forms = get_base_forms_from_dictionary(sent)
    if None in base_forms or '' in base_forms:
        return True
    else:
        return False


def is_sentence_built_of_known_words(sent: str):
    return not has_sentence_unknown_word(sent)

#
# word = "Лемко"
# do_next_word(word)

done_words = add_next_words_to_json()
# done_words = do_next_words(['думати', "дукат", "дідо", "епоха"])
print(done_words)
pl_base_forms = lemko_json_file_worker.get_translations(done_words)
print(pl_base_forms)
polish_word_generator.do_next_words(pl_base_forms)



#
# # lem_sent = db.get_sentence_with_word('палиця')
# lem_sent = 'червены птахи над головами, а в чорным озері плывают красны рыбы'
# lem_words = get_words(lem_sent)
# lem_base_forms = get_base_forms_from_dictionary(lem_sent)
#
# translation = {lem_word: '' for lem_word in lem_words}
# print(translation)
#
# print("Zdanie: " + lem_sent)
# print("Słowa: " + str(lem_words))
# print("Podstawowe formy słów: " + str(lem_base_forms))
#
# words_description_history = []



# # czy słowa są w lemko_dictionary.json
# if is_sentence_built_of_known_words(lem_sent):
#     if update_lemko_words_json_for_sentence(lem_sent):
#         try:
#             pl_base_forms = lemko_json_file_worker.get_translations(lem_base_forms)
#             print(pl_base_forms)
#             if polish_word_generator.do_next_words(pl_base_forms):
#                 pl_translated_words = []
#                 for lem_word in lem_words:
#                     word_description = lemko_json_file_worker.get_word_description(lem_word, ld)
#                     print(word_description)
#                     pl_translated_word_all_forms = polish_json_file_worker.get_odmiany_based_on_description(
#                         word_description)
#                     pattern_number = 0
#                     pl_translated_word = pl_translated_word_all_forms[pattern_number]
#                     pl_base_form_word = polish_json_file_worker.get_word_from_description(word_description)
#                     if is_node_set(word_description[pl_base_form_word]):
#                         word_czesc_mowy = word_description[pl_base_form_word]['czesc_mowy']
#                         history_node = word_description[pl_base_form_word]['formy'][pattern_number]
#                         history_node['czesc_mowy'] = word_czesc_mowy
#                         words_description_history.append(history_node)
#                     else:
#                         words_description_history.append({})
#                     print(pl_translated_word)
#                     pl_translated_words.append(pl_translated_word)
#                     translation[lem_word] = pl_translated_word
#                 print("Polska translacja: " + " ".join(pl_translated_words))
#         except Exception as e:
#             warnings.warn('Nie udało się przetłumaczyć zdania' + e)
#     else:
#         warnings.warn('Nie udało się zaktualizować danych o podanych słowach')
# print(translation)
