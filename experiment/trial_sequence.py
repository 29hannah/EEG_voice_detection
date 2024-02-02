import numpy as np
import random
import csv
import slab

"""Generate a sequence in which element has nearly the same probability to follow each other"""

import numpy
import slab

n_conditions= 11
n_reps= 25

#trans= (n_reps* n_conditions-1)/(n_conditions*n_conditions)+2
trans= 10
while numpy.any(trans>5):
    trials = slab.Trialsequence(conditions=n_conditions, n_reps=n_reps, kind="random_permutation")
    trans = trials.transitions()
    while numpy.any(trans <2):
        trials = slab.Trialsequence(conditions=n_conditions, n_reps=n_reps, kind="random_permutation")
        trans = trials.transitions()









# Check for transitions using modified slab code

i = 0
print("Still looking for sequence")
while i == 0:
    randomized_sequence = start_sequence.copy()
    random.shuffle(randomized_sequence)
    randomized_sequence.insert(0, 1)
    # Check for transitions using modified slab code
    transitions = np.zeros((len(elements), len(elements)))
    for i, j in zip(randomized_sequence, randomized_sequence[1:]):
        transitions[i - 1, j - 1] += 1
        rel_transitions = transitions / n_repetitions
        threshold = 1 / n_elements
        if np.all(rel_transitions) ==threshold:
                print(randomized_sequence)
                i = 1
                results_sequences.append(randomized_sequence)
                results_transitions.append(rel_transitions)
        else:
            #print("Transitions not evenly distributed")
            i = 0






j=0
while len(results_sequences)<n_sequences:
    i = 0
    print("Still looking for sequence")
    while i == 0:
        randomized_sequence = start_sequence.copy()
        random.shuffle(randomized_sequence)
        randomized_sequence.insert(0, 1)
        # Check for transitions using modified slab code
        transitions = np.zeros((len(elements), len(elements)))
        for i, j in zip(randomized_sequence, randomized_sequence[1:]):
            transitions[i - 1, j - 1] += 1

        """
        #Use absolute values to assess the quality of sequence
       abs_threshold = n_repetitions / len(elements) # How often ideally transiion
       limit =  abs_threshold*0.2   #Should be relative to length of elements
       if np.all((transitions < abs_threshold + limit) & (transitions > abs_threshold - limit)) == True:
        """
        rel_transitions = transitions / n_repetitions
        threshold = 1 / n_elements  # How often ideally transiion
        limit = threshold * 0.2  # Should be relative to length of elements
        if np.all((rel_transitions < threshold + limit) & (rel_transitions > threshold - limit)) == True:
            if runcrit_check([j - i for i, j in zip(randomized_sequence[:-1], randomized_sequence[1:])])<=runcrit:
                print(randomized_sequence)
                i = 1
                results_sequences.append(randomized_sequence)
                results_transitions.append(rel_transitions)
        elif np.all((rel_transitions < threshold + limit) & (rel_transitions > threshold - limit)) == False:
            #print("Transitions not evenly distributed")
            i = 0

# Write resultings sequences to csv file
with open(sequences_name + ".csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(results_sequences)




# Define function to check for runcrit
def runcrit_check(list_input):
    count = 0
    prev = 0
    indexend = 0
    for i in range(0,len(list_input)):
        if list_input[i] == 1:
            count += 1
        else:
            if count > prev:
                prev = count
            count = 0
    return(prev)
