# Discord bot script
import os

import discord





client = discord.Client('ODgzMDk4NzM4NDMwNzIyMDk4.YTE_yg.S95Zy9rwf1ycp60lgxraYQBbaQk')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run('your token here')
