import discord
from discord.ext import commands
import requests
from api import API
import os
import sys

class CommandsCog(commands.Cog, name="Score Kommandoer"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def score(self, ctx, *args):
        score = API().getScoreBoard()
        if not score:
            await ctx.send('En feil har oppstått...')
            return

        if not args: # If no user inputted => send first 10 people in scoreboard
            embed = discord.Embed(description='Poengoversikt', color=0x50bdfe)
            for x in range(10):
                user = score[x]
                embed.add_field(name=f'#{x+1} ({user["display_name"]})', value=int(user['challenges_solved']) * 10, inline=True)
            embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}#{ctx.message.author.discriminator}')
            await ctx.send(embed=embed)
        else: # If user(s) inputted => send score for specific user(s)
            found = False
            embed = discord.Embed(description='Poengoversikt', color=0x50bdfe)

            for x in range(len(score)):
                user = score[x]

                if user['display_name'].lower() in [x.lower() for x in args]:
                    found = True
                    embed.add_field(name=f'#{x+1} ({user["display_name"]})', value=int(user['challenges_solved']) * 10, inline=True)
            
            embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}#{ctx.message.author.discriminator}')
            await ctx.send(embed=embed)

            if not found:
                await ctx.send('Ingen bruker med dette navnet!')

    @commands.command()
    @commands.is_owner()
    @commands.dm_only()
    async def restart(self, ctx):
        await ctx.send('Restarting...')
        os.execv(sys.executable, ['python3'] + sys.argv)

def setup(bot):
    bot.add_cog(CommandsCog(bot))