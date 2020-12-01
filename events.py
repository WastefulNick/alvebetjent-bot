import discord
from discord.ext import commands

class EventsCog(commands.Cog, name="Events"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        msg = message.content.lower()

        if message.channel.name == 'cryptobins':
            if msg.find('cryptobin.co') == -1:
                await message.delete()
                await message.channel.send(f'Meldingen din ble slettet fra <#{message.channel.id}> fordi den ikke inneholdt en cryptobin link. Du kan diskutere løsningene i <#652630061584875532>.', delete_after=5)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        msg = after.content.lower()

        if after.channel.name == 'cryptobins':
            if msg.find('cryptobin.co') == -1:
                await after.delete()
                await after.channel.send(f'Meldingen din ble slettet fra <#{message.channel.id}> fordi den ikke inneholdt en cryptobin link. Du kan diskutere løsningene i <#652630061584875532>.', delete_after=5)            

def setup(bot):
    bot.add_cog(EventsCog(bot))