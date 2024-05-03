"""To avoid effect in P1/N1 same ramp for all stimuli"""
import slab
import pathlib
from os.path import join
import os
import numpy as np
import matplotlib.pyplot as plt


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))


folder_path= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/peak_aligned'
all_file_names = [f for f in abs_file_paths(folder_path)]
all_file_names.sort()


for sound_file in all_file_names:
    morph_ratio = float(str(sound_file)[-7:-4])
    sound = slab.Sound(sound_file)
    sound_ramped=sound.ramp(when='onset', duration=0.2)
    sound_ramped = sound_ramped.resample(48828)
    sound_ramped.write("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/ramped_final/ramped_duration-" +
              str(sound_ramped.duration) + "_" + str(morph_ratio) + ".wav", normalise=True)

sound_analysis = dict()
folder_path= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/ramped_final'
all_file_names_ramped = [f for f in abs_file_paths(folder_path)]
all_file_names_ramped.sort()
for sound_file in all_file_names_ramped:
    morph_ratio = float(str(sound_file)[-7:-4])
    sound = slab.Sound(sound_file)
    envelope=sound.envelope()
    sound_analysis[morph_ratio] = {
        "Envelope Ramped Sound": envelope.data[:, 0]
    }

fig, ax = plt.subplots(5, sharex=True, sharey=True)
x=list(np.arange(0, len(sound_analysis[0.0]["Envelope Ramped Sound"]), 1))
x = [x / sound.samplerate for x in x]
ax[0].plot(x,sound_analysis[0.0]["Envelope Ramped Sound"], color="red", label="morph 0.0")
ax[0].set_title("Morph 0.0")
ax[1].plot(x,sound_analysis[0.3]["Envelope Ramped Sound"], color="purple", label="morph 0.3")
ax[1].set_title("Morph 0.3")
ax[2].plot(x,sound_analysis[0.5]["Envelope Ramped Sound"], color="blue", label="morph 0.5")
ax[2].set_title("Morph 0.5")
ax[3].plot(x,sound_analysis[0.7]["Envelope Ramped Sound"], color="orange",label="morph 0.7")
ax[3].set_title("Morph 0.7")
ax[4].plot(x,sound_analysis[1.0]["Envelope Ramped Sound"], color="green",label="morph 1.0")
ax[4].set_title("Morph 1.0")
ax[4].set_xlabel("Time in secs")