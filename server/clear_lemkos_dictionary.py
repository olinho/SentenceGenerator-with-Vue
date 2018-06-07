import json
import re

# **********************************************************
# JSON MUSI BYĆ POSORTOWANY, ABY ALGORYTM DZIAŁAŁ POPRAWNIE
# **********************************************************

# testing file
# json_filename = "data/lemko_dict_tmp.json"
json_filename = "data/lemkos_dictionary.json"


def update_dict(lemko_dict):
    with open(json_filename, 'wb') as file:
        file.write("{\n".encode("utf8"))
        for key, values in lemko_dict.items():
            values = ["\"" + v + "\"" for v in list(values)]
            if len(values) > 0:
                values_str = ", ".join(values)
                file.write(("\"" + key + "\": [" + values_str + "],\n").encode("utf8"))
        file.write("}".encode("utf8"))


# **********************************************************
# JSON MUSI BYĆ POSORTOWANY, ABY ALGORYTM DZIAŁAŁ POPRAWNIE
# **********************************************************
with open(json_filename, "r", encoding="utf8") as file:
    n = 0
    prev_key = ''
    prev_values = []
    all_json = {}

    for line in file.readlines()[1:-1]:
        n += 1
        key, values = str(line).split(":")
        pattern = re.compile(r"\s+")
        key = key.replace("\"", "")
        key = re.sub(pattern, "", key)
        # list of values
        values = values.replace("],", "").replace("]", "").replace("[", "").replace("\"", "").replace("\n", "").split(",")
        # remove whitespaces
        values = [re.sub(pattern, "", v) for v in values]
        if key == prev_key:
            # get unique values
            new_values = list(set(values + prev_values))
            all_json[key] = new_values
            prev_key = key
            prev_values = new_values
        else:
            # json_obj = json.loads("{" + str(node) + "}")
            if key in list(all_json.keys()):
                print('W JSONie jest już klucz ' + key)
            all_json[key] = values
            prev_key = key
            prev_values = values

print(all_json)
update_dict(all_json)
