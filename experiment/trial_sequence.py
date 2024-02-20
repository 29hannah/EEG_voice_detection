"""Generate a sequence in which each element has (almost always) the same probability to follow one another (excluding deviant sound
Marker for deviant is n_conditions+1 = highest condition number
"""
import numpy as np
import slab
import random
import itertools


# Generating the sequence
def generate_sequence(n_conditions, n_reps):
    elements = list(np.arange(1, n_conditions + 1))
    list_start = elements * n_reps
    list_start = list_start
    sequence= []
    pick = random.choice(elements)
    # Make sure that sequence does not start with deviant
    if pick==0:
        pick = random.choice(elements)
    sequence = sequence + [pick]
    pick= random.choice(elements)
    list_start.remove(pick)
    sequence = sequence + [pick]
    pick = random.choice(elements)
    list_start.remove(pick)
    sequence = sequence + [pick]
    while len(sequence)<= n_conditions*n_reps:
        # Check for transitions
        trans_dict = dict()
        combinations = list(itertools.product(list(elements), list(elements)))
        for combination in combinations:
            trans_dict[str(combination[0]) + ',' + str(combination[1])] = 0
        i = 0
        while i < len(sequence)-1:
            trans= str(sequence[i])+','+str(sequence[i+1])
            trans_dict[trans]=trans_dict[trans]+1
            i= i+1
        # Get the smallest transition values
        minval = min(trans_dict.values())
        res_min = [k for k, v in trans_dict.items() if v==minval]
        options_to_choose_from=list()
        for element in res_min:
            if element.split(',')[0] == str(sequence[-1]):
                if int(element.split(',')[1]) in list_start:
                    options_to_choose_from.append(int(element.split(',')[1]))
        if len(options_to_choose_from)==0:
            pick= random.choice(list_start)
            list_start.remove(pick)
            sequence = sequence + [pick]
        else:
            # Choose and delete element from list
            pick=random.choice(options_to_choose_from)
            list_start.remove(pick)
            sequence = sequence + [pick]
    return sequence, trans_dict

def generate_opt_seq(n_conditions, n_reps):
    ideal_trans = ((n_conditions * n_reps) / (n_conditions * n_conditions))
    eval=[1, 2]
    while len(eval)>1:
        sequence, trans_dict = generate_sequence(n_conditions, n_reps)
        trans_values=list(trans_dict.values())
        eval=list()
        for element in trans_values:
            if element!=ideal_trans:
                eval.append(ideal_trans-element)
    return sequence


def generate_slab_freq(n_conditions, n_reps):
    conditions = list(np.arange(1, n_conditions + 1))
    ideal_trans = ((n_conditions * n_reps) / (n_conditions * n_conditions))
    morph_seq = slab.Trialsequence(conditions=conditions, trials=generate_opt_seq(n_conditions, n_reps),
                                   n_reps=n_reps, deviant_freq=0)
    while np.sum(morph_seq.transitions() != ideal_trans):
        morph_seq = slab.Trialsequence(conditions=conditions,
                                       trials=generate_opt_seq(n_conditions, n_reps),
                                       n_reps=n_reps, deviant_freq=0)
    return morph_seq