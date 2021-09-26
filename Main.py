import discord
from discord.ext import commands

token = open("token.txt", "r").read()

PREFIX = '-g '

client = commands.Bot(command_prefix = PREFIX)

def begins(text, start):
    return text.content.lower().startswith(PREFIX+start)

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    
    if begins(message, 'ping'):
        await message.channel.send(f'Pong! {round(client.latency * 1000)}ms')


client.run(token)
