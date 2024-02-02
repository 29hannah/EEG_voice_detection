import os
import pathlib
import json
import os
import json
import pathlib
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import slab
import pathlib
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import mne





#Read in epochs and evokeds
    # retrieves epochs and evokeds for one subject
DIR = pathlib.Path(os.getcwd())
sub_DIR = DIR / "analysis" / "data" /"Neuro2_2023"/ "EEG"
with open(DIR / "analysis"  / "settings" / "preproc_config.json") as file:
    cfg = json.load(file)


evokeds = cfg["epochs"][f"event_id_test"].copy()
for key in cfg["epochs"][f"event_id_test"]:
    evokeds[key] = list()


# Read in the evokeds for one subject
evokeds_folder = sub_DIR / "voc01" / "evokeds"
evoked = mne.read_evokeds(evokeds_folder / pathlib.Path('voc01-ave.fif'))



"""
evokeds, evokeds_avrgd, evokeds_data = cfg["epochs"][f"event_id_vocal_effort"].copy(
    ), cfg["epochs"][f"event_id_vocal_effort"].copy(), cfg["epochs"][f"event_id_vocal_effort"].copy()
for key in cfg["epochs"][f"event_id_vocal_effort"]:
        evokeds[key], evokeds_avrgd[key], evokeds_data[key] = list(), list(), list()
        # get evokeds for every condition and subject.

        for condition in evoked:
            if condition.comment in evokeds:
                evokeds[condition.comment].append(condition.crop(-0.2, 0.6))
                if len(evokeds[condition.comment]) == 1:
                    evokeds_avrgd[condition.comment] = mne.grand_average(
                        evokeds[condition.comment])
                else:
                    continue

"""


# Plot the results for one subject
combined_evokeds= mne.combine_evoked([evoked[0], evoked[1],
                                         evoked[2], evoked[3],
                                         evoked[4]], weights=[0.2, 0.2, 0.2, 0.2, 0.2])

combined_evokeds.plot_topomap()
combined_evokeds.plot_joint()
mne.viz.plot_compare_evokeds(evoked)