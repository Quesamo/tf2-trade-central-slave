"""
This cog periodically updates the name of a certain
channel to display the current key price as retrieved
from backpack.tf
"""

from discord.ext import tasks, commands
import requests
import json

class key_price_display(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        self.key_price_display_channel = self.bot.get_channel(731309709872595015)
        #linter needs to ignore this line. code works fine
        self.refresh_key_price_loop.start() #pylint: disable=no-member


    """
    Gets the current key price from the saved
    API response. Returns float
    """
    def get_key_price(self):
        with open('commands/call_APIs/api_responses/backpacktf_igetpricesv4_response.json', 'r') as api_response:
            response = json.load(api_response)
            key_price = response['response']['items']['Mann Co. Supply Crate Key']['prices']['6']['Tradable']['Craftable'][0]['value']
            return key_price
    
    #automatically updates the display
    @tasks.loop(hours=2.0)
    async def refresh_key_price_loop(self):
        key_price = self.get_key_price()
        await self.key_price_display_channel.edit(name=f"Key price: {key_price} ref")
        print('Key price display updated')

    @refresh_key_price_loop.before_loop
    async def before_refresh_key_price(self):
        await self.bot.wait_until_ready()



    #command that manually updates the display
    @commands.command()
    async def refresh_key_price(self, ctx):
        key_price = self.get_key_price()
        await self.key_price_display_channel.edit(name=f"Key price: {key_price} ref")
        print('Key price display updated')


def setup(bot):
    bot.add_cog(key_price_display(bot))
    print('Cog key_price_display loaded!')