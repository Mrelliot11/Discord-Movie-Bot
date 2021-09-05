# Discord bot script
import os
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import functools
import operator
import imdb
#call imdb py and set
ia = imdb.IMDb()

# connect to sqlite db file
connection = sqlite3.connect("movies.db")
cursor = connection.cursor()
#load .env file
load_dotenv()
#assign token to variable
TOKEN = os.getenv('DISCORD_TOKEN')
#you can change what channels the bot is allowed in here
allowed_channel = 'movie-suggestions'
#setting help command in bot help menu
help_command = commands.DefaultHelpCommand(no_category='Commands')
#initialize bot object
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
    #check if correct channel
    if ctx.channel.name == allowed_channel:
        # grab names from db as list
        rows = cursor.execute('SELECT name FROM movies').fetchall()
        #check if db has data
        if rows:
            # if db has data, reduce tuple to single name
            rw = functools.reduce(operator.add, rows)
            #to pass here and check against db
            if (movie.lower() in rw):
                response = "That movie is already in the database, try again"
            else:
                #insert movie into db
                insert_movie_sql(movie.lower())
                response = 'You have added {}'.format(movie)

        else:
            # if no movies in db, this adds it
            response = 'You have added {}'.format(movie)
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
        #deletes all records
        cursor.execute('DELETE FROM movies WHERE id > 0')
        #commit to db
        connection.commit()
        response = "Database Erased."
    else:
        response = "Please post commands in {} only".format(allowed_channel)

    await ctx.send(response)

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
    #reduce id tuple to int
    st = functools.reduce(operator.add, random_choice)
    #select name from int id
    movie_choice = cursor.execute('SELECT name FROM movies WHERE id = ' +
                                  str(st)).fetchone()
    mc = functools.reduce(operator.add, movie_choice)
    #get movie name and reduce to string, then pass through imdb id search
    imdb_movie = ia.search_movie(mc)
    #grab imdb movie id from movie title
    imdb_movie_id = ia.get_movie(imdb_movie[0].getID())
    #get movie url
    movie_url = ia.get_imdbURL(imdb_movie_id)
    
    response = 'The movie of the night is {}'.format(movie_url)
    return response

def insert_movie_sql(movie):

    # create an insert statement to make it easier
    insert_movies_query = '''INSERT INTO movies (name) VALUES''' + \
        '(' + "'" + movie + "'" + ')'
    # insert the movie data
    cursor.execute(insert_movies_query)
    # this is required after changes are made to commit them to db
    connection.commit()


bot.run(TOKEN)
