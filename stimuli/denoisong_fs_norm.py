import slab
import pathlib
from os.path import join
import os
from scipy.io import wavfile
import noisereduce as nr


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))

folder_path = pathlib.Path
#folder_path= '/Users/hannahsmacbook/PycharmProjects/AVH/stimuli/sound_files/whisper_2/resampled_rms-norm_morphs_behavior_Leipzig'
folder_path= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/cut_sounds'

all_file_names = [f for f in abs_file_paths(folder_path)]

out_folder_path= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/denoised_sounds'
if not os.path.exists(out_folder_path):
    os.makedirs(out_folder_path)
    print("path did not exist, path created")


for file_name in all_file_names:
    rate, data = wavfile.read(file_name)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(out_folder_path + "/d_"+ file_name.stem + ".wav", rate, reduced_noise)


out_folder_path2= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/resampled_sounds'
if not os.path.exists(out_folder_path2):
    os.makedirs(out_folder_path2)
    print("path did not exist, path created")

all_file_names2 = [f for f in abs_file_paths(out_folder_path)]


new_rate=48828 #rate used for dome set-up
for file_name in all_file_names2:
    sound = slab.Binaural(file_name)
    sound = sound.resample(new_rate)
    sound_mon=sound.left
    sound_mon=slab.Sound(sound_mon)
    sound_mon.write(out_folder_path2+ "/s_"+ file_name.stem+".wav", normalise=True)