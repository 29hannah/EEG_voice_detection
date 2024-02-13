"""Code to analyze the behavioral data collected
-> Select the stimuli for the EEG experiment based on behavioral pilot data
-> effect scaling of behavioral data per participant
"""
import os
from analysis.behavioral_summarize_data import summarize_data
from os import listdir
import pandas as pd
import seaborn as sns

DIR = "/Users/hannahsmacbook/PycharmProjects/EEG_voice_detection/analysis"
data_DIR= DIR+ '/data/pilot/'
results_DIR= DIR + "/results/pilot/"
out_DIR_raw= results_DIR +"raw"
out_DIR_sum=  results_DIR +"sum"

dirs= [results_DIR, out_DIR_raw, out_DIR_sum]
for dir in dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("path did not exist, path created")

ids = list(name for name in os.listdir(data_DIR)
           if os.path.isdir(os.path.join(data_DIR, name)))

# Only necessary when runnig the analysis for the first time/making changes to the code summarizing the data
for id in ids:
    summarize_data(id, data_DIR, out_DIR_raw, out_DIR_sum)

# Read in the summarized files per participant and append data frames
files_raw = [file for file in listdir(out_DIR_sum) if file.endswith('.csv')]
appended_data = []
for file in files_raw:
    data = pd.read_csv(out_DIR_sum + '/' + file)
    appended_data.append(data)
results = pd.concat(appended_data)



# Get the data for the final stimuli
# Boxplot
sns.boxplot(results, x= results["Morph ratio"], y=results["%Voice"])

# Calculate stdev over participants: Subset to morph ratio, calculate sted over participants % Voice
morph_ratios = list(results["Morph ratio"].unique())

stdev_results= dict()jj
for morph_ratio in morph_ratios:
    df = results[results["Morph ratio"] == morph_ratio]
    stdev_results[str(morph_ratio)]={"stdev %voice": df['%Voice'].std()}

