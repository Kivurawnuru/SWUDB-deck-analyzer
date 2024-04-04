# SWUDB-deck-analyzer
## About
Python script used for analyzing Star Wars Unlimited decks build by other players and shared on https://swudb.com/ with cards that you own. 

## Usage
Script can be used with database on swudb.com (option ```--mode online```) or with local database in csv file (option ```--mode local```). 
#### Online:
In order to use in online mode, you have to use your username and password (it can be done as parameter, or later script will ask you for it).
#### Local:
In order to use in local mode, you have to provide path to CSV file with cards. CSV should contain columns Set, CardNumber and Count. Example below:
```CSV
Set,CardNumber,Count
SOR,001,1
SOR,003,2
SOR,005,1
```

### Features:
#### Verify top 100 decks on swudb with card you own - result in % of owned cards. Example:
local database:\
```./deck_analyzer.py -m local -f mycards.csv --top```\
online account:\
```./deck_analyzer.py -m online --top```
#### Get missing cards for selected deck:
local database:\
```./deck_analyzer.py -m local -f mycards.csv --compare --url https://swudb.com/deck/view/PvthYvtFaQ```\
online account:\
```./deck_analyzer.py -m online --compare --url https://swudb.com/deck/view/PvthYvtFaQ```
