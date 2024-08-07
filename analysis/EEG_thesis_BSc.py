import json
import pandas as pd
import pathlib
import os
import seaborn as sns
import pythonpsignifitmaster.psignifit as ps
from mne.channels import make_1020_channel_selections
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from mpl_toolkits.axes_grid1 import make_axes_locatable
import mne
from mne.channels import find_ch_adjacency
from mne.stats import  spatio_temporal_cluster_test
from mne.viz import plot_compare_evokeds


# TODO check validity of used approach for clustering
# TODO clusters and channel selection
# TODO plot individual psychometric functions
# Select channels manually: ch indx to name?


# Function to fit psychometric function
def fit_pf(data):
    data_np = data.to_numpy()
    # Define how to fit psychometric function
    options = dict()  # initialize as an empty dictionary
    options['sigmoidName'] = 'logistic'  # choose a cumulative Gauss as the sigmoid
    options['expType'] = 'equalAsymptote'
    plt.figure()
    result = ps.psignifit(data_np, options)
    PSE = result['Fit'][0]

    ps.psigniplot.plotPsych(result, plotThresh=False, extrapolLength=.01)
    return PSE

def ignore_conds(d, *keys):
    return dict(filter(lambda key_value: key_value[0] not in keys, d.items()))


# Set directories
DIR = pathlib.Path(os.getcwd())
behavior_results_DIR = DIR / "analysis" / "results" /"study"/ "behavior"
EEG_DIR= DIR / "analysis" / "results" /"study"/ "EEG"
with open(DIR / "analysis" / "settings" / "preproc_config.json") as file:
    cfg = json.load(file)

subjs=['sub_08', 'sub_09', 'sub_10', 'sub_11', 'sub_07', 'sub_12','sub_13', 'sub_14', 'sub_15', 'sub_16', 'sub_18',
       'sub_19','sub_20', 'sub_21', 'sub_22', 'sub_23', 'sub_24', 'sub_25', 'sub_26', 'sub_27']

# Plot the behavioural data/ Fit the psychometric function
appended_data = []
for subj in subjs:
    data = pd.read_csv(str(behavior_results_DIR) +'/'+ subj + '_summarized-behavior.csv')
    appended_data.append(data)

df_behav = pd.concat(appended_data)


# Behavioural data
# Fit the Psychometric Function and get the PSE
results_PSE=[]
for subj in subjs:
    df_sub= df_behav[df_behav['subj']==subj]
    data = df_sub.copy()
    data = data[['Morph ratio', 'Voice responses', 'N']]
    # Save PSE per subject
    PSE=fit_pf(data)
    results_PSE.append((subj,PSE))

PSE_df = pd.DataFrame(results_PSE, columns=['subj', 'PSE'])


# Plot psychometric function over subjects & distribution of PSE
data = df_behav.copy()
data = data[['Morph ratio', 'Voice responses', 'N']]
data_np = data.to_numpy()
options = dict()  # initialize as an empty dictionary
options['sigmoidName'] = 'logistic'  # choose a cumulative Gauss as the sigmoid
options['expType'] = 'equalAsymptote'
result = ps.psignifit(data_np, options)

fig, axs = plt.subplots(2,sharex= True, gridspec_kw={'height_ratios': [2, 1]})
ps.psigniplot.plotPsych(result,
                        dataColor="blue",
                        lineColor="blue",
                        xLabel="%Voice Responses",
                        yLabel="Morph Ratio",
                        plotThresh=False,
                        plotAsymptote=False,
                        aspectRatio=False,
                        extrapolLength=.0,
                        axisHandle= axs[0])

sns.histplot(data=PSE_df, x="PSE", binwidth=0.1, ax=axs[1])


# EEG data
# Read in the data
evokeds, evokeds_avrgd = cfg["epochs"][f"event_id"].copy(
    ), cfg["epochs"][f"event_id"].copy()
for key in cfg["epochs"][f"event_id"]:
        evokeds[key], evokeds_avrgd[key] = list(), list()

for subj in subjs:
    evokeds_folder = str(EEG_DIR) +"/" + subj +  "/evokeds"
    evoked = mne.read_evokeds(evokeds_folder +"/" + subj  + '-ave.fif')
    for condition in evoked:
        if condition.comment in evokeds:
            evokeds[condition.comment].append(condition.crop(-0.2, 0.5))
            if len(evokeds[condition.comment]) == len(subjs):
                evokeds_avrgd[condition.comment] = mne.grand_average(
                    evokeds[condition.comment])
            else:
                continue

# Plot the butterfly plot
combined_evokeds = mne.combine_evoked([evokeds_avrgd["morph/0.0"], evokeds_avrgd["morph/0.4"],
                                             evokeds_avrgd["morph/0.6"], evokeds_avrgd["morph/1.0"]],
                                       weights=[0.25, 0.25, 0.25, 0.25])
