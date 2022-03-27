# Discord bot script
from concurrent.futures import process
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import sqlite3
import functools
import operator
from fuzzywuzzy import process
from imdb import Cinemagoer

print("Starting Movie Bot...")

# call imdb py and set
ia = Cinemagoer()

#check if connection exists
try:
    # connect to sqlite db file
    connection = sqlite3.connect("movies.db")
    print("Connection to database successful")
    #set cursor
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies (name TEXT, id INTEGER PRIMARY KEY)""")
# if connection fails
except NameError:
    print("No connection to db")

# load .env file
load_dotenv()
# assign token to variable
TOKEN = os.getenv('DISCORD_TOKEN')
# you can change what channels the bot is allowed in here
allowed_channel = ['movie-suggestions', 'movie-night-suggestions']
# setting help command in bot help menu
help_command = commands.DefaultHelpCommand(no_category='Commands')
# initialize bot object
bot = commands.Bot(
    command_prefix='$',
    description='A movie bot to help you make the hard decisions :)',
    help_command=help_command)

@bot.event
async def on_command_error(ctx, error):
    if ctx.channel.name in allowed_channel:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Bad argument')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('You do not have permission to use this command')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send('This command is on cooldown')
        else:
            await ctx.send('An error has occured' + str(error))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='movies with the boys'), status=discord.Status.idle)
            
            
@bot.command(
    name='addmovie',
    aliases = ['add', 'addmov'],
    help=
    ': This command adds the movie of your choice to a database of movie choices, if the choice is already there it '
    'will not add it. E.G. !addmovie The Matrix'
)
async def add_movie(ctx, *args):
    
    movie = ' '.join(args)
    #check if movie exists
    if (movie != "") and (movie != None):
         # check if correct channel
        if ctx.channel.name in allowed_channel:
        # grab names from db as list
            rows = cursor.execute('SELECT name FROM movies').fetchall()
            # check if db has data
            if rows:
                # if db has data, reduce tuple to single name
                rw = functools.reduce(operator.add, rows)
                # to pass here and check against db
                if movie.lower() in rw:
                    response = "That movie is already in the database, try again"
                else:
                    # insert movie into db
                    insert_movie_sql(movie.lower())
                    response = 'You have added {}'.format(movie)

            else:
                # if no movies in db, this adds it
                response = 'You have added {}'.format(movie)
                insert_movie_sql(movie.lower())
        else:
            response = "Please post commands in {} only".format(allowed_channel)
    else: 
        response = "Please enter a movie name e.g. !addmovie The Matrix"
    await ctx.send(response)
    
@bot.command(name='find', alises= ['searchmov', 'searchmovie', 'check'], help= ': This command searches for a movie of your choice in the database, if the movie is not in the database it will not search for it. e.g. !search The Matrix')
async def search_movie(ctx, *args):
    
    movie = ' '.join(args)
    if ctx.channel.name in allowed_channel:
        rows = cursor.execute('SELECT name FROM movies').fetchall()
        if rows:
            rw = functools.reduce(operator.add, rows)
            #use fuzzywuzzy to find the closest match in rw
            choices = rw
            #grab tuple of best choice from rw
            score = process.extractOne(movie, choices)
            #get score from tuple   (score, choice)
            scoreNumber = score[1]
            #if score is greater than 90%, we assume it is a match
            if scoreNumber > 90:
                response = '{} is in the database'.format(movie.lower())
            else: #if not, we assume it is not in the db
                response = '{} is not in the database'.format(movie.lower())    
        else:
            response = "There are no movies in the database."
    else:
        response = "Please post commands in {} only".format(allowed_channel)
    await ctx.send(response)
    
@bot.command(name='movies',
             alises = ['mov', 'show', 'showmovies'],
             help=': This command will show the current choices for movies')
async def check_movie_list(ctx):
    if ctx.channel.name in allowed_channel:
        response = 'The current movies are: '
        rows = cursor.execute('SELECT name FROM movies').fetchall()
        if rows:
            for movie in rows:
                if movie != "":
                    response = response + '\n' + movie[0]
        else:
            response = "The database is empty, please add movies!"
    else:
        response = "Please post commands in movie-suggestions only."
    await ctx.send(response)


@bot.command(name='eraseall',
             alises = ['eraseallmovies', 'erasemovies'],
             help=': Only use this if you really need to erase everything')
async def erase_movies(ctx):
    if ctx.channel.name in allowed_channel:
        # deletes all records
        cursor.execute('DELETE FROM movies WHERE id > 0')
        # commit to db
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
        if ctx.channel.name in allowed_channel:
            response = pick_movie_from_sql()
        else:
            response = "Please post commands in movie-suggestions only."
    else:
        response = "Database is empty, please add movies"
    await ctx.send(response)
    
@bot.command(name='delete',
             help=': This command will delete a movie from the list e.g !delete The Matrix')
async def delete_movie(ctx, *args):
    
    movie = ' '.join(args)
    if movie != "":
        if ctx.channel.name in allowed_channel:
            rows = cursor.execute('SELECT name FROM movies').fetchall()
            if rows:
                rw = functools.reduce(operator.add, rows)
                if movie.lower() in rw:
                    delete_movie_sql(movie.lower())
                    response = '{} has been deleted from the list'.format(movie)
                else:
                    response = 'That movie is not in the list'
            else:
                response = "The database is empty, please add movies!"
        else:
            response = "Please post commands in movie-suggestions only."
    else:
        response = "Please enter a movie name e.g !delete The Matrix"
    await ctx.send(response)

def pick_movie_from_sql():
    # create random choice from table ids
    random_choice = cursor.execute(
        'SELECT id FROM movies ORDER BY RANDOM() LIMIT 1').fetchone()
    # reduce id tuple to int
    st = functools.reduce(operator.add, random_choice)
    # select name from int id
    movie_choice = cursor.execute('SELECT name FROM movies WHERE id = ' +
                                  str(st)).fetchone()
    mc = functools.reduce(operator.add, movie_choice)
    # get movie name and reduce to string, then pass through imdb id search
    imdb_movie = ia.search_movie(mc)[0]
    # get movie url
    movie_url = ia.get_imdbURL(imdb_movie)
    # print movie url
    response = 'The movie of the night is {}'.format(mc) + "\n" + movie_url
    return response

def delete_movie_sql(movie): 
    cursor.execute('DELETE FROM movies WHERE name = ?', (movie,))
    connection.commit()

def insert_movie_sql(movie):
    # create an insert statement to make it easier
    insert_movies_query = '''INSERT INTO movies (name) VALUES''' + \
                          '(' + "'" + movie + "'" + ')'
    # insert the movie data
    cursor.execute(insert_movies_query)
    # this is required after changes are made to commit them to db
    connection.commit()

print("Movie Bot Started...")   

bot.run(TOKEN)
