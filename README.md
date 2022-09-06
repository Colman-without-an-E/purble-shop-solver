# Purble Shop Solver
Hey, you! Remember Purble Place?

<img src="https://windowsreport.com/wp-content/uploads/2022/07/Purble-Place-Windows-11-1.png" height=200>

Of course you do. Everyone knows this. 

Recently, a sudden wave of nostalgia commanded me to download Purble Place, and I had a few <sup>*(too many)*</sup> games on Comfy Cake. 

<img src="graphics/comfy_cakes_stats.png" height=150>

Not to brag, but I'm pretty good at it.

My confidence persuaded me into trying my luck at Purble Shop, and it didn't take long for me to realise I was ***terrible*** at it. Like ***really terrible***. So I did what most people would do in my situation:

<p align=center>
    <img src="graphics/text1.png" width=250>
</p>

And it is quite successful. If you want to use the bot immediately, see the [solver instruction](#solver-instruction) section. 
## How to play
If you haven't played Purble Shop before, you are still very welcome here *(albeit less welcome)* and here is how to play the game. 

There are three difficulties: beginner, intermediate, and advanced. Let's use the beginner difficulty to illustrate what's going on. 

When you start the game, you are greeted with this interface. 
<p align=center>
    <img src="graphics/purble_shop_beginner_start_interface.png" height=180>
</p>

In the wardrobe, there are three features (eyes, nose, and mouth), and for each feature there are three colours (red, purble, yellow). The goal of this game is to guess the correct set of features of this blue butt-plug-looking creature. No offense. 

But how do we know what the correct set of features is?

Answer:
<p style="text-align:center; font-size:20px">We guess!</p>

After picking a set of features (here I picked red eyes, red nose, and red mouth), the game tells you how many features you got right. 

<p align=center>
    <img src="graphics/purble_shop_beginner_guess1_interface.png" height=180>
</p>

In this case, we got two features right. Since this is the beginner difficulty, the game is very generous in telling us which specific features we got right. 

We have seven tries in total to guess. 

In intermediate difficulty, there are four features in total and four colours for each features. And we are not given which specific features we got right. Only the number of right features are given. 

In advanced difficulty, there are five features in total and five colours for each features. However, we are given one extra piece of information besides the number of right features: the number of ***right colour***, but ***wrong feature***. 

<p align=center>
    <img src="graphics/purble_shop_advanced_guess1_interface.png" height=180>
</p>

It's a very simple game, but it requires a heightened sense of logic. 

## Approach

Perhaps counter-intuitive, but you should not guess the set of features you think is the most likely to be right. Instead, we should eliminate as many sets of features based on give information. In other words, we are maximising the ***amount of information*** we will obtain for each guess. In fact, maximising the probability of being right will result in a poorer performance (see [analysis](#analysis) section). 

When I first started approaching this problem mathematically, I was immediately reminded of <a href="https://www.youtube.com/watch?v=v68zYyaEmEA&t=601s">3Blue1Brown's video</a> on solving <a href="https://www.nytimes.com/games/wordle/index.html">Wordle</a>. This approach uses extremely similar idea, so I recommend watching his video for more information (and nicer graphic too!). 

## Solver instruction
There are two solvers:
- [intermediate difficulty solver](solver_intermediate.py)
- [advanced difficulty solver](solver_advanced.py)

The solvers run on Python and take in standard inputs. Below are the steps to steps to running them in your local machine
1. Download solvers ([intermediate difficulty solver](solver_intermediate.py), [advanced difficulty solver](solver_advanced.py))
2. Install required package ([NumPy](https://numpy.org/doc/)) into your environment

    ```
    > pip install numpy
    ```
3. Change to your directory with the downloaded solver files and run the solver of your choice
    ```
    > python solver_advanced.py
    ```
4. Follow the instruction given

Here is an example of how an advanced game goes using the advanced difficulty solver. Before the game starts, you enter the colour symbols.  You might want to use short symbols like initial letter of colour or numbers, but for illustration purposes, I'll just use the colour name in full. 

```
Enter colour symbols

Colour 1: red
Colour 2: purple
Colour 3: yellow
Colour 4: blue
Colour 5: green
```

From here on out, you input the features you guessed and their corresponding results in the game into the terminal. Some useful information will be printed and you decide which features to guess. Rinse and repeat.

For my first guess, I'll guess red, red, red, red, and red. It really doesn't matter what your first guess is. 

<p align=center>
    <img src="graphics/purble_shop_advanced_guess1.png", height=180>
</p>

1 right colour right feature, and 0 right colour wrong features. Let the solver know that:
```
Feature vector guessed: red red red red red
Number of right colour right features: 1
Number of right colour wrong features: 0

Most probable guesses
'blue red blue yellow blue'   ----   0.078125%
'blue red blue yellow yellow'   ----   0.078125%
'blue red blue yellow green'   ----   0.078125%
'blue red blue yellow purple'   ----   0.078125%
'red green blue blue yellow'   ----   0.078125%

Recommend trying the combination 'red purple purple blue blue' since it provides the most expected information
```
Even the best guess has only a 0.078125% chance of being correct. So let's try getting more information by using the solver's suggestion in the game:

<p align=center>
    <img src="graphics/purble_shop_advanced_guess2.png", height=180>
</p>

Let the solver know that:
```
Feature vector guessed: red purple purple blue blue
Number of right colour right feature: 2
Number of right colour wrong features: 0

Most probable guesses
'red green green blue green'   ----   3.125%
'red yellow green green blue'   ----   3.125%
'red yellow green blue green'   ----   3.125%
'red green green green blue'   ----   3.125%
'red yellow purple green green'   ----   3.125%

Recommend trying the combination 'yellow yellow purple green yellow' since it provides the most expected information
```
Again, let's try the suggestion. 

<p align=center>
    <img src="graphics/purble_shop_advanced_guess3.png", height=180>
</p>

```
Feature vector guessed: red purple purple blue blue
Number of right colour right feature: 2
Number of right colour wrong features: 0

Most probable guesses
'red purple green green yellow'   ----   25.0%
'red yellow yellow green blue'   ----   25.0%
'red yellow yellow blue yellow'   ----   25.0%
'red yellow green blue yellow'   ----   25.0%
'purple blue purple purple green'   ----   0.0%

Recommend trying the combination 'red purple green green yellow' since it provides the most expected information
```
The solver has narrowed it to only **4** choices! Let's hope this is the final guess...

<p align=center>
    <img src="graphics/purble_shop_advanced_guess4.png", height=180>
</p>

Ooh! Not quite right! But after entering our guess into our terminal, 

```
Feature vector guessed: red purple green green yellow
Number of right colour right feature: 2
Number of right colour wrong features: 1

Most probable guesses
'red yellow yellow green blue'   ----   100.0%
'purple blue purple blue purple'   ----   0.0%
'purple blue purple blue yellow'   ----   0.0%
'green green green green green'   ----   0.0%
'purple blue purple blue blue'   ----   0.0%

Recommend trying the combination 'red yellow yellow green blue' since it provides the most expected information
```
We've got the answer! Now, let's see if it works!

<figure align=center>
    <img src="graphics/purble_shop_advanced_guess5.png", height=180>
</figure>

Yep! It works! And it only took us 5 tries! 
```
Feature vector guessed: red yellow yellow green blue
Number of right colour right features: 5
Number of right colour wrong features: 0

Congratulations! You are correct on your 5th guess.
```

## Analysis

Since the solver is deterministic, i.e. given the same guesses it will always give the same recommendation, we can easily analyse its performance by going through every single possible feature combination and count how many guesses are needed. 

<figure align=center>
    <img src=data_and_graphs/intermediate_guess_frequency_graph1.png width=250>
    <figcaption>
    Figure 1: Frequency graph of number of guesses with intermediate level solver; maximising amount of information
    </figcaption>
</figure>

The solver succeeded in finding the correct four-feature-four-colour combination in at most 7 tries. In particular, the combinations: 

`['c', 'd', 'b', 'c']`
<br>
`['c', 'd', 'c', 'a']`
<br>
`['d', 'd', 'c', 'b']`

where `'a', 'b', 'c', 'd'` symbolise the four colours in order, take 7 guesses to get right. But on average, it takes only **5.11** guesses to get it right. 

### Comparing approaches

Let's compare the two different approaches of: 

1. maximising the **amount of expected information** (which the solver runs on), and
2. maximising the **probability of being right**

<figure align=center>
    <img src=data_and_graphs/intermediate_guess_frequency_graph2.png width=250>
    <figcaption>
    Figure 2: Frequency graph of number of guesses with intermediate level solver; maximising probability of being right
    </figcaption>
</figure>

Well, it's like the graph speaks for itself. Obviously, maximising probability of being right performs worse, taking up to 10 guesses for some combinations. However, in terms of average number of guesses required, it isn't all that bad! On average, it takes **5.19** guesses to get it right. 

What about the solver for advanced level difficulty? Surely, it wouldn't perform nearly as well as that for intermediate level difficulty! Right...?

<figure align=center>
    <img src=data_and_graphs/advanced_guess_frequency_graph1.png width=250>
    <figcaption>
    Figure 3: Frequency graph of number of guesses with advanced level solver; maximising amount of information
    </figcaption>
</figure>

<figure align=center>
    <img src=data_and_graphs/advanced_guess_frequency_graph2.png width=250>
    <figcaption>
    Figure 4: Frequency graph of number of guesses with advanced level solver; maximising probability of being right
    </figcaption>
</figure>

Surprisingly, it performs arguably better than that for intermediate level difficulty (see figure 3). It also takes at most 7 guesses to get it right, but an astounding 🌟**4.95**🌟 guesses to get it right on average! 

Even if the less optimal approach of maximising probability of being right is used (see figure 4), it still only takes **4.98** guesses to get it right on average! ***And***, you can even be sure that you'll get it right in 7 guesses or less! 

Here is summary below. 

Table 5: Expected number of guesses of solvers for intermediate and advanced difficulty level using the two different approaches

|Maximising                    |Intermediate|Advanced|
|------------------------------|:----------:|:------:|
|Expected amount of information|    5.11    |  4.95  |
|Probability of being right    |    5.19    |  4.98  |