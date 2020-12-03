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

            for x in range(15):
                user = score[x]
                
                if user["eggs_solved"] == "0":
                    embed_string += f'#{x+1} {Utils().formatDisplayName(user["display_name"])} - {int(user["challenges_solved"]) * 10} poeng\n'
                else:
                    embed_string += f'#{x+1} {Utils().formatDisplayName(user["display_name"])} - {int(user["challenges_solved"]) * 10} poeng og ⭐ x {user["eggs_solved"]}\n'
                    
            highest_score = int(score[0]["challenges_solved"]) + int(score[0]["eggs_solved"])
            high_score_count = 0

            for x in range(len(score)):
                user = score[x]
                user_score = int(user["challenges_solved"]) + int(user["eggs_solved"])
                if user_score == highest_score:
                    high_score_count += 1
                else:
                    break

            embed.description = f'{embed_string }\n{high_score_count} flittige arbeidere har maks poeng'
            embed.set_footer(text=f'Etterspurt av: {ctx.message.author.name}#{ctx.message.author.discriminator}')
            await ctx.send(embed=embed)
        else: # If user(s) inputted => send score for specific user(s)
            embed = discord.Embed(title='Poengoversikt', color=0x50bdfe)

            embed_string = Utils().getScoreUsersByName(score, args)

            if embed_string:
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