import os
import pathlib
from os.path import join
import slab


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))

#Change to the continuum you are working with
continuum="whisper_2"

DIR = '/Users/hannahsmacbook/PycharmProjects/AVH/stimuli/sound_files/'+continuum
sub_DIR= DIR +'/original_sounds'
all_file_names = [f for f in abs_file_paths(sub_DIR)]
print(all_file_names)

all_file_names=all_file_names[2:4]

#You  need to select the  sound files->voice/non_voice and relevance (after resampling)
voice_file= all_file_names[1]
non_voice_file= all_file_names[0]

#You  need to select the  sound files->voice/non_voice and relevance (after resampling)
voice = slab.Sound(voice_file)
non_voice = slab.Sound(non_voice_file)

#Create a filterbank based on the voice sound; apply this filterbank the non-voice sound
inverse = slab.Filter.equalizing_filterbank(reference=voice, sound=non_voice)
equalized = inverse.apply(non_voice)


new_rate=48828 #rate used for dome set-up

#Write the file to the filtered folder in python which you need to create manually
voice= voice.resample(new_rate)
equalized= equalized.resample(new_rate)
voice.write(filename='/stimuli/sound_files/filtered_original/whisper.wav', normalise= True)
equalized.write(filename='/stimuli/sound_files/filtered_original/voice_filtered_writing.wav', normalise= True)