combined_evokeds.plot_joint()

# Get compared gfp
mne.viz.plot_compare_evokeds(ignore_conds(
    evokeds_avrgd, "deviant"), combine='gfp')

## Permutation cluster test

"""
# Evokeds per subject/ one subject = one observation
conditions = ['morph/0.0', 'morph/0.4','morph/0.6','morph/1.0']
X_total= []
for condition in conditions:
    condition_idx=conditions.index(condition)
    X_evoked=[]
    for ele in enumerate(subjs):
        subj_idx= ele[0]
        evoked_sub= evokeds[condition][subj_idx].get_data().transpose()
        X_evoked.append(evoked_sub)
    X_total.append(np.stack( X_evoked, axis=0))
"""

# All epochs, all subjects
# Get data of all epochs for one condition in one numpy array
for subj in subjs:
    print(subj)
    epochs_folder = EEG_DIR / subj / "epochs"
    epochs = mne.read_epochs(epochs_folder / pathlib.Path(subj + '-epo.fif'))
    conditions = list(epochs.event_id.keys())[1:5]
    epochs.equalize_event_counts(conditions)
    event_ids = [1,2,3,  4]
    indices = [np.where(epochs.events[:, 2] == event_id)[0] for event_id in event_ids]
    if subj=="sub_08": # = first subject
        X_total = [epochs.get_data()[idx, :, :].transpose(0, 2, 1) for idx in indices]
    else:
        X = [epochs.get_data()[idx, :, :].transpose(0, 2, 1) for idx in indices]
        for event_id in event_ids:
            X_total[event_id-1]= np.concatenate((X_total[event_id-1], X[event_id-1]))


"""
result= dict()
for subj in subjs:
    print(subj)
    epochs_folder = EEG_DIR / subj / "epochs"
    epochs = mne.read_epochs(epochs_folder / pathlib.Path(subj + '-epo.fif'))
    conditions = list(epochs.event_id.keys())[1:5]
    epochs.equalize_event_counts(conditions)
    event_ids = [1, 4]
    indices = [np.where(epochs.events[:, 2] == event_id)[0] for event_id in event_ids]
    X_total = [epochs.get_data()[idx, :, :].transpose(0, 2, 1) for idx in indices]
    # Spatiotemporal permutation cluster test/ mne example: descriptive and not statistically meaningful
    adjacency, ch_names = find_ch_adjacency(epochs.info, ch_type="eeg")
    #mne.viz.plot_ch_adjacency(epochs.info, adjacency, ch_names)
    # Calculate statistical thresholds
    F_obs, clusters, p_values, h0 = permutation_cluster_test(
        X_total,
        adjacency=adjacency,
        n_permutations=100,
        stat_fun=mne.stats.f_oneway
        )

    result[subj]= {
            "f": F_obs,
            "clusters": clusters,
            "p": p_values,
            "fs": epochs.info["sfreq"],
            "t": epochs.times,
        }


results_over_subjects= []
for subj in subjs:
    p_values= result[subj]["p"]
    F_obs= result[subj]["f"]
    clusters= result[subj]["clusters"]

    p_accept = 0.05
    good_cluster_inds = np.where(p_values < p_accept)[0]
    if len(good_cluster_inds)!=0:
        for i_clu, clu_idx in enumerate(good_cluster_inds):
            # unpack cluster information, get unique indices
            time_inds, space_inds = np.squeeze(clusters[clu_idx])
            ch_inds = np.unique(space_inds)
            time_inds = np.unique(time_inds)

            sig_times = epochs.times[time_inds]
            tmin= min(sig_times)
            tmax = max(sig_times)
            results_over_subjects.append((subj, sig_times, tmin, tmax, ch_inds))

df = pd.DataFrame(results_over_subjects, columns =['subj', 'sig_times', 'tmin', 'tmax', 'ch_inds'])
"""

# Based on https://mne.tools/dev/auto_tutorials/stats-sensor-space/75_cluster_ftest_spatiotemporal.html
adjacency, ch_names = find_ch_adjacency(epochs.info, ch_type="eeg")

tail = 1

alpha_cluster_forming = 0.05
n_conditions = len(event_ids)
n_observations = len(X_total[0])
dfn = n_conditions - 1
dfd = n_observations - n_conditions

# Note: we calculate 1 - alpha_cluster_forming to get the critical value
# on the right tail
f_thresh = scipy.stats.f.ppf(1 - alpha_cluster_forming, dfn=dfn, dfd=dfd)

cluster_stats = spatio_temporal_cluster_test(
    X_total,
    n_permutations=1000,
    tail=tail,
    n_jobs=None,
    buffer_size=None,
    adjacency=adjacency,
)

F_obs, clusters, p_values, _ = cluster_stats

