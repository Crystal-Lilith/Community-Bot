import asyncio
import discord
import json
from discord.ext import commands

with open('token.txt') as f:
    token = f.read()

bot = commands.Bot(command_prefix='/')
bot.remove_command("help")

@bot.command(name='server-list')
async def server_list(ctx):
    ctx.send("Warning, it's a little spammy and takes a while to finish")
    for i in bot.guilds:
        await ctx.send(f'-{i.name}')
        #Sends a list of the current servers its in in the current channel

@bot.listen()
async def on_guild_join(guild):
    await bot.get_channel(635077321807626250).send(f'-{guild.name}')
    #Sends the list of servers to the server list channel

@bot.command(name='add-link')
async def add_link(ctx):
    CID = ctx.channel.id
    f=open('CIDs.json','r')
    CIDs = json.load(f)
    f.close()
    if ctx.channel.id in CIDs:
        await ctx.send('Channel is already in the cross-link network')
    else:
        await ctx.send(f'Adding <#{ctx.channel.id}> to the link network...')
        f=open('CIDs.json','w+')
        CIDs.append(CID)
        json.dump(CIDs,f)
        f.close()
        await ctx.send(f'Added <#{ctx.channel.id}> to `CIDs.json`, aka I enabled CrossLink in this channel')
    
@bot.command(name='remove-link')
async def remove_link(ctx):
    f=open('CIDs.json','r')
    CIDs = json.load(f)
    f.close()
    if ctx.channel.id not in CIDs:
        await ctx.send("This channel isn't in the cross-link network so I can't remove it...")
    else:
        await ctx.send(f'Removing <#{ctx.channel.id}> from the link network')
        CID = ctx.channel.id
        f=open('CIDs.json','w+')
        CIDs.remove(CID)
        json.dump(CIDs,f)
        f.close()
        await ctx.send(f'Removed <#{ctx.channel.id}> from `CIDs.json`, aka I disabled CrossLink in this channel')

@bot.listen()

async def on_message(message):
    f=open('CIDs.json','r')
    CIDs = json.load(f)
    f.close()
    msg = message.content
    msg = msg.replace("@", "(a)")
    X = 0
    if message.author.id != bot.user.id:
        await bot.get_channel(635055057662115851).send(f'{message.author}: {msg}') #The Interface for CrossLink for other bots
        try:
            if message.channel.id in CIDs:
                CIDs.remove(message.channel.id)
                for channel in CIDs:
                    await bot.get_channel(CIDs[X]).send(f'{message.author}: {msg}')
                    X = X + 1
                CIDs.append[message.channel.id]
                

            else:
                pass
        except:
            pass



@bot.listen()
async def on_message(message):
    if message.channel.id == 634838725314215936:
        if message.author.id == 269964546322464770:
            try:
                apimsg = message.content
                apimsg = msg.replace("@", "(a)")
                f=open('CIDs.json','r')
                CIDs = json.load(f)
                f.close()
                X = 0
                for channel in CIDs:
                    await bot.get_channel(CIDs[X]).send(f'{apimsg}')
                    X = X + 1
            except:
                pass
@bot.listen()
async def on_ready():
    print('Bot has been started')
    while True:

        activity = discord.Activity(name='Nightcore', type=discord.ActivityType.listening)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)

        activity = discord.Activity(name=(f'{len(bot.guilds)} Servers'), type=discord.ActivityType.watching)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)

        activity = discord.Activity(name='on ManjaroPE (Best Mcpe Server)', type=discord.ActivityType.playing)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)

        activity = discord.Activity(name='/help to people using this bot', type=discord.ActivityType.streaming)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)

@bot.command(name='server-count')
async def server_count(ctx):
        await ctx.send(f"I'm in {len(bot.guilds)} servers!")

@bot.command()
async def github(ctx):
    embed=discord.Embed(title="GitHub", description="Thanks you for being interested in Community bot! If you want to commit please know we don't mind whatever language you choose to help us(Even `C`)\nhttps://github.com/IpProxyNeon/Community-discord-bot/blob/master/README.md", color=0x00ffff)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    help=open('help1.txt','r')
    await ctx.send(help.read())
    help.close()

@bot.command()
async def invite(ctx):
    await ctx.send("Thanks for inviting me to your server!\nhttps://discordapp.com/oauth2/authorize?client_id=610225885093691467&scope=bot&permissions=8")

@bot.command()
async def support(ctx):
    await ctx.send("Here's the link for the support server!\nhttps://discord.gg/Hn3XeUk")

bot.run(token)
