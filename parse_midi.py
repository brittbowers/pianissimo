import pandas as pd
import numpy as np
import pretty_midi as pm
import pickle
from tqdm import tqdm
from collections import defaultdict
import os

df_meta = pd.read_csv('data/maestro_meta.csv')
# Reading midi files into a meta dictionary using the meta csv
def get_pretty_midi(df_meta, path = 'data/maestro'):
    dict_meta = defaultdict(list)
    folderlist = os.listdir(path)
    for folder in folderlist:
        try:
            files = os.listdir(path + '/' + folder)
            for file in tqdm(files):
                filename = path + '/{}/'.format(folder) + file
                mid_pretty = pm.PrettyMIDI(filename)
                meta_file = folder + '/' + file
                dict_meta['composer'].append(df_meta.loc[df_meta['midi_filename'] == meta_file, 'canonical_composer'].tolist()[0])
                dict_meta['title'].append(df_meta.loc[df_meta['midi_filename'] == meta_file, 'canonical_title'].tolist()[0])
                dict_meta['split'].append(df_meta.loc[df_meta['midi_filename'] == meta_file, 'split'].tolist()[0])
                dict_meta['year'].append(df_meta.loc[df_meta['midi_filename'] == meta_file, 'year'].tolist()[0])
                dict_meta['duration'].append(df_meta.loc[df_meta['midi_filename'] == meta_file, 'duration'].tolist()[0])
                dict_meta['pretty_midi'].append(mid_pretty)
        except:
            pass
    return dict_meta

dict_meta = get_pretty_midi(df_meta)

#Pickle Dictionary
with open('data/pret_mid_dict.pickle', 'wb') as handle:
    pickle.dump(dict_meta, handle, protocol=pickle.HIGHEST_PROTOCOL)
