import slab
import freefield
import copy
import pathlib
import numpy
import time
import random
import string
import os
from EEG_voice_detection.experiment.config import get_config


# TODO check for solution after deviant: update collect responses


participant_id = 'test_1602'
stimulus_level=67


slab.set_default_samplerate(44100)
DIR = pathlib.Path(os.getcwd())

config = get_config()
proc_list = config['proc_list']
freefield.initialize('dome', zbus=True, device=proc_list)
freefield.set_logger('WARNING')


def crop_sound(sound, isi):
    isi = slab.Sound.in_samples(isi, sound.samplerate)
    out = copy.deepcopy(sound)
    if sound.n_samples < isi:
        silence_length = isi - sound.n_samples
        silence = slab.Sound.silence(duration=silence_length, samplerate=sound.samplerate)
        left = slab.Sound.sequence(sound.left, silence)
        right = slab.Sound.sequence(sound.right, silence)
        out = slab.Binaural([left, right])
    else:
        out.data = sound.data[: isi]
    out = out.ramp(duration=0.01)
    return out

def load_to_buffer(sound, isi=2.0):
    out = crop_sound(sound, isi)
    isi = slab.Sound.in_samples(isi, 48828)
    freefield.write(tag="playbuflen", value=isi, processors="RP2")
    freefield.write(tag="data_l", value=out.left.data.flatten(), processors="RP2")
    freefield.write(tag="data_r", value=out.right.data.flatten(), processors="RP2")

def collect_responses(seq, results_file):
    response = None
    reaction_time = None
    start_time = time.time()
    while not freefield.read(tag="response", processor="RP2"):
        time.sleep(0.01)
    curr_response = int(freefield.read(tag="response", processor="RP2"))
    if curr_response != 0:
        reaction_time = int(round(time.time() - start_time, 3) * 1000)
        response = int(numpy.log2(curr_response))
        # response for deviant stimulus is reset to 0
    is_correct = response == seq.trials[seq.this_n]
    results_file.write(seq.trials[seq.this_n], tag='solution')
    results_file.write(response, tag='response')
    results_file.write(is_correct, tag='is_correct')
    results_file.write(reaction_time, tag='reaction_time')
    print('Response:' + str(response) +'; RT: ' + str(reaction_time))

def collect_trial(seq, results_file):
    results_file.write(seq.trials[seq.this_n], tag='morph_played')





results_folder = 'C:\\projects\\EEG_voice_detection\\experiment\\results\\EEG'
results_file = slab.ResultsFile(subject=participant_id, folder=results_folder)
results_file.write('EEG_experiment', tag='stage')




#Get list of stimuli in slab format
stim_dict=dict()
stim_path= 'C:\\projects\\EEG_voice_detection\\experiment\\stimuli'
for sound_file in os.listdir(os.path.join(stim_path)):
    sound = slab.Sound.read(os.path.join(stim_path, sound_file))
    sound.level= stimulus_level
    sound =slab.Binaural(sound)
    morph_ratio = sound_file[-7:-4]
    stim_dict[morph_ratio] = sound

morph_ratios= list(stim_dict.keys())

morph_seq = slab.Trialsequence(conditions=[1,5,6,7,11], n_reps=5, deviant_freq=0.3)

input('Press enter to start the experiment')

for morph in morph_seq:
    print('###Trial', morph_seq.this_n+1, '/', morph_seq.n_trials, '####')
    if morph == 0:
        deviant_sound = slab.Binaural.chirp(duration=len(sound))
        deviant_sound.level = stimulus_level
        load_to_buffer(deviant_sound)
        trig_value = len(morph_ratios) + 1
        freefield.write(tag='trigcode', value=trig_value, processors='RX82')
        freefield.play()
        print('Playing deviant')
        collect_responses(morph_seq, results_file)
        freefield.wait_to_finish_playing()
    else:
        stimulus = stim_dict[morph_ratios[morph-1]]
        stimulus.level = stimulus_level
        load_to_buffer(stimulus)
        trig_value = morph
        freefield.write(tag='trigcode', value=trig_value, processors='RX82')
        freefield.play()
        print('Playing morph ', morph_ratios[morph-1])
        collect_trial(morph_seq, results_file)
        freefield.wait_to_finish_playing(proc="RP2", tag="playback")


results_file.write(morph_seq, tag='sequence')
print("Saved participant responses")
