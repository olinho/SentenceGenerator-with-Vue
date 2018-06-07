from flask import Flask, jsonify, request
from flask_cors import CORS
from server.linguistic_converter import LinguisticConverterPl as ling_conv

# configuration
from server.polish_json_file_worker import get_polish_word
from server.read_file import get_json_file, get_polish_words_json
from server.utils import save_polish_word_to_file

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/', methods=['GET'])
def hello():
    return 'Magura'


# Pobiera łemkowską bazę słów i zebrane odmiany
# To nie jest lemkos_dict!
@app.route('/words', methods=['GET'])
def words():
    dic = get_json_file()
    return jsonify(dic)


# Pobiera polski słownik
@app.route('/polish_dict', methods=['GET', 'POST'])
def polish_dict():
    response_object = {'status': 'success'}
    dic = get_polish_words_json()
    if request.method == 'POST':
        post_data = request.get_json()
        # TODO zapis do pliku
        base_form = post_data.get('word')
        czesc_mowy = post_data.get('czesc_mowy')
        odmiana = post_data.get('odmiana')
        polish_word = {base_form: {'czesc_mowy': "-1", 'odmiana': {}}}
        if czesc_mowy != '':
            polish_word[base_form]['czesc_mowy'] = czesc_mowy
        if odmiana != {}:
            polish_word[base_form]['odmiana'] = odmiana

        if save_polish_word_to_file(polish_word):
            response_object['message'] = 'Word added!'
            response_object['updated_word'] = get_polish_word(base_form)
        else:
            response_object['message'] = 'Cannot add this word to dictionary'
            response_object['status'] = 'failure'
    else:
        response_object['dictionary'] = dic
    print(response_object)
    return jsonify(response_object)


# Pobiera mapper to zamiany czesci mowy z num na string
# np. 0 => 'rzeczownik'
@app.route('/part_of_speech_mapper')
def part_of_speech_mapper():
    mapper = ling_conv().get_czesci_mowy_mapper()
    return jsonify(mapper)


if __name__ == '__main__':
    app.run()
