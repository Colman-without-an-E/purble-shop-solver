import numpy as np
import itertools
import sys

instruction = "\n \n  Instruction: \n \n" \
    "This solves the intermediate level of the game 'Purble Shop' of 'Purble Place'.\n \n" \
    "After each guess in the game, you will be asked to input your guess, followed by " \
    "the result of it, i.e. the number of correct features.\n \n" \
    "To enter your guess, type the unique symbol representing each colour" \
    "in order of features with a space in between. \n \n"\
    "You will be given an example after you have chosen your colour symbols. \n \n" \
    "Have fun! \n \n \n"

if __name__ == "__main__":
    print(instruction)

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

print(f"\n \nEnter your guesses \ne.g.Enter")
print(" ".join(colours))
print(f"if first feature is {colours[0]}, second feature is {colours[1]}, and so on")

for k in range(10):
    guess_feat_vec = [str(x) for x in input("Feature vector guessed: ").split()]
    guess_res = int(input("Number of correct features: "))
    if guess_res == 4:
        ordinality = ["st", "nd", "rd"] + ["th"] * 7
        print(f"Congratulations! You are correct on your {k+1}{ordinality[k]} try.")
        break

    cond = (guess_feat_vec, guess_res)

    possible_combs = list_possible_combs(cond = cond, select_from = possible_combs)
    exp_bits = []
    right_probs = []
    for try_comb in all_combs:
        probs = []
        bits = []
        for i in range(5):
            p = len(list_possible_combs(cond = (try_comb, i), select_from = possible_combs)) / len(possible_combs)
            probs.append(p)
            bits.append(get_bits(p))
        exp_bits.append(np.sum(np.array(probs) * np.array(bits)))
        # print(f"The combination {try_comb} gives {np.sum(np.array(probs) * np.array(bits))} expected bits and is {100 * (try_comb.tolist() in possible_combs.tolist()) / len(possible_combs)}% correct.")
        right_probs.append((try_comb.tolist() in possible_combs.tolist()) / len(possible_combs))
    right_probs = np.array(right_probs)
    right_probs_desc_idx = (-right_probs).argsort()
    print("Most probable guesses:")
    for idx in right_probs_desc_idx[:5]:
        print(f"'{' '.join(all_combs[idx])}' -- {right_probs[idx] * 100}%")
    print(f"Recommend trying the combination '{' '.join(all_combs[np.argmax(exp_bits)])}' since it provides the most expected information")