import numpy as np
import slab

"""Generate a sequence in which element has nearly the same probability to follow each other"""

"""
# Some basic stuff
possible_transitions= n_conditions * n_conditions
total_transitions= n_conditions * n_reps -1
occurence_transitions= total_transitions/possible_transitions # needs to be integer
# choose n_reps so that equal occurence of transitions possible
n_reps=23
while ((n_conditions * n_reps)/(n_conditions * n_conditions)).is_integer() == False:
    n_reps= n_reps+1
"""

# For the behavioral part
n_conditions= 11
n_reps= 21 # needs to be a multiple of n_conditions

ideal_trans=((n_conditions * n_reps)/(n_conditions * n_conditions))

trials = slab.Trialsequence(conditions=n_conditions, n_reps=n_reps)
trans = trials.transitions()
rel_trans=trans / n_reps
while np.any(rel_trans>rel_trans.mean()+ 2*rel_trans.std()):
    trials = slab.Trialsequence(conditions=n_conditions, n_reps=n_reps, kind="random_permutation" )
    trans = trials.transitions()
    rel_trans=trans / n_reps

# For EEG
n_conditions= 5
n_reps= 150 # needs to be a multiple of n_conditions

ideal_trans=((n_conditions * n_reps)/(n_conditions * n_conditions))

trials = slab.Trialsequence(conditions=n_conditions, n_reps=n_reps)
trans = trials.transitions()
rel_trans=trans / n_reps
while np.any(rel_trans>rel_trans.mean()+ 2*rel_trans.std()):
    trials = slab.Trialsequence(conditions=n_conditions, n_reps=n_reps, kind="random_permutation" )
    trans = trials.transitions()
    rel_trans=trans / n_reps

