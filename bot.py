import discord
from discord.ext import commands
import sys, traceback
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

prefix = '!'

bot = commands.Bot(command_prefix=prefix, description='Bot som gir info om NPST CTF 2020')
#bot.remove_command('help')

extensions = ['commands', 'events']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print('Logget på som {0.user}'.format(bot))

bot.run(token, bot=True, reconnect=True) 