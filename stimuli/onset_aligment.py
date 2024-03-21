"Analysis of the morph stimuli"
import scipy.signal
import slab
import pathlib
from os.path import join
import os
import seaborn as sns
import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt

#TODO save results as csv file

def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))


folder_path= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/final_sounds'
all_file_names = [f for f in abs_file_paths(folder_path)]
all_file_names.sort()

sound_analysis=dict()
for sound_file in all_file_names:
    morph_ratio = float(str(sound_file)[-7:-4])
    sound = slab.Sound(sound_file)
    envelope = sound.envelope()
    sound_analysis[morph_ratio] = {
        "Envelope": envelope.data[:, 0],
        "Sound": sound.data[:, 0]
    }

y= list(sound_analysis[0.0]["Envelope"])
z= list(sound_analysis[1.0]["Envelope"])
a= list(sound_analysis[0.5]["Envelope"])


x=list(np.arange(0, len(y), 1))
x = [x / sound.n_samples for x in x]

fig, ax = plt.subplots(3, sharex=True, sharey=True)
ax[0].plot(x, y, color="red", label="morph 0.0")
ax[1].plot(x, a, color="blue", label="morph 0.5")
ax[2].plot(x, z, color="green",label="morph 1.0")


# Finding peaks
y= list(sound_analysis[0.0]["Envelope"])
z= list(sound_analysis[1.0]["Envelope"])
a= list(sound_analysis[0.5]["Envelope"])


# Get the index of the first peak
indx00=list(scipy.signal.find_peaks(y,height=0.1)[0])[0]
indx05=list(scipy.signal.find_peaks(a, height=0.1)[0])[0]
indx10=list(scipy.signal.find_peaks(z, height=0.1)[0])[0]

a2=a
y2=y
z2=z

del a2[0:(indx05)]
del z2[0:(indx10)]
del y2[0:(indx00)]


fig, ax = plt.subplots(3, sharex=True, sharey=True)
ax[0].plot(y2, color="red", label="morph 0.0")
ax[1].plot(a2, color="blue", label="morph 0.5")
ax[2].plot(z2, color="green",label="morph 1.0")


#Peak alignment and specifiying the duration
indcs=list()
for sound_file in all_file_names:
    morph_ratio = float(str(sound_file)[-7:-4])
    sound = slab.Sound(sound_file)
    envelope = sound.envelope()
    indx= list(scipy.signal.find_peaks(envelope.data[:, 0], height=0.1)[0])[0]
    indcs.append(indx)
max_ind=max(indcs)

sound_analysis=dict()
for sound_file in all_file_names:
    morph_ratio = float(str(sound_file)[-7:-4])
    sound = slab.Sound(sound_file)
    envelope = sound.envelope()
    indx= list(scipy.signal.find_peaks(envelope.data[:, 0], height=0.1)[0])[0]
    sound_cut = sound.data[indx:indx+(sound.n_samples-max_ind)]
    sig = slab.Sound(data=sound_cut, samplerate=48000)
    print(sig.duration)

    sig.write("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/peak_aligned/duration"+
                str(sig.duration)+"_" +str(morph_ratio) + ".wav")
    envelope_cut=sig.envelope()
    sound_analysis[morph_ratio] = {
        "Envelope Cut Sound": envelope_cut.data[:, 0]
    }

all_file_names2 = [f for f in abs_file_paths("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/peak_aligned")]
sound_analysis=dict()
for sound_file2 in all_file_names2:
    sound = slab.Sound(sound_file2)
    morph_ratio = float(str(sound_file2)[-7:-4])
    envelope = sound.envelope()
    sound_analysis[morph_ratio] = {
        "Envelope Cut Sound": envelope.data[:, 0]
    }

fig, ax = plt.subplots(5, sharex=True, sharey=True)
ax[0].plot(sound_analysis[0.0]["Envelope Cut Sound"], color="blue", label="morph 0.0")
ax[1].plot(sound_analysis[0.3]["Envelope Cut Sound"], color="blue", label="morph 0.3")
ax[2].plot(sound_analysis[0.5]["Envelope Cut Sound"], color="blue", label="morph 0.5")
ax[3].plot(sound_analysis[0.7]["Envelope Cut Sound"], color="blue",label="morph 0.7")
ax[4].plot(sound_analysis[1.0]["Envelope Cut Sound"], color="blue",label="morph 1.0")