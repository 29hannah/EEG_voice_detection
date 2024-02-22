"""Code to analyze the behavioral data collected
-> Select the stimuli for the EEG experiment based on behavioral pilot data
"""
import os
from analysis.behavioral_summarize_data import summarize_data
from os import listdir
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DIR = "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/analysis"
data_DIR= DIR+ '/data/pilot/'
results_DIR= DIR + "/results/pilot/"
out_DIR_raw= results_DIR +"raw"
out_DIR_sum=  results_DIR +"sum"
out_DIR_plots=  results_DIR +"plots"


dirs= [results_DIR, out_DIR_raw, out_DIR_sum, out_DIR_plots]
for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("path did not exist, path created")

ids = list(name for name in os.listdir(data_DIR)
           if os.path.isdir(os.path.join(data_DIR, name)))
ids = [k for k in ids if '.DS_Store' not in k]

# Only necessary when running the analysis for the first time/making changes to the code summarizing the data
for id in ids:
    print(id)
    summarize_data(id, data_DIR, out_DIR_raw, out_DIR_sum)

# Read in the summarized files per participant and append data frames
files_sum = [file for file in listdir(out_DIR_sum) if file.endswith('.csv')]
appended_data = []
for file in files_sum:
    data = pd.read_csv(out_DIR_sum + '/' + file)
    appended_data.append(data)
results = pd.concat(appended_data)

# Get the data for the final stimuli
# Calculate stdev over participants: Subset to morph ratio, calculate stdev over participants % Voice
morph_ratios = list(results["Morph ratio"].unique())
stdev_results= dict()
i=1
for morph_ratio in morph_ratios:
    df = results[results["Morph ratio"] == morph_ratio]
    stdev_results[str(i)]={"Morph ratio": morph_ratio , "stdev %voice": df['%Voice'].std()}
    i=i+1

results_stdev = pd.DataFrame.from_dict(stdev_results)
results_stdev = results_stdev.swapaxes("index", "columns")
results_stdev.to_csv(results_DIR + '/stdev_responses')


# Plot the stdev
f, axes = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [2, 1]})
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.lineplot(data=results, x=results["Morph ratio"], y=results["%Voice"], hue=results["Id"], ax=axes[0])
sns.scatterplot(data=results, x=results["Morph ratio"], y=results["%Voice"], hue=results["Id"], legend=False,ax=axes[0])

sns.lineplot(data=results_stdev, x=results_stdev["Morph ratio"], y=results_stdev["stdev %voice"], ax=axes[1])
plt.xticks(ticks=morph_ratios)
plt.savefig(out_DIR_plots+ "/behavioral_data_raw+stdev")

# Read in the raw files per participant and append data frames
files_raw = [file for file in listdir(out_DIR_raw) if file.endswith('.csv')]
appended_data = []
for file in files_raw:
    data = pd.read_csv(out_DIR_raw + '/' + file)
    appended_data.append(data)
results_raw = pd.concat(appended_data)

for id in ids:
    f, axes = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 1]})
    df_sub= results_raw[results_raw['Id'] == id]
    df_sub_sum=results[results['Id'] == id]
    sns.scatterplot(data=df_sub, x=df_sub_sum["Morph ratio"], y=df_sub_sum["%Voice"], legend=False,
                    ax=axes[0]).set_title(id)
    sns.lineplot(data=df_sub, x=df_sub_sum["Morph ratio"], y=df_sub_sum["%Voice"], legend=False,
                    ax=axes[0])
    sns.boxplot(data=df_sub, x=df_sub['Morph ratio'], y=df_sub['Reaction time'])
    plt.ylim(-1000, 5000)
    plt.savefig(out_DIR_plots + "/ rt_"+id )
    plt.close()

# Analysis new file format
appended_data = []
for id in ids:
    files= [file for file in listdir(data_DIR+id) if file.endswith('.csv')]
    file = [k for k in files if 'experiment'  in k]
    data = pd.read_csv(data_DIR+id + '/' + file[0])
    appended_data.append(data)
results_df = pd.concat(appended_data)


conditions= list(results_df["Morph played"].unique())
results=dict()
i=1
for id in ids:
    df_sub = results_df[results_df['Participant'] == id]
    for condition in conditions:
        df = df_sub[df_sub["Morph played"] == condition]
        morph= df['Morph played'].iloc[0]
        response_count=list(df['Response'].value_counts().values)
        responses = list(df['Response'].value_counts().index.values)
        if len(response_count)!=1:
            no= response_count[responses.index(2.0)]
            yes= response_count[responses.index(1.0)]
        elif 2.0 not in responses:
            no=0
            yes= response_count[responses.index(1.0)]
        elif 1.0 not in responses:
            no =response_count[responses.index(2.0)]
            yes =0
        results[str(i)] = {"Condition": condition, "Morph ratio": morph,  "Voice responses":yes, "N": sum(response_count),
                           "Participant":id
                           }
        i=i+1
results_sum_df= pd.DataFrame.from_dict(results)
results_sum_df = results_sum_df.swapaxes("index", "columns")

results_sum_df["%Voice"] = (results_sum_df["Voice responses"] / results_sum_df["N"])

for id in ids:
    f, axes = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 1]})
    df_sub= results_sum_df[results_sum_df['Participant'] == id]
    sns.scatterplot(data=df_sub, x=df_sub["Morph ratio"], y=df_sub["%Voice"], legend=False,
                    ax=axes[0]).set_title(id)
    sns.lineplot(data=df_sub, x=df_sub["Morph ratio"], y=df_sub["%Voice"], legend=False,
                    ax=axes[0])
    sns.boxplot(data=results_df, x=results_df['Morph played'], y=results_df['Reaction time'])
    plt.ylim(-1000, 5000)
    plt.savefig(out_DIR_plots + "/ rt_"+id )
    plt.close()
