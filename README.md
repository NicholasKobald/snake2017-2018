Snake AI for the Battlesnake coding competition hosted in Victoria, BC.

### Prerequisites
* python 3 (prolly 3.4 + to be safe?)
* pip
* ngrok for local testing
* heroku (for real deployment)

### Setup

Get Python libraries:
```
pip install -r requirements.txt
```

Start a snake server on your local machine with:
```
python main.py
```

### Connect Local Snake to Public URL
* install [ngrok](https://ngrok.com/download), then run it:
* run `./ngrok http 5000` to connect local HTTP server running at port 5000 to a public forwarding URL
* find given public forwarding URL e.g. `https://318d8562.ngrok.io`
* create snake with public URL to [Battlesnake server](https://play.battlesnake.io/)


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

### Testing
Unit tests are added to replicate cases where our snake is making bad decisions and make sure it is no longer doing so. To add new tests:
* create a new module in the `tests/` directory that implements a `unittest.TestCase` subclass
* implement test functions in new class
* import new test class in `run_tests.py`
See `test_pick_move.py` for example.

Run tests:
```
python run_tests.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```