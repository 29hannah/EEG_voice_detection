from experiment.trial_sequence import generate_slab_freq
import random
import math
from collections import Counter

n_conditions=11 # for EEG experiment 4; for behavioural part 11
n_reps= 11# for EEG experiment 40; for behavioural part 11

morph_ratios = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11]
continua_opt=['A', 'B', 'C']

balance_continua_dict= {}
for morph_ratio in morph_ratios:
    continua= continua_opt * math.ceil(n_conditions * n_reps/ len(continua_opt)/n_conditions)
    random.shuffle(continua)
    continua.append(random.choice(continua_opt))
    balance_continua_dict[morph_ratio]=continua

conditions= []
morph_seq = generate_slab_freq(n_conditions=n_conditions, n_reps=n_reps)
for morph in morph_seq:
    continuum= balance_continua_dict[morph][0]
    conditions.append(str(morph) + ',' + continuum)
    del balance_continua_dict[morph][0]


Counter(conditions)
