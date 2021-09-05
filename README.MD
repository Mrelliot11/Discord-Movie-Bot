DISCORD MOVIE BOT

This is a discord movie bot that can run commands for a movie night. The bot is run on python with data storage using sqlite, and stores movie choices to be picked at random from a discord channel. 


Make sure to use dashes for the movie name if there are multiple words.

COMMANDS:

!addmovie 'movie-name': adds your movie choice to the database, if the movie is already present you will be asked to add a different movie.

!pick: chooses a movie at random

!movies: shows all the movies put into the db so far

!eraseall: deletes all the movies in the .db file