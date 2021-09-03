# Discord bot script
import os
<<<<<<< HEAD
=======
from getpass import getpass
from mysql.connector import connect, Error
from typing import Text
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import functools
import operator

#connect to sqlite db file
connection = sqlite3.connect("movies.db")
cursor = connection.cursor()
>>>>>>> 10b1d4dee3469347bf8884619e59e2330549dcd6

#set rows to object containing all movies from db
movie_names = cursor.execute("SELECT * FROM MOVIESTABLE").fetchall()

<<<<<<< HEAD
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
=======
print(movie_names)
# TODO: switch this to the .command function
>>>>>>> 10b1d4dee3469347bf8884619e59e2330549dcd6

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')

@bot.command(name='addmovie', help='adds the movie of your choice to a database of movie choices')
async def add_movie(ctx, movie):

    #create an insert statement to make it easier
    insert_movies_query = '''INSERT INTO MOVIESTABLE (name) VALUES''' + '(' + "'" + movie + "'" + ')'
    #insert the movie data
    cursor.execute(insert_movies_query)
    
    #this is required after changes are made to commit them to db
    connection.commit()

    #show response on discord end
    response = 'You have logged {}'.format(movie)
    await ctx.send(response)

<<<<<<< HEAD
client.run(TOKEN)
=======
@bot.command(name='pickmovie', help='pick a random movie from the list')
async def pick_movie(ctx):

    #create random choice from table ids
    random_choice = cursor.execute('SELECT id FROM moviestable ORDER BY RANDOM() LIMIT 1').fetchone()

    
    
    st = functools.reduce(operator.add, random_choice)
    print(st)
    movie_choice = cursor.execute('SELECT name FROM moviestable WHERE id = ' + str(st)).fetchone()
    mc = functools.reduce(operator.add, movie_choice)
    print(mc)
    response = 'The movie of the night is {}'.format(mc)
    
    await ctx.send(response)



bot.run(TOKEN)
>>>>>>> 10b1d4dee3469347bf8884619e59e2330549dcd6
