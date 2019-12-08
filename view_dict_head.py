import json
import pickle
filetype = input('Filetype:')

if filetype == 'json':
    with open('data/time_notes_dict.json', 'r') as handle:
        dict_meta = json.load(handle)
    print(dict_meta['time_notes'][0])
else:
    with open('data/time_notes_dict.pickle', 'rb') as handle
        dict_meta = pickle.load(handle)
    print(dict_meta['time_notes'][0])
