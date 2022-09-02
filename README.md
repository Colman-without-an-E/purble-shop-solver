# Purble Shop Solver
Hey you! Remember Purble Place?

<img src="https://windowsreport.com/wp-content/uploads/2022/07/Purble-Place-Windows-11-1.png" width=200>

Of course you do. Everyone should know this. 

Recently, a sudden wave of nostalgia commanded me to download Purble Place, and I had a few <sup>*(too many)*</sup> games on Comfy Cake. 

<img src="graphics/comfy_cakes_stats.png" height=150>

Not to brag, but I'm pretty good at it.

My confidence persuaded me into trying my luck at Purble Shop, and it didn't take long for me to realise I was ***terrible*** at it. Like ***really terrible***. So I did what most people would do in my situation:
<p style="text-align:center; font-family: 'Brush Script MT'; font-size:30px; color:pink">
    Write a bot to solve it!
</p>

## How to play
If you haven't played Purble Shop before, you are still very welcome here *(albeit less welcome)* and here is how to play the game. 

There are three difficulties: beginner, intermediate, and advanced. Let's use the beginner difficulty to illustrate what's going on. 

When you start the game, you are greeted with this interface. 
<p align=center>
    <img src="graphics/purble_shop_beginner_start_interface.png" height=150>
</p>

In the wardrobe, there are three features (eyes, nose, and mouth), and for each feature there are three colours (red, purble, yellow). The goal of this game is to guess the correct set of features of this blue butt-plug-looking creature. No offense. 

But how do we know what the correct set of features is?

Answer:
<p style="text-align:center; font-size:20px">We guess!</p>

After picking a set of features (here I picked red eyes, red nose, and red mouth), the game tells you how many features you got right. 

<p align=center>
    <img src="graphics/purble_shop_beginner_guess1_interface.png" height=150>
</p>

In this case, we got two features right. Since this is the beginner difficulty, the game is very generous in telling us which specific features we got right. 

We have seven tries in total to guess. 

In intermediate difficulty, there are four features in total and four colours for each features. And we are not given which specific features we got right. Only the number of right features are given. 

In advanced difficulty, there are five features in total and five colours for each features. However, we are given one extra piece of information besides the number of right features: the number of ***right colour***, but ***wrong feature***. 

<p align=center>
    <img src="graphics/purble_shop_advanced_guess1_interface.png" height=150>
</p>

It's a very simple game, but it requires a heightened sense of logic. 

## The approach

Perhaps counter-intuitive, but you should not guess the set of features you think is the most likely to be right. Instead, we should eliminate as many sets of features based on give information. In other words, we are maximising the **amount of information** we will obtain for each guess. 

When I first started approaching this problem mathematically, I was immediately reminded of <a href="https://www.youtube.com/watch?v=v68zYyaEmEA&t=601s">3Blue1Brown's video</a> on solving <a href="https://www.nytimes.com/games/wordle/index.html">Wordle</a>. This approach uses extremely similar idea, so I recommend watching his video for more information (and nicer graphic too!). 