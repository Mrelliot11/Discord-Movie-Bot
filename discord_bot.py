# Discord bot script
import os
from getpass import getpass
from mysql.connector import connect, Error
from typing import Text
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3

connection = sqlite3.connect("movies.db")
cursor = connection.cursor()

connection.commit()
rows = cursor.execute("SELECT * FROM movies").fetchall()

print(rows)
# TODO: switch this to the .command function

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')

@bot.command(name='addmovie', help='adds the movie of your choice to a database of movie choices')
async def add_movie(ctx, movie):


    insert_movies_query = """
    INSERT INTO movies (name) 
    VALUES (
    """  + movie + """ )"""




    response = 'You have logged {}'.format(movie)
    await ctx.send(response)


bot.run(TOKEN)