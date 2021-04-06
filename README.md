# Momentum Football Bets - Honer's Algorithm

<p align="center">
<img width="364" alt="honers" src="https://user-images.githubusercontent.com/25267873/113485553-fff9ae80-94a5-11eb-86a6-298693f5ba65.png">
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#install">Install</a></li>
    <li><a href="#concept">Concept</a></li>
    <li><a href="#example">Example</a> </li>
    <li><a href="#license">License</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
    <li><a href="#future-improvements">Future Improvements</a></li>
  </ol>
</details>

## About The Project

The aim of this project is to try and estimate each team's momentum based on their near future fixtures. This is based on the stats of the last 6 results of each of the teams. Then, it attempts to estimate the risk of a bet by calculating the momentum gap between both teams. The end goal is to improve your football acca's odds. 

The data is gathered by web scraping SkySports website. E.g. https://www.skysports.com/premier-league-fixtures for fixtures, and https://www.skysports.com/football/wolverhampton-wanderers-vs-liverpool/stats/429116 for fixture stats (where is possible to find last 6 match results).

As an input given as an argument, it is allowed to select:
  * -d/--days: How many days in the future to look for fixtures. Default: 4.
  * -c/--confidence: What is the confidence threshold that the user wants output. Default: 0, i.e. no filter in place.

## Install

This project was originally written and tested with Python 3.6.8.

1. Install Anaconda

The recommendation is to use this project with Anaconda's Python distribution - either full [__Anaconda3 Latest__](https://repo.anaconda.com/archive/) or [__Miniconda3 Latest__](https://repo.anaconda.com/archive/).

Confirm that you have it with: `conda -V`. The output should be something along the lines of: `conda 4.9.2`

2. Create Environment

You can name the environment whatever you want, e.g.: `bets`.
```
conda create -n bets python=3.6.8
````

3. Activate the virtual environment
```
conda activate bets
```
Note: At the end, you can deactivate it with: `conda deactivate`

4. Fork the Project

- Via HTTPS: `https://github.com/DidierRLopes/momentum-football-bets.git`
- via SSH:  `git@github.com:DidierRLopes/momentum-football-bets.git`

Navigate into the folder with: `cd momentum-football-bets/`

5. Install poetry
```
conda install poetry
```

6. Install poetry dependencies
```
poetry install
```
This is a library for package management, and ensures a smoother experience than: ``pip install -r requirements.txt``. Although the later should also work just fine.

7.  You're ready to Bet!

```
python honers.py
```


## Concept

Firstly, we attribute 6 points to last result of a team, 5 points to the previous to that one, and so on. 

Secondly, based on the outcome of the results, the points will be either positive (+1) in case of a winning, negative (-1) in case of a loss, and 0 otherwise (i.e. draw).

**Momentum Score**

The momentum score is then achieved using these combination between last 6 games and their outcomes.

E.g. If Liverpool last match results were: WIN, WIN, WIN, DRAW, LOSE, DRAW, from more recent to older. 

Liverpool's momentum score would be: (6 x (+1)) + (5 x (+1)) + (4 x (+1)) + (3 x (0)) + (2 x (-1)) + (1 x (0)) = 13

Internally, the program's momentum score is splitted across the following bins/descriptions, with min and MAX being -21 and +21, respectively.


![momentum](https://user-images.githubusercontent.com/25267873/113485974-494afd80-94a8-11eb-8fa7-44ef9ddb7e65.jpg)


**Bet Confidence**

Since the momentum of a team only shows one side of the story, you need to compare the momentum of the teams that are playing each other in order to estimate if your bet is risky/safe.

E.g. If Liverpool is having an Excellent momentum of 6 wins in a row, and so is Manchester United, this is considered a risky bet. 

However, if Liverpool has draw all their previous match, and therefore have a momentum of 0, BUT United has loss all the previous 6 matches, (i.e. momentum of -21), this may be worth a bet due to the disgusting momentum of United.

Hence, the Bet Confidence is estimated from the difference between the momentum score of both teams. The bigger the gap score, the less risky will the app be. 

Internally, the program's bet confidence is splitted across the following bins/descriptions, with min and MAX being 0 and +42, respectively.

![confidence](https://user-images.githubusercontent.com/25267873/113485973-4819d080-94a8-11eb-920f-ed78733d24b6.jpg)

## Example

<img width="706" alt="example" src="https://user-images.githubusercontent.com/25267873/113477261-88f9f100-9478-11eb-9cb0-74936de34078.png">

This is the perfect example of how this algorithm still needs tuning and will not guess the outcome of a game, since Chelsea lost 5-2. And that's the reason why we like football. 

## License

Distributed under the MIT License. See [LICENSE](https://github.com/DidierRLopes/momentum-football-bets/blob/main/LICENSE) for more information.

## Disclaimer

I'm NO Bets advisor. This was made for fun, and to automate a due diligence boring task.

## Future Improvements

* Improve scoring algorithm weights
* Consider ranking of opponent team in last results
* Consider competition in last results (e.g. champions league more weight than premier league)
