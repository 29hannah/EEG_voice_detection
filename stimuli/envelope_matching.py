"""Match the envelope of the two original sounds before morphing
-apply the envelope of the vocal sound (whisper) to the non-vocal sound (pencil on paper)
"""

import slab
import pathlib
from os.path import join
import os
import matplotlib.pyplot as plt
import numpy as np

# Read in the sounds

def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))

folder_path = pathlib.Path
folder_path='/Users/hannahsmacbook/MATLAB/Projects/AVH/Stimuli/sound_files/whisper_2/normalized_files/'
all_file_names = [f for f in abs_file_paths(folder_path)]

non_voice_sound= slab.Binaural(all_file_names[1])
envelope_nonvoice = non_voice_sound.envelope()

voice_sound= sound = slab.Binaural(all_file_names[0])
envelope_voice = voice_sound.envelope()

non_voice_sound_voice_env_sound=non_voice_sound.envelope(apply_envelope=envelope_voice.data[:,0])
non_voice_sound_voice_env= non_voice_sound_voice_env_sound.envelope()

# Plot envelopes before
fig, axs = plt.subplots(3, sharex=True)

y= list(envelope_voice.data[:,0])
z= list(envelope_nonvoice.data[:,0])
a= list(non_voice_sound_voice_env.data[:,0])
axs[0].plot(y)
axs[0].set_title('Envelope Voice Sound')
axs[1].plot(z)
axs[1].set_title('Envelope Non Voice Sound (before envelope matching)')
axs[2].plot(a)
axs[2].set_title('Envelope Non Voice Sound (after envelope matching)')


# Save the sounds
voice_sound.write("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/envelope_mod/voice_sound.wav",
                  normalise=True)
non_voice_sound_voice_env_sound.write("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/envelope_mod/nonvoice_sound.wav",
                                normalise=True)



