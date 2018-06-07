import itertools
import json
import operator
import re
import warnings

from functools import reduce


polish_json_filename = './static/polish_words.json'
lemko_json_filename = './static/lemko_words.json'

def firstLetterFromSentencesToUpper(sentences):
    return [sent[0].upper() + sent[1:] for sent in sentences]


# does a permutation lists
def listsToSentences(lists):
    sets_of_words = list(itertools.product(*lists))
    sentences = [" ".join(list(sets_of_words[i])) for i in range(0, sets_of_words.__len__() - 1)]
    sentences = firstLetterFromSentencesToUpper(sentences)
    return sentences


def saveLemkosSentences(sentences):
    lem_sentences_file = open("data/lemkos_sentences.txt", 'w', encoding="UTF-8")
    for sent in sentences:
        lem_sentences_file.write(sent + "\n")


def savePolishSentences(sentences):
    pl_sentences_file = open("data/polish_sentences.txt", 'w', encoding="UTF-8")
    for sent in sentences:
        pl_sentences_file.write(sent + "\n")


# l_lem is list of lists of words (noun, verb, etc.)
def createAndSaveToFileSentences(l_lem, l_pl):
    lem_sentences = listsToSentences(l_lem)
    pl_sentences = listsToSentences(l_pl)
    saveLemkosSentences(lem_sentences)
    savePolishSentences(pl_sentences)


def flatten(l: []):
    return reduce(operator.concat, l)


def unnest_list(l: []):
    while True:
        l = flatten(l)
        try:
            if len(l) > 0:
                continue
        except Exception:
            return l
        return l


def get_words(sentence):
    return [word.lower() for word in re.findall(r'\w+', sentence) if word != '']


def format_text(text: str):
    pattern = re.compile(r'\s+')
    formatted = re.sub(pattern, ' ', text).lower()
    return formatted


def remove_none(l: []):
    return list(filter(lambda x: x != None, l))


def get_polish_base_forms_from_json_file():
    polish_dict = {}
    with open("data/polish_words.json", "r", encoding="utf8") as file:
        polish_dict = json.load(file)
    return list(polish_dict.keys())


def zip_nums_with_values(values):
    n = len(values) + 1
    return dict(list(zip(range(0, n), values)))


def get_values_from_index(table: [], indx: []):
    res = []
    try:
        for i in indx:
            res.append(table[i])
    except IndexError as e:
        print('Index error')
        return res
    return res


# it additionally reload polish_dict variable from polish_json_file_worker file
def save_polish_word_to_file(polish_word):
    if polish_word != {}:
        with open(polish_json_filename, "r", encoding="utf8") as file:
            polish_dict = json.load(file)
        polish_dict.update(polish_word)
        with open(polish_json_filename, 'wb') as file:
            file.write(json.dumps(polish_dict, indent=2, sort_keys=True, ensure_ascii=False).encode('utf8'))
            return True


def save_lemko_word_to_file(lemko_word):
    with open("data/lemko_words.json", "r", encoding="utf8") as file:
        lemko_dict = json.load(file)
    lemko_dict.update(lemko_word)
    with open('data/lemko_words.json', 'wb') as file:
        file.write(json.dumps(lemko_dict, indent=2, sort_keys=True, ensure_ascii=False).encode('utf8'))
        return True


def is_node_set(node: {}):
    return node != {} and node != ''


def get_node_key(node: {}):
    if is_node_set(node):
        return list(node.keys())[0]
    else:
        warnings.warn('Pusty node')
        return None


def get_node_val(node: {}):
    if is_node_set(node):
        return list(node.values())[0]
    else:
        return None


def get_keys(node: {}):
    if is_node_set(node):
        return list(node.keys())
    else:
        warnings.warn('Pusty node')
        return None


def get_values(node: {}):
    if is_node_set(node):
        return list(node.values())
    else:
        warnings.warn('Pusty node')
        return None
