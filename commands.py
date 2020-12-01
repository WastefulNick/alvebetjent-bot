import discord
from discord.ext import commands
import requests
from utils import Utils
import os
import sys

class CommandsCog(commands.Cog, name="Score Kommandoer"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def score(self, ctx, *args):
        score = Utils().getScoreBoard()
        if not score:
            await ctx.send('En feil har oppstått...')
            return

        if not args: # If no user inputted => send first 10 people in scoreboard
            embed = discord.Embed(title='Poengoversikt', color=0x50bdfe)
            embed_string = ''

            for x in range(10):
                user = score[x]
                embed_string += f'#{x+1} {Utils().formatDisplayName(user["display_name"])} - {int(user["challenges_solved"]) * 10} poeng\n'

            embed.description = embed_string
            embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}#{ctx.message.author.discriminator}')
            await ctx.send(embed=embed)
        else: # If user(s) inputted => send score for specific user(s)
            found = False
            embed = discord.Embed(title='Poengoversikt', color=0x50bdfe)
            embed_string = ''

            for x in range(len(score)):
                user = score[x]

                for arg in args:
                    if arg.lower() in user['display_name'].lower():
                        found = True
                        embed_string += f'#{x+1} {Utils().formatDisplayName(user["display_name"])} - {int(user["challenges_solved"]) * 10} poeng\n'

            if found:
                embed.description = embed_string
                embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}#{ctx.message.author.discriminator}')
                await ctx.send(embed=embed)
            else:
                await ctx.send('Ingen bruker med dette navnet!')

    @commands.command()
    @commands.is_owner()
    @commands.dm_only()
    async def restart(self, ctx):
        await ctx.send('Restarting...')
        os.execv(sys.executable, ['python3'] + sys.argv)

def setup(bot):
    bot.add_cog(CommandsCog(bot))