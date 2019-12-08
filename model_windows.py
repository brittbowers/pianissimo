import pandas as pd
import numpy as np
import pretty_midi as pm
import pickle
from tqdm import tqdm
from collections import defaultdict
import os
import json

with open('data/time_notes_dict.json', 'r') as handle:
    dict_meta = json.load(handle)

def dict_note_index(time_notes):
    dict_index = defaultdict(int)
    dict_index['e'] = 0
    i = 1
    for time, notes in time_notes.items():
        if notes not in dict_index:
            dict_index[notes] = i
            i += 1
        else:
            pass
    return dict_index

def input_target_seq(dict_time_notes, seq_len = 50):
    # Get the starting and ending time points with notes
    start, end = sorted(list(time_notes.keys()))[0], sorted(list(time_notes.keys()))[-1]
    lst_train, lst_target = [], []
    flag_target_append = False
    # Iterate through all of the timepoints in between start and end
    for ind, time in enumerate(range(start, end)):
        window_train, window_target = [], []
        start_ind = 0

        # If the ind is in the first window
        if ind < seq_len: # ind = 0 < 50
            # Change window start to sequence length (window) - 1
            start_ind = seq_len - ind - 1 #start ind = 50 - 0 -1 = 49
            for i in range(start_ind): # 0 - 49
                window_train.append('e')  # Adding e for every item in start list
                flag_target_append = True

        for i in range(start_ind, seq_len): # 49 - 50
            # Set the index to
            ind = time - (seq_len - i - 1) # 103 - (50 - 49 - 1) = 103
            if ind in dict_time_notes:
                window_train.append(dict_time_notes[ind])
            else:
                window_train.append('e')

        if time+1 in dict_time_notes:
            window_target.append(dict_time_notes[time+1])
        else:
            window_target.append('e')
        lst_train.append(window_train)
        lst_target.append(window_target)

    return lst_train, lst_target

def notes_to_index(lst_train, lst_target, dict_index):
    lst_train_ind, lst_target_ind = [], []
    for wind_train, note_target in zip(lst_train, lst_target):
        lst_train_wind = []
        lst_target_ind.append(dict_index[note_target[0]])
        for note_train in wind_train:
            lst_train_wind.append(dict_index[note_train])
        lst_train_ind.append(lst_train_wind)
    return lst_train_ind, lst_target_ind

dict_meta['train'] = []
dict_meta['target'] = []
dict_index = dict_note_index(time_notes)
for time_notes in tqdm(dict_meta['time_notes']):
    lst_train, lst_target = input_target_seq(time_notes)
    lst_train_ind, lst_target_ind = notes_to_index(lst_train, lst_target, dict_index)
    dict_meta['train'].append(lst_train_ind)
    dict_meta['target'].append(lst_target_ind)

with open('data/train_tar_dict.json', 'w') as handle:
    json.dump(dict_meta, handle)
