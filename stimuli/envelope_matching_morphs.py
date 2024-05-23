import slab
import pathlib
from os.path import join
import os
import matplotlib.pyplot as plt
import numpy as np


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))

folder_path = pathlib.Path
folder_path= "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/resampled_sounds"
env_folder= "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/env_morphs"

file_names = [f for f in abs_file_paths(folder_path)]
file_names.sort()

"""
non_voice= slab.Sound('/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/morphs/morph-0.0.wav')
x = list(np.arange(0, len(non_voice.envelope().data[:, 0]), 1))
x = [x / non_voice.samplerate for x in x]
y1= non_voice.envelope().data[:, 0]
voice= slab.Sound('/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/morphs/morph-1.0.wav')
y2= voice.envelope().data[:, 0]
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(x,y1)
ax[1].plot(x,y2)

# Time points cut
tps= [6.71, 5.81, 5.21, 4.05, 2.05]
# Get the envelope and waveform of all sounds/ subset file names based on tp
for tp in tps:
    # Subset files
    subset_files=[]
    for sound_file in file_names:
        if 'c-' + str(tp) in str(sound_file):
            subset_files.append(sound_file)
    fig, ax = plt.subplots(11, 2, sharex=True)
    for sub_sound_file in subset_files:
        sound = slab.Sound(sub_sound_file)
        morph_ratio = float(str(sub_sound_file)[-7:-4])
        indx=subset_files.index(sub_sound_file)
        # Plot waveform
        sound.waveform(axis=ax[indx,0])
        ax[indx, 0].set_title(str(morph_ratio))
        # Plot envelope
        x = list(np.arange(0, len(sound.envelope().data[:, 0]), 1))
        x = [x / sound.samplerate for x in x]
        y= sound.envelope().data[:, 0]
        ax[indx,1].set_ylim([0, 0.5])
        ax[indx,1].plot(x,y)
"""


# Get envelope to match the sounds to
tps= [4.05, 5.91, 6.81]
for tp in tps:
    # Subset files
    subset_files=[]
    for sound_file in file_names:
        if 'c-' + str(tp) in str(sound_file):
            subset_files.append(sound_file)
    subset_files.sort()
    morph_template= slab.Sound(subset_files[10])
    morph_ratio_template = float(str(subset_files[10])[-7:-4])
    print(morph_ratio_template)
    envelope_template= morph_template.envelope()

    x = list(np.arange(0, len(envelope_template.data[:, 0]), 1))
    x = [x / morph_template.samplerate for x in x]
    y = envelope_template.data[:, 0]
    plt.figure()
    ax= plt.plot(x,y)
    plt.axhline(y=0.0, color='black', linestyle='-')

    for sub_sound_file in subset_files:
        morph = slab.Sound(sub_sound_file)
        morph_ratio = float(str(sub_sound_file)[-7:-4])
        # Get the morphs envelope
        env_morph= morph.envelope()
        # Get the envelope ratio to template
        envelope_ratio = envelope_template.data[:, 0] / env_morph.data[:, 0]
        # Apply the envelope ratio to the morph
        matched_morph = morph.envelope(apply_envelope=envelope_ratio)
        # Add ramp
        ramped_morph=matched_morph.ramp(when='both', duration=0.01)
        ramped_morph.write(env_folder + "/r_e-template-"+str(morph_ratio_template) +  "_" + sub_sound_file.stem + ".wav", normalise=True)



# Get the envelope and waveform of all envelope matched sounds
env_file_names = [f for f in abs_file_paths(env_folder)]
env_file_names.sort()
for tp in tps:
    # Subset files
    subset_files=[]
    for sound_file in env_file_names:
        if 'c-' + str(tp) in str(sound_file):
            subset_files.append(sound_file)
    subset_files.sort()
    fig, ax = plt.subplots(11, 2, sharex=True)
    for sub_sound_file in subset_files:
        sound = slab.Sound(sub_sound_file)
        morph_ratio = float(str(sub_sound_file)[-7:-4])
        indx=subset_files.index(sub_sound_file)
        # Plot waveform
        sound.waveform(axis=ax[indx,0])
        ax[indx, 0].set_title(str(morph_ratio))
        # Plot envelope
        x = list(np.arange(0, len(sound.envelope().data[:, 0]), 1))
        x = [x / sound.samplerate for x in x]
        y= sound.envelope().data[:, 0]
        ax[indx,1].set_ylim([0, 0.5])
        ax[indx,1].plot(x,y)

