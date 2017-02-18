# snake2017
implementation for the 2017 battlesnake


Prerequisistes: 

	docker
	python 2.7.x
	pip
	heroku (soon)
	
Set up docker, as per the instructions found here: https://hub.docker.com/r/noelbk/battle_snake_server/

<h2> Snake Server </h2> 


Get Python libraries:

	pip install -r requirements.txt

Start a snake server on your local machine with

    python main.py
See https://stemboltq.github.io/battle_snake/ for request format.

<h2> Host Server </h2> 

After setting up docker run with

    DEPRECATED: docker run -d -p 4000:4000 --net=host noelbk/battle_snake_server
    docker run -d -p 4000:4000 --net=host stembolt/battle_snake
insure snake server(s) themselves are on a PUBLIC port, ie

	0.0.0.0.whatever
DOCKER COMMANDS:

	q starts a game
	< rewinds
	> steps one move forward

