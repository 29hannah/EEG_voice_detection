"""Fitting psychometric function for behavioral data
"""
import slab
import pathlib
from os.path import join
import os
import pandas as pd
import pythonpsignifitmaster.psignifit as ps

def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))


data_dir = "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/analysis/data/Neuro2_2023/voc01_behavioral"
all_file_names = [f for f in abs_file_paths(data_dir)]

results=list()
for file_name in all_file_names:
    result = slab.ResultsFile.read_file(str(file_name))
    results.extend(result)

# Get information from the slab result files
behavioral_results=dict()
behavioral_results_2=list()

for i in range(len(results)):
    if results[i]=={'condition_this_trial': 0}:
        condition= results[i-2]['condition_this_trial']
        try:
            response= results[i+1]['response']
            rt= results[i+2]['reaction_time']
        except:
            continue

        behavioral_results[str(i)]={
            "Condition":condition,
            "Response": response,
            "Reaction time": rt}

        # Save as list of tuples
        behavioral_results_2.append((condition, response, rt))


df_behavior= pd.DataFrame.from_dict(behavioral_results)
df_behavior=df_behavior.swapaxes("index", "columns")

# Summarize the data to adequate format for psychometric function fitting
conditions= list(df_behavior["Condition"].unique())
results=dict()
i=1
for condition in conditions:
    df = df_behavior[df_behavior["Condition"] == condition]
    response_count=list(df['Response'].value_counts().values)
    N=sum(response_count)
    response= list(df['Response'].value_counts().index.values)
    if condition != 'original':
       bandwidth= float(condition[-3:])
    else:
        bandwidth=0.0
    results[str(i)] = {"Condition": bandwidth, "Voice responses" :response_count[0], "N": N}
    i=i+1

results_sum_df= pd.DataFrame.from_dict(results)
results_sum_df = results_sum_df.swapaxes("index", "columns")

test= results_sum_df.copy()
data_np=test.to_numpy()
options = dict()  # initialize as an empty dictionary
options['sigmoidName'] = 'norm'  # choose a cumulative Gauss as the sigmoid
options['expType'] = 'YesNo'
result = ps.psignifit(data_np, options)
PSE=result['Fit'][0]
ps.psigniplot.plotPsych(result)
