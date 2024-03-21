"Peak alignment and envelop matching of the morph stimuli"
import scipy.signal
import slab
import pathlib
from os.path import join
import os
import numpy as np
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

# Plot the envelopes of the "raw" morphed sounds
x=list(np.arange(0, len(y), 1))
x = [x / sound.n_samples for x in x]

fig, ax = plt.subplots(3, sharex=True, sharey=True)
ax[0].plot(x, y, color="red", label="morph 0.0")
ax[1].plot(x, a, color="blue", label="morph 0.5")
ax[2].plot(x, z, color="green",label="morph 1.0")


#Peak alignment and specifiying the duration

# Finding the "latest"peak to specify maximum possible sound duration
indcs=list()
for sound_file in all_file_names:
    morph_ratio = float(str(sound_file)[-7:-4])
    sound = slab.Sound(sound_file)
    envelope = sound.envelope()
    indx= list(scipy.signal.find_peaks(envelope.data[:, 0], height=0.1)[0])[0]
    indcs.append(indx)
max_ind=max(indcs)

# Cut the sounds based on their first peak(everything before is removed) and save sounds with specified duration
duration= 12000 #enter duration in samples here
sound_analysis=dict()
for sound_file in all_file_names:
    morph_ratio = float(str(sound_file)[-7:-4])
    sound = slab.Sound(sound_file)
    envelope = sound.envelope()
    indx= list(scipy.signal.find_peaks(envelope.data[:, 0], height=0.1)[0])[0]
    sound_cut = sound.data[indx:indx+duration]
    sig = slab.Sound(data=sound_cut, samplerate=48000)
    sig = sig.resample(48828)
    #print(sig.duration)

    sig.write("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/peak_aligned/duration-"+
                str(sig.duration)+"_" +str(morph_ratio) + ".wav")
    envelope_cut=sig.envelope()
    sound_analysis[morph_ratio] = {
        "Envelope Cut Sound": envelope_cut.data[:, 0]
    }

all_file_names2 = [f for f in abs_file_paths("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/peak_aligned")]

sub_duration=[]
for file_name in all_file_names2:
    if "duration-0.59" in file_name.stem:
        sub_duration.append(file_name)

sound_analysis=dict()
for sound_file2 in sub_duration:
    sound = slab.Sound(sound_file2)
    morph_ratio = float(str(sound_file2)[-7:-4])
    envelope = sound.envelope()
    sound_analysis[morph_ratio] = {
        "Envelope Cut Sound": envelope.data[:, 0]
    }

fig, ax = plt.subplots(5, sharex=True, sharey=True)
x=list(np.arange(0, len(sound_analysis[0.0]["Envelope Cut Sound"]), 1))
x = [x / sound.samplerate for x in x]
ax[0].plot(x,sound_analysis[0.0]["Envelope Cut Sound"], color="red", label="morph 0.0")
ax[0].set_title("Morph 0.0")
ax[1].plot(x,sound_analysis[0.3]["Envelope Cut Sound"], color="purple", label="morph 0.3")
ax[1].set_title("Morph 0.3")
ax[2].plot(x,sound_analysis[0.5]["Envelope Cut Sound"], color="blue", label="morph 0.5")
ax[2].set_title("Morph 0.5")
ax[3].plot(x,sound_analysis[0.7]["Envelope Cut Sound"], color="orange",label="morph 0.7")
ax[3].set_title("Morph 0.7")
ax[4].plot(x,sound_analysis[1.0]["Envelope Cut Sound"], color="green",label="morph 1.0")
ax[4].set_title("Morph 1.0")
ax[4].set_xlabel("Time in secs")




