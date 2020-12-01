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

        embed = discord.Embed(description='Poengoversikt', color=0x50bdfe)
        for x in range(10):
            user = score[x]
            embed.add_field(name=f'#{x+1} ({user["display_name"]})', value=user["challenges_solved"], inline=True)
        embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    @commands.dm_only()
    async def restart(self, ctx):
        await ctx.send('Restarting...')
        os.execv(sys.executable, ['python3'] + sys.argv)

def setup(bot):
    bot.add_cog(CommandsCog(bot))