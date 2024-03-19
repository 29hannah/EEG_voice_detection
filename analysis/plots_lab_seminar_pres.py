import json
import numpy as np
import pathlib
import os
import mne
from matplotlib import cm
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
from os import listdir
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#Read in epochs and evokeds
    # retrieves epochs and evokeds for one subject
DIR = pathlib.Path(os.getcwd())
sub_DIR = DIR / "analysis" / "results" /"pilot"/ "EEG"
with open(DIR / "analysis"  / "settings" / "preproc_config.json") as file:
    cfg = json.load(file)

# Read in the evokeds for one subject
evokeds_folder = sub_DIR / "tade_2902" / "evokeds"
evoked = mne.read_evokeds(evokeds_folder / pathlib.Path('tade_2902-ave.fif'))

evokeds=evoked[1:4]

# Plot compared evokeds
cmap = ListedColormap(["green", "blue", "red"])

ax=mne.viz.plot_compare_evokeds(evokeds, picks=["FC6"],show_sensors=True, legend= "lower right", ylim=dict(eeg=[-3, 3]))
ax.set_xlim(0,0.3)
plt.savefig("FC6 tade.pdf", dpi=800)
plt.close()

mne.viz.plot_compare_evokeds(evokeds, picks=["FC5"],show_sensors=True,legend= "lower right", ylim=dict(eeg=[-3, 3]))
plt.savefig("FC5 tade.pdf", dpi=800)
plt.close()

# Measure the amplitude between 190 and 260
amps= []
for i in range(len(evokeds)):
    evoked=evokeds[i]
    tmin= 0.190
    tmax= 0.260
    data=evoked.get_data(["FC6"], tmin=tmin, tmax=tmax, units="uV")
    amp = np.mean(data)
    result=( "FC6",evoked.comment, amp)
    amps.append(result)
for i in range(len(evokeds)):
    evoked=evokeds[i]
    tmin= 0.190
    tmax= 0.260
    data=evoked.get_data(["FC5"], tmin=tmin, tmax=tmax, units="uV")
    amp = np.mean(data)
    result=( "FC5",evoked.comment, amp)
    amps.append(result)




# Get behavioral data from EEG
data_dir= '/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/analysis/data/pilot/tade_2902'
files = [file for file in listdir(data_dir) if file.endswith('.csv')]
files = [k for k in files if 'EEG' in k]

appended_data = []
for file in files:
    data = pd.read_csv(data_dir + '/' + file)
    appended_data.append(data)
results_df = pd.concat(appended_data)
# Get the behavioral data in adequate form
results=[]
for file in files:
    data = pd.read_csv(data_dir + '/' + file)
    for i in range(len(data)):
        if data.loc[i, "Morph played"]== 'Deviant' and i!=0:
            morph= data.loc[i-1, "Morph played"]
            response= data.loc[i, "Response"]
            rt=data.loc[i, "Reaction time"]
            result= (morph, response, rt)
            results.append(result)

results_final = [result for result in results if result[0] not in (('Deviant'))]

df = pd.DataFrame(results_final, columns=['Morph', 'Response', 'RT'])

morphs= list(df['Morph'].unique())

results_dict=dict()
i=0
for morph in morphs:
    df_sub = df[df["Morph"] == morph]
    response_count = list(df_sub['Response'].value_counts().values)
    responses = list(df_sub['Response'].value_counts().index.values)
    if len(response_count) != 1:
        no = response_count[responses.index('2')]
        yes = response_count[responses.index('1')]
    elif '2' not in responses:
        no = 0
        yes = response_count[responses.index('1')]
    elif '1' not in responses:
        no = response_count[responses.index('2')]
        yes = 0
    results_dict[str(i)] = {"Morph ratio": morph, "Voice responses": yes, "N": sum(response_count) }
    i = i + 1

df_EEG_sum=pd.DataFrame.from_dict(results_dict, orient='index')
df_EEG_sum["%Voice"] = (df_EEG_sum["Voice responses"] / df_EEG_sum["N"])
df_EEG_sum=df_EEG_sum.sort_values(by=['Morph ratio']).sort_values(by=['Morph ratio'])
df_EEG_sum['Morph ratio'] = df_EEG_sum['Morph ratio'].astype(float)


# Plot amplitude and behavior
amps_2=[]
for element in amps:
    if element[1]=="category/0":
        amp= (element[0], element[1], element[2], 0.0)
    if element[1] == "category/1":
        amp= (element[0], element[1], element[2], 0.5)
    if element[1] == "category/2":
        amp= (element[0], element[1], element[2], 1.0)
    amps_2.append(amp)

df_amp = pd.DataFrame(amps_2, columns =['electrode', 'cat', 'amp', "Morph ratio"])

df_final=pd.merge(df_EEG_sum, df_amp, on='Morph ratio')

sns.barplot(data=df_final, x="Morph ratio", y= "amp",hue="electrode")
plt.savefig("amp raw tade.pdf", dpi=800)
plt.close()