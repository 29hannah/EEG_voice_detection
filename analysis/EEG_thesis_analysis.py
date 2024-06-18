import json
import matplotlib.pyplot as plt
import mne
from os import listdir
import pandas as pd
import pathlib
import os
import seaborn as sns

# TODO: models
# TODO localizer??
# TODO component analysis 

"""This script contains code to analyze our data 
It consists of three parts 
1) Within subject analysis: explore and plot the data for one subject 
2) Over subjects analysis: explore and plot the data over all subjects (=grand average) 
3) Correlation EEG amplitude: get mean amplitude per subject and test hypothesized models
"""

# Set directories
DIR = pathlib.Path(os.getcwd())
behavior_results_DIR = DIR / "analysis" / "results" /"study"/ "behavior"
with open(DIR / "analysis" / "settings" / "preproc_config.json") as file:
    cfg = json.load(file)


### Analysis within participants ###
subj= "sub_15" # Define which participant's data to analyse


# Define directories for subject
EEG_DIR = DIR / "analysis" / "results" /"study"/ "EEG"/ subj / "evokeds"
#EEG_DIR = DIR / "analysis" / "results" /"pilot"/ "EEG"/ subj / "evokeds"
evoked = mne.read_evokeds(EEG_DIR / pathlib.Path(subj+'-ave.fif'))
behavior_dir= DIR / "analysis" / "data" /"study"/  subj
plots_DIR= DIR / "analysis" / "results" /"study"/ "plots" / subj
if not os.path.isdir(plots_DIR):
        os.makedirs(plots_DIR)

