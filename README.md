# snake2017
implementation for the 2017 battlesnake

to setup:
	pip install -r requirements.txt

To run:

Set up docker, as per the instructions found here: https://hub.docker.com/r/noelbk/battle_snake_server/

Start a snake server on your local machine with

    python main.py
See https://stemboltq.github.io/battle_snake/ for request format.

After setting up docker run with

    docker run -d -p 4000:4000 --net=host noelbk/battle_snake_server
insure snake server(s) themselves are on a PUBLIC port, ie

	0.0.0.0.whatever
DOCKER COMMANDS:

	q starts a game
	< rewinds
	> steps one move forward

