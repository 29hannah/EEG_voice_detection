""" Check for the correctness of the generated sequences
- Equal occurrence of all elements
- Check for similarity between sequences
- Equal occurrence of transitions
"""

from experiment.trial_sequence import generate_slab_freq
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from difflib import SequenceMatcher

n_conditions= 6 # Including deviant!
n_reps= 54# has to be a multiple of n_conditions

# Generate 500 sequences
sequences=[]
for i in range(500):
    print(i)
    morph_seq = generate_slab_freq(n_conditions=4, n_reps=40)
    sequences.append(morph_seq.trials)

# To check that all elements have the same frequency of occurrence
sum=[]
for sequence in sequences:
    res=[]
    res=Counter(sequence)
    i=1
    results=[]
    for i in range(len(res)):
        i=i+1
        results.append(res[i])
    sum.append(results)
for element in sum:
    plt.plot(element)

# Check how similar the sequences are

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
results=[]
for i in range(len(sequences)-1):
    seq_1=sequences[i]
    seq_2=sequences[i+1]
    res=similar(str(seq_1), str(seq_2))
    results.append(res)
plt.plot(results)



# Double check for correctness of transitions
trans=[]
ideal_trans = ((n_conditions * n_reps) / (n_conditions * n_conditions))
for i in range(500):
    print(i)
    trans.append(np.sum( morph_seq.transitions() != ideal_trans))
plt.plot(trans)