# Plot the topo map
combined_evokeds= mne.combine_evoked([evoked[1],evoked[2], evoked[3],evoked[4]],weights=[0.25, 0.25, 0.25, 0.25])
fig= combined_evokeds.plot_topomap([-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
fig.savefig(str(plots_DIR) + '/' + 'topo-map_combined-evokeds_'+ subj + '.pdf')
plt.close()

# Plot the compared evokeds
picks= "FCz"
fig=mne.viz.plot_compare_evokeds([evoked[1],evoked[2], evoked[3],evoked[4]],
                             picks=picks,truncate_xaxis= -0.1, colors=["firebrick", "lightsalmon", "lightblue", "darkblue"],
                             show_sensors=True, legend="lower right")
fig[0].savefig(str(plots_DIR) + '/' + 'compared-evokeds_'+ subj + '_'+ picks +'.pdf')
plt.close()

# Plot the difference waves
picks= "FCz"
diff_wave1= mne.combine_evoked([evoked[4],evoked[1]],weights=[1, -1])
diff_wave2= mne.combine_evoked([evoked[4],evoked[2]],weights=[1, -1])
diff_wave3= mne.combine_evoked([evoked[4],evoked[3]],weights=[1, -1])

fig=mne.viz.plot_compare_evokeds([diff_wave1,diff_wave2, diff_wave3],
                             picks=picks,truncate_xaxis= -0.1, colors=["#D9614E", "#B07D84", "#591157"],
                             show_sensors=True, legend="lower right")

fig[0].savefig(str(plots_DIR) + '/' + 'difference-waves_compared-evokeds_'+ subj + '_'+ picks +'.pdf')
plt.close()

# Get the difference topo maps (for now, adjust vlim based on plot above)
fig, axs = plt.subplots(1,3)
fig.set_size_inches(10, 7)
time = 0.3
fig.suptitle("Time: "+ str(time) + "s", y=0.75, fontsize= 18)
diff_wave1.plot_topomap([time], axes=axs[0], colorbar=False, vlim=(-2.5, 2.5))
axs[0].set_title("morph 1.0 - morph 0.0", fontsize=14)
diff_wave2.plot_topomap([time], axes=axs[1], colorbar=False, vlim=(-2.5, 2.5))
axs[1].set_title("morph 1.0 - morph 0.4", fontsize=14)
diff_wave3.plot_topomap([time], axes=axs[2], colorbar=False, vlim= (-2.5, 2.5))
axs[2].set_title("morph 1.0 - morph 0.6", fontsize=14)
fig.savefig(str(plots_DIR) + '/' + 'difference-waves_topo-map_'+ subj + '.pdf')
plt.close()


# Summarize and plot the behavioral data
files = [file for file in listdir(behavior_dir) if file.endswith('.csv')]
files = [k for k in files if 'experiment' in k]
data = pd.read_csv(str(behavior_dir) + '/' + files[0])

morphs= list(data['Morph played'].unique())
results_dict=dict()
i=0
for morph in morphs:
    df_sub = data[data["Morph played"] == morph]
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

results=pd.DataFrame.from_dict(results_dict, orient='index')
results["%Voice"] = (results["Voice responses"] / results["N"])
results=results.sort_values(by=['Morph ratio']).sort_values(by=['Morph ratio'])
results['Morph ratio'] = results['Morph ratio'].astype(float)
results = results.assign(subj=[subj] * len(morphs))
results.to_csv(str(behavior_results_DIR) +'/'+ subj + '_summarized-behavior.csv')

sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_theme(rc={'figure.figsize':(8, 6)})
plot=sns.lineplot(data=results, x=results["Morph ratio"], y=results["%Voice"])
plot.set_ylim(0,1)
sns.scatterplot(data=results, x=results["Morph ratio"], y=results["%Voice"]).set_title(subj)
fig = plot.get_figure()
fig.savefig(str(plots_DIR) + '/' + 'behavioral_data_'+ subj + '.pdf')
plt.close()





### Analysis over participants ###
data_DIR= EEG_DIR = DIR / "analysis" / "results" /"study"/ "EEG"
ids = list(name for name in os.listdir(data_DIR)
               if os.path.isdir(os.path.join(data_DIR, name)))
subjs=['sub_08', 'sub_09', 'sub_10', 'sub_11', 'sub_07', 'sub_12','sub_13', 'sub_14']

# Behaviour
appended_data = []
for subj in subjs:
    data = pd.read_csv(str(behavior_results_DIR) +'/'+ subj + '_summarized-behavior.csv')
    appended_data.append(data)

df_behav = pd.concat(appended_data)

sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_theme(rc={'figure.figsize':(8, 6)})

#Boxplot to visualise
sns.catplot(data=df_behav, x="Morph ratio", y="%Voice", kind="box")

# Histograms to visualise
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, sharey=True)

sns.histplot(data=df_behav[df_behav["Morph ratio"] == 0.0], x="%Voice", binwidth=0.1, ax=ax1)
sns.histplot(data=df_behav[df_behav["Morph ratio"] == 0.4], x="%Voice", binwidth=0.1, ax=ax2)
sns.histplot(data=df_behav[df_behav["Morph ratio"] == 0.6], x="%Voice", binwidth=0.1, ax=ax3)
sns.histplot(data=df_behav[df_behav["Morph ratio"] == 1.0], x="%Voice", binwidth=0.1, ax=ax4)

# EEG
evokeds_subj={}
evokeds00=list()
evokeds04=list()
evokeds06=list()
evokeds10=list()
for subj in subjs:
    EEG_DIR = DIR / "analysis" / "results" / "study" / "EEG" / subj / "evokeds"
    if subj== 'sub_07':
        evoked = mne.read_evokeds(EEG_DIR / pathlib.Path('sub07-ave.fif'))
    else:
        evoked = mne.read_evokeds(EEG_DIR / pathlib.Path(subj + '-ave.fif'))
    for evok in evoked:
        if evok.comment=='morph/0.0':
            evokeds00.append(evok)
        elif evok.comment=='morph/0.4':
            evokeds04.append(evok)
        elif evok.comment == 'morph/0.6':
            evokeds06.append(evok)
        elif evok.comment == 'morph/1.0':
            evokeds10.append(evok)
    evokeds_subj[subj]= evoked


# Get the amplitude per subject
channels = ["FC6", "FC5", "FCz"]
tmin= 0.19
tmax= 0.26

results = []
for subj in subjs:
    behavior_df= df_behav[df_behav["subj"]==subj]
    evoked = evokeds_subj[subj]
    for channel in channels:
        morph00 = evoked[1].copy().pick(channel).crop(tmin=tmin, tmax=tmax)
        morph04 = evoked[2].copy().pick(channel).crop(tmin=tmin, tmax=tmax)
        morph06 = evoked[3].copy().pick(channel).crop(tmin=tmin, tmax=tmax)
        morph10 = evoked[4].copy().pick(channel).crop(tmin=tmin, tmax=tmax)
        # Extract mean amplitude in µV over time
        mean_amp_morph00 = morph00.data.mean(axis=1) * 1e6
        mean_amp_morph04 = morph04.data.mean(axis=1) * 1e6
        mean_amp_morph06 = morph06.data.mean(axis=1) * 1e6
        mean_amp_morph10 = morph10.data.mean(axis=1) * 1e6

        result = [(subj, 0.0, channel, tmin, tmax, mean_amp_morph00[0],
                   behavior_df[behavior_df["Morph ratio"] == 0.0]['%Voice'].iloc[0]),
                  (subj, 0.4, channel, tmin, tmax, mean_amp_morph04[0],
                   behavior_df[behavior_df["Morph ratio"] == 0.4]['%Voice'].iloc[0]),
                  (subj, 0.6, channel, tmin, tmax, mean_amp_morph06[0],
                   behavior_df[behavior_df["Morph ratio"] == 0.6]['%Voice'].iloc[0]),
                  (subj, 1.0, channel, tmin, tmax, mean_amp_morph10[0],
                   behavior_df[behavior_df["Morph ratio"] == 1.0]['%Voice'].iloc[0])
                  ]
        results.extend(result)

df_amp = pd.DataFrame(results, columns=['subj', 'morph', 'channel', 'tmin', 'tmax', 'amp', '%Voice'])
df_amp.to_csv('/Users/hannahsmacbook/EEG_voice/summarized-behavior-EEG.csv')

# Get averaged evokeds over subjects
avrgd_evokeds= {"morph 0.0": mne.grand_average(evokeds00),
    "morph 0.4": mne.grand_average(evokeds04),
    "morph 0.6": mne.grand_average(evokeds06),
    "morph 1.0": mne.grand_average(evokeds10)
}

# Plot the compared evokeds
picks= "FCz"
fig=mne.viz.plot_compare_evokeds([avrgd_evokeds["morph 0.0"],
                                  avrgd_evokeds["morph 0.4"],
                                  avrgd_evokeds["morph 0.6"],
                                  avrgd_evokeds["morph 1.0"]],
                             picks=picks,truncate_xaxis= -0.1, colors=["firebrick", "lightsalmon", "lightblue", "darkblue"],
                             show_sensors=True, legend="lower right")



