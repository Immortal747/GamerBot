import discord
from discord.ext import commands

token = open("token.txt", "r").read()

PREFIX = '-G '

client = commands.Bot(command_prefix = PREFIX)

def begins(text, start):
    return text.lower().startswith(PREFIX+start)

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    text = message.content

    if begins(text, 'ping'):
        await message.channel.send(f'Pong! {round(client.latency * 1000)}ms')

    if begins(text, 'find '):
        tokens = text.split()
        member = discord.utils.find(lambda m: m.name == tokens[1], channel.guild.members)
        await message.channel.send(member)


client.run(token)
