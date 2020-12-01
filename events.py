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

        cb_chnl_ids = [656583866600914953, 697736009357721630]

        for chnl_id in cb_chnl_ids:
            if message.channel.id == chnl_id:
                if msg.find('cryptobin.co') == -1:
                    await message.delete()
                    await message.channel.send(f'Meldingen din ble slettet fra <#{chnl_id}> fordi den ikke inneholdt en cryptobin link. Du kan diskutere løsningene i <#652630061584875532>', delete_after=5)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        msg = after.content.lower()

        cb_chnl_ids = [656583866600914953, 697736009357721630]

        for chnl_id in cb_chnl_ids:
            if after.channel.id == chnl_id:
                if msg.find('cryptobin.co') == -1:
                    await after.delete()
                    await after.channel.send('Meldingen din ble slettet fra <#656583866600914953> fordi den ikke inneholdt en cryptobin link. Du kan diskutere løsningene i <#652630061584875532>', delete_after=5)            

def setup(bot):
    bot.add_cog(EventsCog(bot))