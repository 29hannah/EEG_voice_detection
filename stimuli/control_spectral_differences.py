import slab
import pathlib
from os.path import join
import os
import matplotlib.pyplot as plt


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))


env_folder= "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/env_morphs"


file_names = [f for f in abs_file_paths(env_folder)]
file_names.sort()
fig, ax = plt.subplots(4, 2, sharex=True, sharey=True)
morph_ratios=[0.0, 0.4, 0.6, 1.0]
for sound_file in file_names:
    sound = slab.Sound(sound_file)
    morph_ratio = float(str(sound_file)[-7:-4])
    if morph_ratio in morph_ratios:
        if morph_ratio== 0.0:
            ind=0
        elif morph_ratio== 0.4:
            ind=1
        elif morph_ratio== 0.6:
            ind = 2
        elif morph_ratio== 1.0:
            ind = 3
      # Cut sound
        sig_cut = sound.data[round(0.0 * sound.samplerate):round(0.1 * sound.samplerate)]
        sound_cut = slab.Sound(data=sig_cut, samplerate=48828)
      # Plot spectra
        sound_cut.spectrum(axis=ax[ind, 0])
        # Aweighted sound and spectrum
        aw_sound = sound_cut.aweight()
        aw_sound.spectrum(axis=ax[ind,1])

    # Set title
    ax[0, 0].set_title("Spectrum")
    ax[0, 1].set_title("Aweighted Spectrum")
    if ind !=0:
        ax[ind, 0].set_title("")
        ax[ind, 1].set_title("")


