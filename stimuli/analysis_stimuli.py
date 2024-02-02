"Analysis of the morph stimuli"
import slab
import pathlib
from os.path import join
import os
import seaborn as sns
import parselmouth
import numpy as np
import glob
from parselmouth.praat import call
import pandas as pd
import matplotlib.pyplot as plt


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))

folder_path = pathlib.Path
folder_path= '/Users/hannahsmacbook/PycharmProjects/AVH/stimuli/sound_files/whisper_2/resampled_rms-norm_morphs_behavior_Leipzig'

all_file_names = [f for f in abs_file_paths(folder_path)]
all_file_names.sort()



# functions to create color gradient
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]


sound_analysis=dict()
# Acoustic features->slab
for sound_file in all_file_names:
    sound = slab.Binaural(sound_file)
    morph_ratio= float(str(sound_file)[-7:-4])
    centroid = sound.spectral_feature(feature='centroid')[1]
    flux= sound.spectral_feature(feature='flux')[1]
    flatness = sound.spectral_feature(feature='flatness')[1]
    rolloff = sound.spectral_feature(feature='rolloff')[1]
    crest_factor= sound.crest_factor()
    onset_slope = sound.onset_slope()
    envelope = sound.envelope()

    sound_analysis[morph_ratio] = {
        "Centroid": centroid,
        "Flux": flux,
        "Flatness": flatness,
        "Rolloff": rolloff,
        "Crest Factor": crest_factor,
        "Onset slope": onset_slope,
        "Envelope": envelope.data[:,0],
        "Sound": sound.data[:,0]
    }



# Praat parselmouth
def harmonicity_analysis(sound):
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    hnr=[hnr]
    return hnr
def mfcc_analysis(sound):
    mfcc=sound.to_mfcc()
    mfcc_values = mfcc.to_matrix_features().values
    mfcc_mean= (np.mean(mfcc_values, axis=1)).tolist()
    return mfcc_mean

praat_analysis = dict()
for wave_file in glob.glob(folder_path + "/*.wav"):
    sound = parselmouth.Sound(wave_file)
    morph_ratio = float(wave_file[-7:-4])
    hnr = harmonicity_analysis(sound)
    mfcc_mean = mfcc_analysis(sound)
    praat_analysis[morph_ratio] = {
        "HNR": hnr[0],
        "MFCC": mfcc_mean[0]}


df_slab= pd.DataFrame.from_dict(sound_analysis)
df_praat= pd.DataFrame.from_dict(praat_analysis)
df= pd.concat([df_slab, df_praat])

features= df.axes[0].tolist()




#Plotting the results

#Setting color gradient
color2 = "#000000 "
color1 = "#ADD8E6"
num_points=11
colors=get_color_gradient(color1, color2, num_points)


for feature in features:
        x=list(sound_analysis.keys())
        y=list()
        for morph in x:
            value=df[morph][feature]
            y.append(value)
        plt.figure()
        if feature != "Envelope" and feature != "Sound":
            sns.regplot(x=x, y=y).set_title(feature)
        if feature == "Envelope" or feature == "Sound":
         fig, ax = plt.subplots()
         for i in range(len(y)):
             ax.plot(y[i],color= colors[i],  label=str(x[i]))
             leg = ax.legend()





# Plot spectra
for sound_file in all_file_names:
    sound = slab.Binaural(sound_file)
    sound.spectrum()