# Only get the envelope
env_file_names = [f for f in abs_file_paths(env_folder)]
env_file_names.sort()

for tp in tps:
    # Subset files
    subset_files=[]
    for sound_file in env_file_names:
        if 'c-' + str(tp) in str(sound_file):
            subset_files.append(sound_file)
    subset_files.sort()
    fig, ax = plt.subplots(11, 1, sharex=True)
    fig.suptitle(str(tp))
    for sub_sound_file in subset_files:
        sound = slab.Sound(sub_sound_file)
        morph_ratio = float(str(sub_sound_file)[-7:-4])
        indx=subset_files.index(sub_sound_file)
        # Plot envelope
        x = list(np.arange(0, len(sound.envelope().data[:, 0]), 1))
        x = [x / sound.samplerate for x in x]
        y= sound.envelope().data[:, 0]
        ax[indx].set_ylim([0, 0.5])
        ax[indx].plot(x,y)

# Get the spectra
for tp in tps:
    # Subset files
    subset_files=[]
    for sound_file in env_file_names:
        if 'c-' + str(tp) in str(sound_file):
            subset_files.append(sound_file)
    subset_files.sort()
    fig, ax = plt.subplots(11, 1, sharex=True, sharey=True)
    fig.suptitle(str(tp))
    for sub_sound_file in subset_files:
        sound = slab.Sound(sub_sound_file)
        indx = subset_files.index(sub_sound_file)
        sound.spectrum(axis=ax[indx])
        ax[indx].title.set_text(" ")

# Get the spectrogram
for tp in tps:
    # Subset files
    subset_files=[]
    for sound_file in env_file_names:
        if 'c-' + str(tp) in str(sound_file):
            subset_files.append(sound_file)
    subset_files.sort()
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)
    fig.suptitle(str(tp))
    for sub_sound_file in subset_files:
        sound = slab.Sound(sub_sound_file)
        indx = subset_files.index(sub_sound_file)
        if indx==0:
            sound.spectrogram(axis=ax[indx])
            ax[indx].title.set_text(" ")
        elif indx==10:
            sound.spectrogram(axis=ax[2])
            ax[2].title.set_text(" ")
        elif indx==5:
            sound.spectrogram(axis=ax[1])
            ax[1].title.set_text(" ")



"""
# Compare envelope and ERP
import mne
evoked = mne.read_evokeds('/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/analysis/results/pilot/EEG/hannah_test_1605/evokeds/hannah_test_1605-ave.fif')

evoked[1].crop(tmin=0.0, tmax=0.499)
evoked[2].crop(tmin=0.0, tmax=0.499)
evoked[3].crop(tmin=0.0, tmax=0.499)
evoked[4].crop(tmin=0.0, tmax=0.499)

fig, ax = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [2, 1, 1]})
picks= "FCz"
fig=mne.viz.plot_compare_evokeds([evoked[1],evoked[2], evoked[3],evoked[4]],
                             picks=picks,truncate_xaxis= -0.1, colors=["firebrick", "lightsalmon", "lightblue", "darkblue"],
                             show_sensors=True, legend="lower right", axes=ax[0], title= "ERP at FCz" )

env_file_names = [f for f in abs_file_paths(env_folder)]
env_file_names.sort()
morph_ratios=[0.0, 0.4, 0.6, 1.0]
ax[1].set_title("Stimuli Envelopes")
ax[2].set_title("Stimuli Aweighted Envelopes")
for sound_file in env_file_names:
    sound = slab.Sound(sound_file)
    morph_ratio = float(str(sound_file)[-7:-4])
    if morph_ratio in morph_ratios:
        if morph_ratio== 0.0:
            color="firebrick"
        elif morph_ratio== 0.4:
            color = "lightsalmon"
        elif morph_ratio== 0.6:
            color = "lightblue"
        elif morph_ratio== 1.0:
            color = "darkblue"
        # Plot envelopes
        x = list(np.arange(0, len(sound.envelope().data[:, 0]), 1))
        x = [x / sound.samplerate for x in x]
        y= sound.envelope().data[:, 0]
        ax[1].set_ylim([0, 0.6])
        ax[1].plot(x,y, color=color)
        #sound.spectrogram()

        # Plot aweighted envelope
        aw_sound = sound.aweight()

        y2 = aw_sound.envelope().data[:, 0]
        ax[2].set_ylim([0, 0.6])
        ax[2].plot(x, y2, color=color)
        ax[2].set_xlabel("Time in sec")
"""
