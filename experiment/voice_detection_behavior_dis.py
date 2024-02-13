import slab
import freefield
import pathlib
import numpy
import os
from EEG_voice_detection.experiment.config import get_config
import time



# TODO check transitions between morphs
# TODO check response time


participant_id = 'hannah_1202'
stimulus_level=67
phase= 'experiment'# Can either be training or experiment

slab.set_default_samplerate(44100)
DIR = pathlib.Path(os.getcwd())

config = get_config()
proc_list = config['proc_list']
freefield.initialize('dome', zbus=True, device=proc_list)
freefield.set_logger('WARNING')


def crop_sound(sound):
    left = slab.Sound.sequence(sound.left)
    right = slab.Sound.sequence(sound.right)
    out = slab.Binaural([left, right])
    return out

def load_to_buffer(sound):
    out = crop_sound(sound)
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
    print('[Response ' + str(response) + ']', str(seq.this_n) + ')')
    # while freefield.read(tag="playback", n_samples=1, processor="RP2"):
        # time.sleep(0.01)


results_folder = 'C:\\projects\\EEG_voice_detection\\experiment\\results\\behavior'
results_file = slab.ResultsFile(subject=participant_id, folder=results_folder)
results_file.write(phase, tag='stage')



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

input('Press enter to start the experiment')

if phase=='training':
    morph_seq = slab.Trialsequence(conditions=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], trials=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], n_reps=1)
if phase=='experiment':
    morph_seq = slab.Trialsequence(conditions=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], n_reps=21)

for morph in morph_seq:
    stimulus= stim_dict[morph_ratios[morph-1]]
    load_to_buffer(stimulus)
    freefield.play()
    print('Playing morph ', morph_ratios[morph-1])
    freefield.wait_to_finish_playing(proc="RP2", tag="playback")
    collect_responses(morph_seq, results_file)
    time.sleep(0.5) #wait 0.5 secs before playing the next stimulus-> in a sense the isi

results_file.write(morph_seq, tag='sequence')
print("Saved participant responses")