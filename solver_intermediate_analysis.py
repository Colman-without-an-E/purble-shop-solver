import numpy as np
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import pickle
from time import time
plt.rcParams.update({'font.size': 16})

# return number of right colour right features
def reveal(feat_vec, true_feat_vec):
    return np.count_nonzero(feat_vec == true_feat_vec)

colours = ['1','2','3','4']
all_combs = np.array([list(feat_vec) for feat_vec in itertools.product(colours, repeat = 4)])

# create right colour right feature score matrix
X = np.array([all_combs for i in range(4**4)])
Y = np.transpose(X, axes = (1,0,2))
RCRF = np.count_nonzero(X == Y, axis=2)
# plt.imshow(RCRF)
# plt.savefig(r"Purble-Shop-Solver/data_and_graphs/feat_score_heatmap_intermediate.png")
# plt.show()

guess_counts = []
for m, true_feat_vec in enumerate(all_combs):

    # initialise possible feature combinations
    possible_combs_idx = np.arange(len(all_combs))

    # initalise first guess
    guess_feat_vec_idx = 0
    guess_feat_vec = all_combs[guess_feat_vec_idx]
    guess_res = reveal(guess_feat_vec, true_feat_vec)
    guess_count = 1

    # guess until correct
    while (guess_res != 4) and (guess_count < 10): # force stop after 10 guesses

        # update possible feature combinations
        possible_combs_idx = np.intersect1d(
            np.where(RCRF[guess_feat_vec_idx] == guess_res)[0], 
            possible_combs_idx, assume_unique=True)
        possible_combs = all_combs[possible_combs_idx]
        pool_size = len(possible_combs)
        
        # initialise lists of expected bits and probabilities of being right
        exp_bits_for_each_comb = []
        right_probs_for_each_comb = []

        # for every feature combination
        for try_comb_idx, try_comb in enumerate(all_combs):
            
            # compute score frequency
            rcrf_scores = RCRF[try_comb_idx, possible_combs_idx]
            score_frequency = Counter(rcrf_scores)
            
            # expected bits
            score_probs = np.array(list(
            score_frequency.values()
            )) / pool_size # unordered; ommitted scores with probability 0
            score_bits = -np.log2(score_probs)
            exp_bits = (score_probs * score_bits).sum()
            exp_bits_for_each_comb.append(exp_bits)

            # probability of being right
            right_frequency = score_frequency.get(4)
            right_prob = 0 if right_frequency is None else right_frequency / pool_size
            right_probs_for_each_comb.append(right_prob)
        
        right_probs_for_each_comb = np.array(right_probs_for_each_comb)

        # get indices of combinations which provide maximal bit
        max_bits_combs_idx = np.where(exp_bits_for_each_comb == np.max(exp_bits_for_each_comb))[0]

        # from the list of combinations which provide maximal bits, choose the one with the highest probability of being right
        max_bits_max_right_prob_combs_idx = np.argmax(right_probs_for_each_comb[max_bits_combs_idx])

        # guess
        guess_feat_vec_idx = max_bits_combs_idx[max_bits_max_right_prob_combs_idx]
        guess_feat_vec = all_combs[guess_feat_vec_idx]
        guess_res = reveal(guess_feat_vec, true_feat_vec)
        guess_count += 1
    guess_counts.append(guess_count)
    print(f"Testing on {m+1}th feature vector")
print(guess_counts)

# with open("solver_intermediate_guess_counts1.pickle", "wb") as handle:
#     pickle.dump(guess_counts, handle)

# with open("Purble-Shop-Solver/data_and_graphs/solver_intermediate_guess_counts1.pickle", 'rb') as handle:
#     guess_counts = pickle.load(handle)

bins = np.arange(0, np.max(guess_counts) + 1.5) - 0.5
fig, ax = plt.subplots()
ax.hist(guess_counts, bins)
ax.set_xticks(bins + 0.5)
ax.set_xlabel("number of guesses")
ax.set_ylabel("frequency")
plt.tight_layout()
# plt.savefig("Purble-Shop-Solver/data_and_graphs/solver_intermediate_guess_count_graph1.png")
plt.show()