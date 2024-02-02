"""Max's code for the Neuro 2 Praktikum 2023 downloaded from the GitHub repository """
from labplatform.core.Setting import ExperimentSetting
from labplatform.core.ExperimentLogic import ExperimentLogic
from labplatform.core.Data import ExperimentData
from labplatform.core.Subject import Subject
from labplatform.config import get_config
import os
from traits.api import Str, Int, Dict, Float, Any
import slab
import time
import logging
import random
from experiment.RXRP2Device import RX8RP2Device
from experiment.config import vocoding_config


# TODO




log = logging.getLogger(__name__)
cfg = voice_detection_behavior_config #TODO specific directory required?


class VoiceDetectionSetting(ExperimentSetting):
    experiment_name = Str('VoiceDetection', group='status', dsec='name of the experiment', noshow=True)
    conditions = Int(cfg.conditions, group="primary", dsec="Number of different morph steps")
    trial_number = Int(cfg.trial_number, group='status', dsec='Number of trials in each condition')
    trial_watch = Float(cfg.trial_duration, group='status', dsec='Duration of each stimulus, (s)')
    #deviant_freq = Float(cfg.deviant_freq, group='status', dsec='Deviant frequency')
    setup = Str("FREEFIELD", group="status", dsec="Name of the experiment setup")

    def _get_total_trial(self):
        return self.trial_number * len(self.conditions)


class VoiceDetectionExperiment(ExperimentLogic):

    setting = VoiceDetectionSetting()
    data = ExperimentData()  # dont worry about this
    results = Any()
    devices = Dict()
    sequence = slab.Trialsequence(conditions=setting.conditions,
                                  n_reps=setting.trial_number,
                                  deviant_freq=setting.deviant_freq)

    stim_path = os.path.join(get_config("SOUND_ROOT"), "neurobio2_2023\\vocoding", "normalized_2") # TODO syntax of dir?
    stim_dict = dict()
    sound_to_play = Any()
    deviant_sound = slab.Binaural.chirp(duration=0.1, samplerate=48828.0)  # same length as other stimuli
    response = Int()
    time_0 = Float()
    rt = Any()
    #trig_code = Any()

    def _devices_default(self):
        rx8rp2 = RX8RP2Device()
        return {"RX8RP2": rx8rp2}

    def _initialize(self):
        pass

    def _pause(self):
        pass

    def _stop(self):
        pass

    def setup_experiment(self, info=None):
        self.load_stimuli()

    def prepare_trial(self): #TODO trigger related stuff can be removed? Response time?
        this_condition = self.sequence.__next__()
        #if this_condition != 0:
        #    self.trig_code = list(self.stim_dict.keys()).index(this_condition) + 1  # eeg trigger code
        #else:
        #    self.trig_code = 6  # deviant
        #self.devices["RX8RP2"].handle.write("trigcode", self.trig_code, procs="RX82")
        # print(self.trig_code)
        # print(self.devices["RX8RP2"].handle.read("trigcode", proc="RX82"))
        #if not this_condition == 0:
        self.sound_to_play = random.choice(self.stim_dict[this_condition])
        #elif this_condition == 0:
            #self.sound_to_play = self.deviant_sound
        self.load_to_buffer(sound=self.sound_to_play)
        self.results.write(self.sequence.this_n, "trial_n")
        self.results.write(this_condition, "condition_this_trial")

    def start_trial(self):
        self.time_0 = time.time()  # starting time of the trial
        self.devices["RX8RP2"].start()
        self.devices["RX8RP2"].wait_to_finish_playing(proc="RP2")
        # self.sound_to_play.play()
        #if self.sequence.this_trial == 0: #TODO If statement can be removed->button press is always required
        self.devices["RX8RP2"].wait_for_button()
        self.response = self.devices["RX8RP2"].get_response()
        self.results.write(data=self.response, tag="response")
        self.rt = int(round(time.time() - self.time_0, 3) * 1000)
        self.results.write(data=self.rt, tag="reaction_time")

    def stop_trial(self):
        self.devices["RX8RP2"].pause()

    def load_stimuli(self): # TODO less complicated since only 10 sound files in dir->how change? Differen dirs for behavior and EEG experiment?!
        for directory in os.listdir(self.stim_path):
            sound_list = list()
            for sound_file in os.listdir(os.path.join(self.stim_path, directory)):
                sound = slab.Sound.read(os.path.join(self.stim_path, directory, sound_file))
                sound_list.append(sound)
            self.stim_dict[directory] = sound_list
        ori_sound_list = list()
        for ori_sound_file in os.listdir(os.path.join(get_config("SOUND_ROOT"), "neurobio2_2023\\vocoding\\original\\N_LUFS")):  # TODO syntax of dir? Why different to before?
            ori_sound = slab.Sound.read(os.path.join(get_config("SOUND_ROOT"), "neurobio2_2023\\vocoding\\original\\N_LUFS", ori_sound_file))  # TODO syntax of dir? Why different to before?
            ori_sound_list.append(ori_sound)
        self.stim_dict["original"] = ori_sound_list

    def load_to_buffer(self, sound):
        left = sound.channel(0).data.flatten()
        right = sound.channel(1).data.flatten()
        self.devices["RX8RP2"].handle.write("playbuflen", sound.n_samples, "RP2")
        self.devices["RX8RP2"].handle.write("data_l", left, "RP2")
        self.devices["RX8RP2"].handle.write("data_r", right, "RP2")

    """
    def clear_buffer(self):
        buffer_size = self.setting.trial_watch * self.devices["RX8RP2"].setting.device_freq
        self.devices["RX8RP2"].handle.write("data_l", left, "RP2")
        self.devices["RX8RP2"].handle.write("data_r", right, "RP2")
    """


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    log.addHandler(ch)

    # initialize subject
    print("Enter subject id:")
    subject_name= input()
    subject = Subject(name=subject_name, group="EEG", species="Human")
    subject.data_path = os.path.join(get_config("DATA_ROOT"), f"{subject.name}.h5")
    try:
        subject.add_subject_to_h5file(os.path.join(get_config("SUBJECT_ROOT"), f"{subject.name}.h5"))
    except ValueError:
        subject.read_info_from_h5file(os.path.join(get_config("SUBJECT_ROOT"), f"{subject.name}.h5"))

    exp = VoiceDetectionExperiment(subject=subject)
    exp.results = slab.ResultsFile(subject=subject.name, folder=get_config("DATA_ROOT"))
    exp.start() # to run the experiment
