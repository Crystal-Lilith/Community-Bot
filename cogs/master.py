import asyncio
import discord
from discord.ext import commands

Master = [524288464422830095,624305005385482281]

class master(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("'master' Cog has been loaded!")

    @commands.command()
    async def say(self, ctx, *, msg):
        if ctx.author.id in Master:
            await ctx.message.delete()
            await ctx.send(msg)
        else:
            await ctx.send("You don't own meh")

    @commands.command()
    async def spam(self, ctx, *, msg):
        if ctx.author.id in Master:
            for s in range(0,100):
                if ctx.author.id in Master:
                    if ctx.message.content == 'stop':
                        break
                    else:
                        await ctx.send(msg)
                else:
                    pass
        else:
            await ctx.send("No I'm not gonna spam for you! Screw you!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error,commands.CommandNotFound):
            pass
        else:
            print(error)
            await ctx.send(error)

def setup(bot):
    bot.add_cog(master(bot))
