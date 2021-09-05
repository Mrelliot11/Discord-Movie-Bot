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

@bot.command(name='addmovie', help='adds the movie of your choice to a database of movie choices')
async def add_movie(ctx, movie):
    rows = cursor.execute('SELECT name FROM movies').fetchall()
    rw = functools.reduce(operator.add, rows)
    if (movie in rw):
            # TODO: turn tuple into name string, check name for dupes
           response = "That movie is already in the database, try again" 
    else: 
            insert_movie(movie)
            response = 'You have logged {}'.format(movie)
    await ctx.send(response)

        
            
    
def insert_movie(movie):
    #create an insert statement to make it easier
        insert_movies_query = '''INSERT INTO movies (name) VALUES''' + '(' + "'" + movie + "'" + ')'
    #insert the movie data
        cursor.execute(insert_movies_query)
    #this is required after changes are made to commit them to db
        connection.commit()

@bot.command(name='pickmovie', help='pick a random movie from the list')
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
