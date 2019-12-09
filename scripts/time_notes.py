import pandas as pd
import numpy as np
import pretty_midi as pm
import pickle
from tqdm import tqdm
from collections import defaultdict
import os
import json

with open('data/pret_mid_dict.pickle', 'rb') as handle:
    dict_meta = pickle.load(handle)

def time_notes_dict(dict_meta):
    with open('data/time_notes.json', 'w') as to_write:
        for i,mid_pretty in tqdm(enumerate(dict_meta['pretty_midi'])): ## CHANGE FOR TEST
            dict_each = defaultdict()
            piano_midi = mid_pretty.instruments[0] # Get the piano channels
            piano_roll = piano_midi.get_piano_roll()

            # Make a dictionary of notes to all time points
            notes_time = defaultdict(list)
            for note,times in enumerate(piano_roll):
                notes_time[note] = [time for time,strike in enumerate(times) if int(strike) != 0]

            # Make a dictionary of time points to all notes at that time point
            time_notes = defaultdict(list)
            for note, times in notes_time.items():
                for time in times:
                    time_notes[time].append(note)

            # Convert time_notes dict to strings
            for time, notes in time_notes.items():
                if len(notes) == 1:
                    time_notes[time] = str(notes[0])
                else:
                    notes = [str(note) for note in notes]
                    time_notes[time] = ','.join(notes)
            dict_each['time_notes']= time_notes
            for key in dict_meta:
                if key != 'pretty_midi':
                    dict_each[key] = dict_meta[key][i]
            json.dump(dict_each, to_write)
            to_write.write('\n')
    return print('done')

time_notes_dict(dict_meta)
