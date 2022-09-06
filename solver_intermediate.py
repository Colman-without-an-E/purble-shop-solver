import numpy as np
import itertools
from collections import Counter

if __name__ == "__main__":
    print("\n \n  Instruction: \n \n" \
    "This solves the intermediate level of the game 'Purble Shop' of 'Purble Place'.\n \n" \
    "After each guess in the game, you will be asked to input your guess, followed by " \
    "the result of it, i.e. the number of correct features.\n \n" \
    "To enter your guess, type the unique symbol representing each colour " \
    "in order of features with a space in between. \n \n"\
    "You will be given an example after you have chosen your colour symbols. \n \n" \
    "Have fun! \n \n \n")

dups_in_colours = True
flag = False
while dups_in_colours: # while there are duplicated colour symbols
    if flag:
        print("\n \nCannot have duplicated colour symbols!\n \n")
    print("Enter colour symbols\n")
    colours = []
    for i in range(4):
        colours.append(str(input(f"Colour {i+1}: ")))
    dups_in_colours = len(colours) != len(set(colours))
    flag = True

all_combs = np.array([list(feat_vec) for feat_vec in itertools.product(colours, repeat = 4)])
possible_combs = all_combs

# create right colour right feature score matrix
X = np.array([all_combs for i in range(4**4)])
Y = np.transpose(X, axes = (1,0,2))
RCRF = np.count_nonzero(X == Y, axis=2)

print(f"\n \nEnter your guesses \ne.g.Enter")
print(" ".join(colours))
print(f"if first feature is {colours[0]}, second feature is {colours[1]}, and so on")

# initialise possible feature combinations
possible_combs_idx = np.arange(len(all_combs))

# force stop after 10 guesses
for guess_count in range(10):
    
    # user input
    guess_feat_vec = [str(x) for x in input("\nFeature vector guessed: ").split()]
    guess_res = int(input("Number of right features: "))

    if guess_res == 4:
        break
    guess_feat_vec_idx = np.nonzero(np.all(all_combs == guess_feat_vec, axis = 1))[0][0]

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

        # compute score_frequency
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

    # print the 5 most probable guesses
    probable_guesses_idx = np.argpartition(right_probs_for_each_comb, -5)[-5:]
    probable_guesses_idx = probable_guesses_idx[np.argsort(-right_probs_for_each_comb[probable_guesses_idx])] # sort
    print("\nMost probable guesses")
    for idx in probable_guesses_idx:
        print(f"'{' '.join(all_combs[idx])}'   ----   {right_probs_for_each_comb[idx] * 100}%")

    # print recommended guess
    max_bits_combs_idx = np.where(exp_bits_for_each_comb == np.max(exp_bits_for_each_comb))[0]
    max_bits_max_right_prob_combs_idx = np.argmax(right_probs_for_each_comb[max_bits_combs_idx])
    recommended_guess_feat_vec = all_combs[max_bits_combs_idx[max_bits_max_right_prob_combs_idx]]
    print("\nRecommend trying the combination '{}' since it provides the most expected information".format(
        ' '.join(recommended_guess_feat_vec)
        ))

# print end message
ordinality = ["st", "nd", "rd"] + ["th"] * 7
print("\nCongratulations! You are correct on your {0}{1} guess.".format(
    guess_count+1, ordinality[guess_count]
    ))