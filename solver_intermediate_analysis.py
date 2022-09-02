import numpy as np
import itertools
import matplotlib.pyplot as plt
from time import time
import pickle

colours = ['1','2','3','4']
all_combs = np.array([list(feat_vec) for feat_vec in itertools.product(colours, repeat = 4)])

def list_possible_combs(cond, select_from = all_combs):
    combs = []
    for feat_vec in select_from:
        if np.sum(feat_vec == cond[0]) == cond[1]:
            combs.append(feat_vec)
    return np.array(combs)

def get_bits(p):
    # returns 0 if p = 0
    if p == 0:
        return 0
    else:
        return -np.log2(p)

def reveal(feat_vec, true_feat_vec):
    return np.sum(feat_vec == true_feat_vec)


guess_counts = []
# simulate
for true_feat_vec in all_combs:

    start = time()
    # initialise possible combs
    possible_combs = all_combs
    
    # initialise first guess
    guess_feat_vec = ['1', '1', '1', '1']
    guess_res = reveal(feat_vec = guess_feat_vec, true_feat_vec = true_feat_vec)
    guess_count = 1

    while (guess_res != 4) and (guess_count < 20): # force stop after 20 guesses
        cond = (guess_feat_vec, guess_res)

        possible_combs = list_possible_combs(cond = cond, select_from = possible_combs)

        # initialise expected bits and probabilities of being right lists
        exp_bits_for_each_comb = []
        right_probs_for_each_comb = []

        # go through every possible combination
        for try_comb in all_combs:
            probs_for_each_event = []
            bits_for_each_event = []

            # for each possible event (no features right, one feature right, ..., five features right)
            for i in range(5):
                if len(possible_combs) == 0: # do better
                    p = 0
                else:
                    p = len(list_possible_combs(cond = (try_comb, i), select_from = possible_combs)) / len(possible_combs)
                probs_for_each_event.append(p)
                bits_for_each_event.append(get_bits(p))
            
            # compute expected bits
            exp_bits = np.sum(np.array(probs_for_each_event) * np.array(bits_for_each_event))
            exp_bits_for_each_comb.append(exp_bits)

            # compute probability of being right
            if len(possible_combs) == 0:
                right_prob = 0
            else:
                right_prob = (try_comb.tolist() in possible_combs.tolist()) / len(possible_combs) # do better that this
            right_probs_for_each_comb.append(right_prob)

            # print(f"The combination {try_comb} gives {exp_bits} expected bits and is {100 * right_prob}% correct.")

        # 
        right_probs_for_each_comb = np.array(right_probs_for_each_comb)
        right_probs_for_each_comb_desc_idx = (-right_probs_for_each_comb).argsort()

        # get combinations which provide maximal bits
        max_bits_combs_idx = np.where(exp_bits_for_each_comb == np.max(exp_bits_for_each_comb))
        max_bits_combs = all_combs[max_bits_combs_idx]

        # from the list of combinations which provide maximal bits, choose the one with the highest probability of being right
        max_bits_max_right_prob_combs_idx = np.argmax(right_probs_for_each_comb[max_bits_combs_idx])
        guess_feat_vec = max_bits_combs[max_bits_max_right_prob_combs_idx]
        guess_res = reveal(feat_vec = guess_feat_vec, true_feat_vec = true_feat_vec)

        guess_count += 1

        # print(f"Guessed '{' '.join(guess_feat_vec)}', which provides {np.max(exp_bits_for_each_comb)} expected bits and is {100*np.max(right_probs_for_each_comb[max_bits_combs_idx])}% right.")
        # print(f"Guess result: {guess_res}")
    stop = time()
    print(f"{stop-start}s elapsed.")
    
    guess_counts.append(guess_count)
print(guess_counts)

with open("solver_intermediate_guess_counts1.pickle", "wb") as handle:
    pickle.dump(guess_counts, handle)

bins = np.arange(0, np.max(guess_counts) + 1.5) - 0.5
fig, ax = plt.subplots()
ax.hist(guess_counts, bins)
ax.set_xticks(bins + 0.5)
plt.savefig("solver_intermediate_guess_count_graph1.jpg")
plt.show()