# Subselect clusters
p_accept = 0.05
good_cluster_inds = np.where(p_values < p_accept)[0]
print(len(good_cluster_inds))

ch_inds_all= np.arange(0, 65, 1, dtype=int)


# loop over clusters
for i_clu, clu_idx in enumerate(good_cluster_inds):
    # unpack cluster information, get unique indices
    time_inds, space_inds = np.squeeze(clusters[clu_idx])
    ch_inds = np.unique(space_inds)
    time_inds = np.unique(time_inds)
    # get topography for F stat
    f_map = F_obs[time_inds, ...].mean(axis=0)
    # get signals at the sensors contributing to the cluster
    sig_times = epochs.times[time_inds]
    # create spatial mask
    mask = np.zeros((f_map.shape[0], 1), dtype=bool)
    #mask[ch_inds, :] = True
    # manually
    ch_inds_sub= np.array([13,52])
    mask[ch_inds_sub, :] = True

    # initialize figure
    fig, ax_topo = plt.subplots(1, 1, figsize=(10, 3), layout="constrained")

    # plot average test statistic and mark significant sensors
    f_evoked = mne.EvokedArray(f_map[:, np.newaxis], epochs.info, tmin=0)
    f_evoked.plot_topomap(
        times=0,
        axes=ax_topo,
        mask=mask,
        cmap="Reds",
        vlim=(np.min, np.max),
        show=False,
        colorbar=False,
        mask_params=dict(markersize=10),
    )
    image = ax_topo.images[0]
    # remove the title that would otherwise say "0.000 s"
    ax_topo.set_title("")
    # create additional axes (for ERF and colorbar)
    divider = make_axes_locatable(ax_topo)
    # add axes for colorbar
    ax_colorbar = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(image, cax=ax_colorbar)
    ax_topo.set_xlabel(
        "Averaged F-map ({:0.3f} - {:0.3f} s)".format(*sig_times[[0, -1]])
    )
    # add new axis for time courses and plot time courses
    ax_signals = divider.append_axes("right", size="300%", pad=1.2)
    title = f"Cluster #{i_clu + 1}, {len(ch_inds)} sensor"
    if len(ch_inds) > 1:
        title += "s (mean)"
    plot_compare_evokeds(
        ignore_conds(
            evokeds_avrgd, "deviant"),
        title=title,
        picks=ch_inds,
        axes=ax_signals,
        show=False,
        split_legend=True,
        truncate_yaxis="auto",
    )
    # plot temporal cluster extent
    ymin, ymax = ax_signals.get_ylim()
    ax_signals.fill_betweenx(
        (ymin, ymax), sig_times[0], sig_times[-1], color="orange", alpha=0.3

    )

    # Plot image plot
    significant_points = np.zeros((351, 65), dtype=bool)
    significant_points[time_inds, :] = True
    significant_points[ ch_inds_all[ch_inds[np.searchsorted(ch_inds, ch_inds_all)] != ch_inds_all], :] = False
    significant_points=np.swapaxes(significant_points, 0, 1)

    selections = make_1020_channel_selections(combined_evokeds.info, midline="12z")
    fig, axes = plt.subplots(nrows=3, figsize=(8, 8))
    axes = {sel: ax for sel, ax in zip(selections, axes.ravel())}
    time_unit = dict(time_unit="s")
    combined_evokeds.plot_image(
        axes=axes,
        group_by=selections,
        colorbar=False,
        show=False,
        mask=significant_points,
        show_names="all",
        titles=None,
        **time_unit,
    )
    plt.colorbar(axes["Left"].images[-1], ax=list(axes.values()), shrink=0.3, label="µV")

plt.show()



# Get amplitude measurements per subject
tmin = 0.122
tmax = 0.448
channels=['Cz', 'CPz']
results=[]
for subj_idx in enumerate(subjs):
    for condition in conditions:
        evok= evokeds[condition][subj_idx[0]]
        ROI= mne.pick_channels(evok.info["ch_names"], include=channels)
        roi_dict = dict(left_ROI=ROI)
        roi_evoked = mne.channels.combine_channels(evok, roi_dict, method="mean")
        amp = roi_evoked.crop(tmin=tmin, tmax=tmax).data.mean(axis=1) * 1e6

        voice_responses=  df_behav.loc[(df_behav['subj'] ==subj_idx[1]) & (df_behav['Morph ratio'] ==float(condition[-3:]))].iloc[0]['%Voice']

        result= (subj_idx[1],float(condition[-3:]), amp[0], voice_responses)
        results.append(result)

df = pd.DataFrame(results, columns=['subj', 'condition','amp', '%Voice'])
sns.scatterplot(data=df, x="amp", y="%Voice", hue='subj', legend= False)
sns.lmplot(x="condition", y="amp", data=df, y_jitter=.03)
df.to_csv("/Users/hannahsmacbook/EEG_voice/EEG_data.csv")
