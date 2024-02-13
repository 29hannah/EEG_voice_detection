import os
import pathlib
from os.path import join
import slab
import pandas as pd


def summarize_data(id, data_DIR, out_DIR_raw, out_DIR_sum):
    data_dir= data_DIR+id


    def abs_file_paths(directory):
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                if not f.startswith('.'):
                    yield pathlib.Path(join(dirpath, f))


    all_file_names = [f for f in abs_file_paths(data_dir)]

    # Get information from the slab result files
    results = list()
    for file_name in all_file_names:
        if slab.ResultsFile.read_file(str(file_name), tag='stage') == 'experiment':
            result = slab.ResultsFile.read_file(str(file_name))
            results.extend(result)
    behavioral_results = dict()
    morph_ratios = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for i in range(len(results)):
        if 'solution' in results[i]:
            solution = results[i]['solution']
            try:
                response = results[i + 1]['response']
                rt = results[i + 3]['reaction_time']
            except:
                continue
            behavioral_results[str(i)] = {
                "Condition": solution,
                "Id": id,
                "Morph ratio": morph_ratios[solution - 1],
                "Response": response,
                "Reaction time": rt}
    df_behavior = pd.DataFrame.from_dict(behavioral_results)
    df_behavior = df_behavior.swapaxes("index", "columns")

    df_behavior.to_csv(out_DIR_raw + '/' + id + '_raw-data.csv')

    # Summarize the data to adequate format for psychometric function fitting
    conditions = list(df_behavior["Condition"].unique())
    results = dict()
    i = 1
    for condition in conditions:
        df = df_behavior[df_behavior["Condition"] == condition]
        morph = df['Morph ratio'].iloc[0]
        response_count = list(df['Response'].value_counts().values)
        responses = list(df['Response'].value_counts().index.values)
        if len(response_count) != 1:
            no = response_count[responses.index(2.0)]
            yes = response_count[responses.index(1.0)]
        elif 2.0 not in responses:
            no = 0
            yes = response_count[responses.index(1.0)]
        elif 2.0 not in responses:
            no = response_count[responses.index(2.0)]
            yes = 0

        results[str(i)] = {"Condition": condition, "Id": id, "Morph ratio": morph, "Voice responses": yes,
                           "N": sum(response_count), "%Voice": yes/sum(response_count)}
        i = i + 1
    results_sum_df = pd.DataFrame.from_dict(results)
    results_sum_df = results_sum_df.swapaxes("index", "columns")

    results_sum_df.to_csv(out_DIR_sum + '/' + id + '_summarized-data.csv')


