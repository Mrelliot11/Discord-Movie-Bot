DISCORD MOVIE BOT

# Description

This is a discord movie bot that can run commands for a movie night. The bot is run on python with data storage using sqlite, and stores movie choices to be picked at random from a discord channel. 

# Requirements
## Windows:

Requires [Fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/), [imdbPy](https://cinemagoer.github.io/), and [DiscordPy](https://discordpy.readthedocs.io/en/stable/intro.html#installing)

`pip install fuzzywuzzy`

`pip install cinemagoer`

`py -3 -m pip install -U discord.py`

# COMMANDS

- !addmovie: adds your movie choice to the database if not already present.

- !pick: chooses a movie at random and gives IMDB listing

- !movies: shows all the movies put into the db so far

- !eraseall: deletes all the movies in the .db file

- !search: searches the list of entered movies for the entered movie

- !delete: deletes the entered movie
