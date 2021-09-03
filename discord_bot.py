# Discord bot script
import os
from getpass import getpass
from mysql.connector import connect, Error
from typing import Text
from discord.ext import commands
import discord
from dotenv import load_dotenv



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')

@bot.command(name='addmovie', help='adds the movie of your choice to a database of movie choices')
async def add_movie(ctx, movie):

    try:
        with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="movies",
    ) as connection:
         print(connection)
    except Error as e:
        print(e)

    insert_movies_query = """
    INSERT INTO movies (Name) 
    VALUES (
    """  + movie + """ )"""




    response = 'You have logged {}'.format(movie)
    await ctx.send(response)


bot.run(TOKEN)