import discord
from discord.ext import commands
from URLReader import URLReader

import random

token = open("token.txt", "r").read()
channel_log_id = open("channel_log.txt", "r").read()

PREFIX = '>'

client = commands.Bot(command_prefix = PREFIX)

dms = []
channels = []

def begins(text, start):
    return text.content.lower().startswith(PREFIX+start)

def begins_np(text, start, prefix):
    return text.content.lower().startswith(prefix+start)

def find_dms(name):
    for i in range(0, len(dms)):
        if name == dms[i]:
            return i

    return -1

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    global dms

    #essential commands (don't alter)

    if begins(message, 'ping'):
        await message.channel.send(f'Pong! {round(client.latency * 1000)}ms')

    if begins(message, 'typerace'):
        words = message.content.split()

        if len(words)<3:
            await message.channel.send('https://www.nitrotype.com/race/'+message.author.name)
            return

        await message.channel.send('https://www.nitrotype.com/race/'+words[2])

    if begins(message, 'dice'):
        words = message.content.split()

        if len(words) < 3:
            await message.channel.send(str(int(random.random()*6)+1))
            return

        if words[2].isnumeric() and int(words[2])>=2 and int(words[2])<=1000000:
            await message.channel.send(str(int(random.random()*int(words[2]))+1))
            return

        await message.channel.send('Give number of sides [2, 1000000]')

    #utility commands (can alter)

    if begins(message, 'chess'):
        words = message.content.split()
        await message.channel.send('https://www.chess.com/play/'+words[2])
    if begins(message, 'daddy'):
        await message.channel.send('DADDDY RYAANNNNNN :hot_face: :hot_face: :hot_face:')
        await message.channel.send('https://tenor.com/view/ryan-reynolds-kiss-handsome-smile-gif-17092194')
    if begins(message, 'you-suck'):
        await message.channel.send('You suck vincent and mihir imagine being in software pleb')
    if begins(message, 'rhino'):
        await message.channel.send(' SMACK zZz :pinched_fingers: :pinched_fingers: :pinched_fingers:')
    if begins(message, 'conlin'):
        await message.channel.send('conlin is always daddy')
    if begins(message, 'carl-bot'):
        await message.channel.send('Carl-Bot is trash, Gamer-Bot is the future!')
    if begins(message, 'burnt') or begins(message, 'roasted'):
        await message.channel.send('https://tenor.com/IRyK.gif')
    if begins(message, 'cap'):
        await message.channel.send('https://tenor.com/boU4B.gif')
    if begins(message, 'fun times'):
        await message.channel.send('https://tenor.com/bB7t6.gif')

    #Reads dms then sends it to the given channel, only sends back to log if this is the first reply from that user
    #To get to gamer logs
    #channel = client.get_channel(int(channel_log_id))
    rank = find_dms(message.author.name)
    if message.guild is None and message.author != client.user and rank>-1:
        dms.pop(rank)
        channel = channels[rank]
        await channel.send(message.author.mention+' just sent: "'+message.content+'"')
        channels.pop(rank)

    await client.process_commands(message)

@client.command(pass_context=True)
async def cnick(ctx, member: discord.Member, new_name):
    roles = ctx.message.author.roles
    mod = False
    for i in range(0, len(roles)):
        if roles[i].name=="Mod":
            mod = True
            i = len(roles)
    
    if mod or ctx.message.author.id == member.id:
        await ctx.send("Changed nickname: "+member.name+" to "+new_name)
        await member.edit(nick = new_name)
    else:
        await ctx.send("Need to be mod! Otherwise, you can only change your own name!")

@client.command(pass_context=True)
async def attack(ctx, member: discord.Member):
    await ctx.send(member.mention)
    await ctx.send("Just attacked "+member.name)

@client.command(pass_context=True)
async def dm(ctx, user : discord.User, *, msg):
    global dms

    dms.append(user.name)
    channels.append(ctx.message.channel)
    
    try:
        await user.send(msg)
        await ctx.send(f'Your Message has been sent')
    except:
        await user.create_dm()
        await user.send(msg)
        await ctx.send(f'A new dm has been created and your Message has been sent')

client.run(token)
