import json
import matplotlib.pyplot as plt
import numpy as np
import mne
from os import listdir
import pandas as pd
import seaborn as sns
import pathlib
from os.path import join
import os
import pythonpsignifitmaster.psignifit as ps
from matplotlib import cm
from matplotlib.colors import ListedColormap,LinearSegmentedColormap



#Read in epochs and evokeds
    # retrieves epochs and evokeds for one subject
DIR = pathlib.Path(os.getcwd())
sub_DIR = DIR / "analysis" / "results" /"study"/ "EEG"
with open(DIR / "analysis"  / "settings" / "preproc_config.json") as file:
    cfg = json.load(file)


evokeds = cfg["epochs"][f"event_id"].copy()
for key in cfg["epochs"][f"event_id"]:
    evokeds[key] = list()


# Read in the evokeds for one subject
evokeds_folder = sub_DIR / "sub_02" / "evokeds"
evoked = mne.read_evokeds(evokeds_folder / pathlib.Path('sub_02-ave.fif'))


# Plot the results for one subject

# Combined evokeds
combined_evokeds= mne.combine_evoked([evoked[1],evoked[2], evoked[3],evoked[4]],weights=[0.25, 0.25, 0.25, 0.25])
combined_evokeds.plot_topomap([-0.2,-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
combined_evokeds.plot_joint()
mne.viz.plot_evoked(combined_evokeds, gfp=True)

# Compared evokeds
evokeds=evoked[1:len(evoked)]


Blues_modified = cm.get_cmap('Blues', 256)
newcmp = ListedColormap(Blues_modified(np.linspace(0.2, 0.99, 256)))


mne.viz.plot_compare_evokeds(evokeds, picks=["FCz"],show_sensors=True,legend= True)
mne.viz.plot_compare_evokeds([evoked[4], evoked[1]], picks=["FCz"],show_sensors=True,legend= True)


""""
# Plot compared evokeds and envelopes at the same time
from os.path import join
import slab
def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))
all_file_names2 = [f for f in abs_file_paths("/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/stimuli/sound_files/peak_aligned")]

sound_analysis=dict()
for sound_file2 in all_file_names2:
    sound = slab.Sound(sound_file2)
    morph_ratio = float(str(sound_file2)[-7:-4])
    envelope = sound.envelope()
    sound_analysis[morph_ratio] = {
        "Envelope Cut Sound": envelope.data[:, 0]
    }


mne.viz.plot_compare_evokeds(evokeds, picks=["FCz"],show_sensors=True,legend= True)

plt.figure()
x=list(np.arange(0, len(sound_analysis[0.0]["Envelope Cut Sound"]), 1))
x = [x / sound.samplerate for x in x]
plt.plot(x,sound_analysis[0.0]["Envelope Cut Sound"], color="blue", label="morph 0.0")

plt.plot(x,sound_analysis[1.0]["Envelope Cut Sound"], color="darkorange",label="morph 1.0")
"""

# Difference wave
diff_wave_1 = mne.combine_evoked([evoked[4], evoked[1]],weights=[1, -1])
diff_wave_2 = mne.combine_evoked([evoked[4], evoked[2]],weights=[1, -1])
diff_wave_3 = mne.combine_evoked([evoked[4], evoked[3]],weights=[1, -1])

mne.viz.plot_compare_evokeds([diff_wave_1, diff_wave_2, diff_wave_3], picks=["FCz"],show_sensors=True,legend= True)


diff_wave_1.plot_topomap([-0.2,-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
diff_wave_2.plot_topomap([-0.2,-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
diff_wave_3.plot_topomap([-0.2,-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5])



# Get behavioral data from test
data_dir= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/analysis/data/study/sub_02'
files = [file for file in listdir(data_dir) if file.endswith('.csv')]
files = [k for k in files if 'experiment' in k]
appended_data = []
for file in files:
    data = pd.read_csv(data_dir + '/' + file)
    appended_data.append(data)
results_df = pd.concat(appended_data)

morphs= list(results_df['Morph played'].unique())
results_dict=dict()
i=0
for morph in morphs:
    df_sub = results_df[results_df["Morph played"] == morph]
    response_count = list(df_sub['Response'].value_counts().values)
    responses = list(df_sub['Response'].value_counts().index.values)
    if len(response_count) != 1:
        no = response_count[responses.index(2)]
        yes = response_count[responses.index(1)]
    elif 2 not in responses:
        no = 0
        yes = response_count[responses.index(1)]
    elif 1 not in responses:
        no = response_count[responses.index(2)]
        yes = 0
    results_dict[str(i)] = {"Morph ratio": morph, "Voice responses": yes, "N": sum(response_count) }
    i = i + 1

df_EEG_sum=pd.DataFrame.from_dict(results_dict, orient='index')
df_EEG_sum["%Voice"] = (df_EEG_sum["Voice responses"] / df_EEG_sum["N"])
df_EEG_sum=df_EEG_sum.sort_values(by=['Morph ratio']).sort_values(by=['Morph ratio'])
df_EEG_sum['Morph ratio'] = df_EEG_sum['Morph ratio'].astype(float)


def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))


test= df_EEG_sum.copy()
data_np=test.to_numpy()
options = dict()  # initialize as an empty dictionary
options['sigmoidName'] = 'norm'  # choose a cumulative Gauss as the sigmoid
options['expType'] = 'equalAsymptote'
result = ps.psignifit(data_np, options)
PSE=result['Fit'][0]
ps.psigniplot.plotPsych(result, extrapolLength = 0.01)


"""
# Measure the amplitude between 190 and 260
amps= []
for i in range(len(evokeds)):
    evoked=evokeds[i]
    tmin= 0.190
    tmax= 0.260
    data=evoked.get_data(["FC6"], tmin=tmin, tmax=tmax, units="uV")
    amp = np.mean(data)
    result=("FC6",evoked.comment, amp)
    amps.append(result)
for i in range(len(evokeds)):
    evoked=evokeds[i]
    tmin= 0.190
    tmax= 0.260
    data=evoked.get_data(["FC5"], tmin=tmin, tmax=tmax, units="uV")
    amp = np.mean(data)
    result=( "FC5",evoked.comment, amp)
    amps.append(result)

# Plot amplitude
amps_2=[]
for element in amps:
    if element[1]=="morph/0.0":
        amp= (element[0], element[1], element[2], 0.0)
    if element[1] == "morph/0.5":
        amp= (element[0], element[1], element[2], 0.5)
    if element[1] == "morph/1.0":
        amp= (element[0], element[1], element[2], 1.0)
    amps_2.append(amp)

df_amp = pd.DataFrame(amps_2, columns =['electrode', 'cat', 'amp', "Morph ratio"])
df_final=pd.merge(df_EEG_sum, df_amp, on='Morph ratio')

sns.barplot(data=df_amp, x="Morph ratio", y= "amp",hue="electrode")
plt.title("Amplitude between 190 and 260 ms ")


# Plot amplitude and behavior
df=pd.merge(df_final, df_EEG_sum, on='Morph ratio')
sns.scatterplot(data=df, x="%Voice_y", y="amp", hue="electrode")
sns.lineplot(data=df, x="%Voice_y", y="amp", hue= "electrode")
plt.title("Amplitude between 190 and 260 ms ")
"""