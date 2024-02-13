"""Fitting psychometric function for behavioral data (local machine)
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


test= results_sum_df.copy()
data_np=test.to_numpy()
options = dict()  # initialize as an empty dictionary
options['sigmoidName'] = 'norm'  # choose a cumulative Gauss as the sigmoid
options['expType'] = 'YesNo'
result = ps.psignifit(data_np, options)
PSE=result['Fit'][0]
ps.psigniplot.plotPsych(result)
