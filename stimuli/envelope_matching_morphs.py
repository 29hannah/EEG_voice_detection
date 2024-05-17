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

# Get the envelope and waveform of all sounds
fig, ax = plt.subplots(11, 2, sharex=True)
for sound_file in file_names:
    sound = slab.Sound(sound_file)
    morph_ratio = float(str(sound_file)[-7:-4])
    indx=file_names.index(sound_file)
    # Plot waveform
    sound.waveform(axis=ax[indx,0])
    ax[indx, 0].set_title(str(morph_ratio))
    # Plot envelope
    x = list(np.arange(0, len(sound.envelope().data[:, 0]), 1))
    x = [x / sound.samplerate for x in x]
    y= sound.envelope().data[:, 0]
    ax[indx,1].set_ylim([0, 0.5])
    ax[indx,1].plot(x,y)





# Get envelope to match the sounds to
morph_template= slab.Sound(file_names[10])
morph_ratio_template = float(str(file_names[10])[-7:-4])
template_cut = morph_template.data[round(0.37 * morph_template.samplerate):round(0.97 * morph_template.samplerate)]
morph_template = slab.Sound(data=template_cut, samplerate=48828)
envelope_template= morph_template.envelope()

morph_template.waveform()

x = list(np.arange(0, len(envelope_template.data[:, 0]), 1))
x = [x / morph_template.samplerate for x in x]
y = envelope_template.data[:, 0]
ax= plt.plot(x,y)
plt.axhline(y=0.0, color='black', linestyle='-')


for sound_file in file_names:
    morph = slab.Sound(sound_file)
    morph_ratio = float(str(sound_file)[-7:-4])
    sound_cut = morph.data[round(0.37 * morph.samplerate):round(0.97 * morph.samplerate)]
    morph_cut = slab.Sound(data=sound_cut, samplerate=48828)
    # Get the morphs envelope
    env_morph= morph_cut.envelope()
    # Get the envelope ratio to template
    envelope_ratio = envelope_template.data[:, 0] / env_morph.data[:, 0]
    # Apply the envelope ratio to the morph
    matched_morph = morph_cut.envelope(apply_envelope=envelope_ratio)
    # Add ramp
    ramped_morph=matched_morph.ramp(when='onset', duration=0.01)
    matched_morph.write(env_folder + "/r_e-template-"+str(morph_ratio_template) +  "_" + sound_file.stem + ".wav", normalise=True)

# Get the envelope and waveform of all envelope matched sounds
env_file_names = [f for f in abs_file_paths(env_folder)]
env_file_names.sort()
fig, ax = plt.subplots(11, 2, sharex=True)
for sound_file in env_file_names:
    sound = slab.Sound(sound_file)
    morph_ratio = float(str(sound_file)[-7:-4])
    indx=env_file_names.index(sound_file)
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
fig, ax = plt.subplots(11, 1, sharex=True)
for sound_file in env_file_names:
    sound = slab.Sound(sound_file)
    morph_ratio = float(str(sound_file)[-7:-4])
    indx=env_file_names.index(sound_file)
    # Plot envelope
    x = list(np.arange(0, len(sound.envelope().data[:, 0]), 1))
    x = [x / sound.samplerate for x in x]
    y= sound.envelope().data[:, 0]
    ax[indx].set_ylim([0, 0.5])
    ax[indx].plot(x,y)


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

