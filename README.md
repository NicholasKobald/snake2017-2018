# snake
implementation for the 2018 battlesnake

### Overview

First, each move is ranked by how good it is for getting towards food. This is weighted by how clustered the food is, how near we are too it, and if we are the closest snake. The snake is as greedy as possible, and will never pass on food if it decides its safe. 

Then, beginning with the highest priority move, we compute a number of heuristics in order to determine if it's sufficiently safe to take. We accept (and return) the highest priority move that meets our safety requirements. The requirement heuristics are:

 - Look for a path that goes `n` moves into the future, where `n` is the length of the longest snake. Each move, assume every snake takes a step forward (thus freeing its tale at each step). This effectively generalizes the 'follow your tail logic' but will also work with other snakes tails. 
   - Ideally, use a path that doesn't require a tile within 2 tiles of another snakes head. If that fails for every valid move, try not using any tiles directly adjacent to a snake head, and if that still fails ignore this step completely.  
  - For each move, compute the number of paths that go 4 moves into the future. (The maximum value is 3^4). If the standard error (given by `improvement = 1.0 - (first_choice_val * 1.0) / max_val` between the best move according to this heuristic, and the current candidate move is more than 70%, this heuristic takes over. 
   - All of the above failed? Use flood-fill and move into the largest component (but we're probably dead if this ever happens). 


Of these heuristics, the first is the most important, and does the best job mimicking the search strategies that were used really effectively by some of the other successful snakes. 

#### Potential Improvements

There's a number of magic numbers all over the place, and it's really unlikely they are the best numbers that could be chosen. Actually simulating the snake across a lot of games to try to get good values there is one piece of low hanging fruit.

The weakest aspect of the snake is it's very unlikely to beat a properly implemented search-based snake in a 1v1 scenario, since we don't intentionally do anything to take advantage of a winning position. There's probably some things that could be done to try to account for that, such as using the voronoi heuristic when the game becomes a duel. 

When constructing our path of length `n`, we only take into account our own snake eating food, however in many cases we can be reasonably sure other snakes also intend on eating. At least estimating that could improve the first heuristic. 

Prerequisistes:

	docker
	python 3 (prolly 3.4 + to be safe?) 
	pip
	heroku (soon)


<h2> Snake Server </h2>


Get Python libraries:

	pip install -r requirements.txt

Start a snake server on your local machine with

    python main.py


Instructions for running the snake server locally (and documentation) over at: 

https://github.com/sendwithus/battlesnake

### Deploying 
if you are deploying the master branch,
```
heroku git:clone -a <heroku_repo_name>  
git push heroku master
```

If you are deploying a none-master branch (but still want it to build) 
```
heroku push heroku branchname:master 
``` 
