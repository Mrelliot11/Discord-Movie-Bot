# Discord bot script
import os
from getpass import getpass
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import functools
import operator

#connect to sqlite db file
connection = sqlite3.connect("movies.db")
cursor = connection.cursor()

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.command(name='addmov', help=': This command adds the movie of your choice to a database of movie choices, if the choice is already there it will not add it.')
async def add_movie(ctx, movie):
    #grab names from db as list
    rows = cursor.execute('SELECT name FROM movies').fetchall()
    if rows:
        #if db has data
        rw = functools.reduce(operator.add, rows)
        if (movie.lower() in rw):
            response = "That movie is already in the database, try again" 
        else: 
                insert_movie(movie.lower())
                response = 'You have logged {}'.format(movie)
    
    else:
        #if no movies in db, this adds it
        response = "Movie Added"
        insert_movie(movie.lower())

    await ctx.send(response)



@bot.command(name='movies', help=': This command will show the current choices for movies')
async def check_movie_list(ctx):
      rows = cursor.execute('SELECT name FROM movies').fetchall()
      await ctx.send(rows)
    
@bot.command(name='eraseall', help=': Only use this if you really need to erase everything')
async def erase_movies(ctx):
        cursor.execute('DELETE FROM movies WHERE id > 0')
        connection.commit()
        await ctx.send("Database erased.")

def insert_movie(movie):
    #create an insert statement to make it easier
        insert_movies_query = '''INSERT INTO movies (name) VALUES''' + '(' + "'" + movie + "'" + ')'
    #insert the movie data
        cursor.execute(insert_movies_query)
    #this is required after changes are made to commit them to db
        connection.commit()

@bot.command(name='pickone', help=': This command will pick a random movie from the list')
async def pick_movie(ctx):
    response = pick_movie()
    await ctx.send(response)

def pick_movie():
    #create random choice from table ids
        random_choice = cursor.execute('SELECT id FROM movies ORDER BY RANDOM() LIMIT 1').fetchone()
        st = functools.reduce(operator.add, random_choice)
        movie_choice = cursor.execute('SELECT name FROM movies WHERE id = ' + str(st)).fetchone()
        mc = functools.reduce(operator.add, movie_choice)
        response = 'The movie of the night is {}'.format(mc)
        return response



bot.run(TOKEN)
