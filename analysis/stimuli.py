"""Script to analyse the stimuli used for Master Thesis"""

import slab
import pathlib
from os.path import join
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))

folder_path = pathlib.Path
folder_path= "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/env_morphs"

file_names = [f for f in abs_file_paths(folder_path)]

# Get the sounds in a dictionary

# Spectrum




In [24]: cosine_similarity([[1, 0, -1]], [[-1,-1, 0]])

# Envelope



# Spectrogram


