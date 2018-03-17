# snake
implementation for the 2018 battlesnake

### Overview

First, each move is ranked by how good it is for getting towards food. This is weighted by how clustered the food is, how near we are too it, and if we are the closest snake. The snake is as greedy as possible, and will never pass on food if it decides its safe. 

Then, beginning with the highest priority move, we perform a number of heuristics in order to determine if it's sufficiently safe to take. We accept (and return) the highest priority move that meets our safety requirements. The requirements heuristics are:
    - Look for a path that goes `n` moves into the future, where `n` is the length of the longest snake. Each move, assume every snake takes a step forward (thus freeing its tale at each step).
    - Ideally, use a path that doesn't require a tile within 2 tiles of another snakes head. If that fails for every valid move, try not using any tiles directly adjacent, and if that still fails ignore this step completely.  
    - For each move, compute the number of paths that go 4 moves into the future. (The maximum value is 3^4) If one move has a significantly higher amount of possible paths than the others, select that move instead. This prevents us from cornering ourselves in a place that is easily cut off. . 
    - All of the above failed? Use floodfill and move into the largest component. 

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
