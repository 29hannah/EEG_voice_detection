"""Script to analyze the behavioral data collected before and during the EEG experiment
->Evaluate behavioral discriminability between morph ratios presented"""

from os import listdir
import pandas as pd
from scipy.stats import fisher_exact
import numpy as np

# Comparing sets of binary behavioral data (AFC procedure)

# Read in the behavioral data separtely for each participant
DIR = "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/analysis"
data_DIR= DIR+ '/data/pilot/'
results_DIR= DIR + "/results/pilot/"
out_DIR_sum=  results_DIR +"sum"

files_sum = [file for file in listdir(out_DIR_sum) if file.endswith('.csv')]

data = pd.read_csv(out_DIR_sum + '/' + files_sum[0])
morph_ratios = list(data["Morph ratio"].unique())
morph_ratios.sort()


discrim_results= []
for file in files_sum:
    i = 0
    while i<len(morph_ratios)-1:
        data = pd.read_csv(out_DIR_sum + '/' + file)
        morph_ratio_1= morph_ratios[i]
        morph_ratio_2=morph_ratios[i+1]

        # Create numpy array
        a = np.array([[data[data["Morph ratio"] == morph_ratio_1].iloc[0]['Voice responses'],
                    data[data["Morph ratio"] == morph_ratio_1].iloc[0]['N']-data[data["Morph ratio"] == morph_ratio_1].iloc[0]['Voice responses']],
                    [data[data["Morph ratio"] == morph_ratio_2].iloc[0]['Voice responses'],
                    data[data["Morph ratio"] == morph_ratio_2].iloc[0]['N']-data[data["Morph ratio"] == morph_ratio_2].iloc[0]['Voice responses']]])
        odds_ratio, p_value = fisher_exact(a)
        # Save the result
        discrim_result=(data["Id"].iloc[0], morph_ratio_1, morph_ratio_2, odds_ratio, p_value)
        discrim_results.append(discrim_result)
        i=i+1

# List with results tuples to df
df = pd.DataFrame(data, columns =['Id', 'Morph ratio 1', 'Morph ratio 2', 'Odds ratio', 'p value'])
df.to_csv(results_DIR + '/behavioral_discriminability')