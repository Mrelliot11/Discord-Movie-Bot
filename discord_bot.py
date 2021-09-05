# Discord bot script
import os
from discord.ext import commands
from discord.ext.commands.help import HelpCommand
from dotenv import load_dotenv
import sqlite3
import functools
import operator
import imdb
from imdb.Movie import Movie

ia = imdb.IMDb()

# connect to sqlite db file
connection = sqlite3.connect("movies.db")
cursor = connection.cursor()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

allowed_channel = 'movie-suggestions'
help_command = commands.DefaultHelpCommand(no_category='Commands')
bot = commands.Bot(
    command_prefix='!',
    description='A movie bot to help you make the hard decisions :)',
    help_command=help_command)


@bot.command(
    name='addmovie',
    help=
    ': This command adds the movie of your choice to a database of movie choices, if the choice is already there it will not add it.'
)
async def add_movie(ctx, movie):

    if ctx.channel.name == allowed_channel:
        # grab names from db as list
        rows = cursor.execute('SELECT name FROM movies').fetchall()
        if rows:
            # if db has data
            rw = functools.reduce(operator.add, rows)
            if (movie.lower() in rw):
                response = "That movie is already in the database, try again"
            else:
                insert_movie_sql(movie.lower())
                response = 'You have logged {}'.format(movie)

        else:
            # if no movies in db, this adds it
            response = "Movie Added"
            insert_movie_sql(movie.lower())
    else:
        response = "Please post commands in {} only".format(allowed_channel)
    await ctx.send(response)


@bot.command(name='movies',
             help=': This command will show the current choices for movies')
async def check_movie_list(ctx):
    if ctx.channel.name == allowed_channel:
        rows = cursor.execute('SELECT name FROM movies').fetchall()
        if rows:
            response = rows
        else:
            response = "The database is empty, please add movies!"
    else:
        response = "Please post commands in movie-suggestions only."
    await ctx.send(response)


@bot.command(name='eraseall',
             help=': Only use this if you really need to erase everything')
async def erase_movies(ctx):
    if ctx.channel.name == allowed_channel:
        cursor.execute('DELETE FROM movies WHERE id > 0')
        connection.commit()
        response = "Database Erased."
    else:
        response = "Please post commands in {} only".format(allowed_channel)

    await ctx.send(response)


def insert_movie_sql(movie):

    # create an insert statement to make it easier
    insert_movies_query = '''INSERT INTO movies (name) VALUES''' + \
        '(' + "'" + movie + "'" + ')'
    # insert the movie data
    cursor.execute(insert_movies_query)
    # this is required after changes are made to commit them to db
    connection.commit()


@bot.command(name='pick',
             help=': This command will pick a random movie from the list')
async def pick_movie(ctx):

    rows = cursor.execute('SELECT name FROM movies').fetchall()
    if rows:
        if ctx.channel.name == allowed_channel:
            response = pick_movie()

        else:
            response = "Please post commands in movie-suggestions only."
    else:
        response = "Database is empty, please add movies"
    await ctx.send(response)


def pick_movie():
    # create random choice from table ids
    random_choice = cursor.execute(
        'SELECT id FROM movies ORDER BY RANDOM() LIMIT 1').fetchone()
    st = functools.reduce(operator.add, random_choice)
    movie_choice = cursor.execute('SELECT name FROM movies WHERE id = ' +
                                  str(st)).fetchone()
    mc = functools.reduce(operator.add, movie_choice)

    imdb_movie = ia.search_movie(mc)
    imdb_movie_id = ia.get_movie(imdb_movie[0].getID())
    movie_url = ia.get_imdbURL(imdb_movie_id)
    response = 'The movie of the night is {}'.format(movie_url)
    return response


bot.run(TOKEN)
