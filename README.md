# snake2017
implementation for the 2017 battlesnake


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
