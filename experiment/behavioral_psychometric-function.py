import slab
import pathlib
from os.path import join
import os
import pandas as pd
import EEG_voice_detection.pythonpsignifitmaster.psignifit as ps
import matplotlib.pyplot as plt
import seaborn as sns

participant_id= 'test_220_2'

def abs_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if not f.startswith('.'):
                yield pathlib.Path(join(dirpath, f))


data_dir = "C:\\projects\\EEG_voice_detection\\experiment\\results\\behavior\\" + participant_id
all_file_names = [f for f in abs_file_paths(data_dir)]

'''
# Get information from the slab result files
results=list()
for file_name in all_file_names:
    if slab.ResultsFile.read_file(str(file_name), tag='stage')== 'experiment':
        result= slab.ResultsFile.read_file(str(file_name))
        results.extend(result)

behavioral_results=dict()
morph_ratios=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
for i in range(len(results)):
    if 'solution' in results[i]:
        solution= results[i]['solution']
        try:
            response= results[i+1]['response']
            rt= results[i+3]['reaction_time']
        except:
            continue
        behavioral_results[str(i)]={
            "Condition":solution,
            "Morph ratio": morph_ratios[solution-1] ,
            "Response": response,
            "Reaction time": rt}
df_behavior= pd.DataFrame.from_dict(behavioral_results)
df_behavior=df_behavior.swapaxes("index", "columns")
'''
participant_results=list()
for file in all_file_names:
    data = pd.read_csv(file)
    participant_results.append(data)
df_behavior=pd.concat(participant_results)

# Summarize the data to adequate format for psychometric function fitting
conditions= list(df_behavior["Morph played"].unique())
results=dict()
i=1
for condition in conditions:
    df = df_behavior[df_behavior["Morph played"] == condition]
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
    results[str(i)] = {"Condition": condition, "Morph ratio": morph,  "Voice responses":yes, "N": sum(response_count)}
    i=i+1
results_sum_df= pd.DataFrame.from_dict(results)
results_sum_df = results_sum_df.swapaxes("index", "columns")



sns.lineplot(data=df_behavior, x=df_behavior['Morph ratio'], y=df_behavior['Reaction time'], err_style='bars',
             errorbar=('se',2))
plt.savefig("C:\\projects\\EEG_voice_detection\\experiment\\results\\behavior\\plots\\rt_" + participant_id )
plt.close()


data= results_sum_df.copy()
data= data[['Morph ratio', 'Voice responses', 'N']]
data_np=data.to_numpy()
options = dict()  # initialize as an empty dictionary
options['sigmoidName'] = 'logistic'  # choose a cumulative Gauss as the sigmoid
options['expType'] = 'equalAsymptote'
result = ps.psignifit(data_np, options)
PSE=result['Fit'][0]
ps.psigniplot.plotPsych(result, extrapolLength= 0.01)
plt.savefig("C:\\projects\\EEG_voice_detection\\experiment\\results\\behavior\\plots\\pf_plot" + participant_id )
plt.close()

