"""
This cog is responsible for automatic calling of APIs via loops.
Currently, this is only used to get iGetPricesV4 from backpack.tf
for use by $unupc and in the key price display.
"""

from discord.ext import tasks, commands
import requests
import json
import datetime


class call_APIs(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
        #linter needs to ignore this line. code works fine
        self.refreshprices_loop.start() # pylint: disable=no-member

    """
    Writes output from backpack.tf's
    iGetPricesV4 API to a file
    """
    def refreshprices_func(self):

        with open('commands/call_APIs/bptf_api_key.txt', 'r') as api_key: #opens the file containing the api key (remember the core bot file is in a higher directory)
            key = api_key.read() #reads the file and assigns to a var
            payload = {'key': key} #formats the request payload
            print('Connecting to Backpack.tf API')

        request = requests.get('https://backpack.tf/api/IGetPrices/v4?', params=payload) #requests from the API with the given params
        response = request.json() #formats the json retrieved from the API
        if response['response']['success'] == 0: #if the request is unsuccsessful
            print('Request failed')
            print(f"Message: {response['response']['message']}")
        with open('commands/call_APIs/api_responses/backpacktf_igetpricesv4_response.json', 'w+') as backpacktf_response: #writes the api response to a file
            json.dump(response, backpacktf_response)

        #the API gives the download time in epoch, useful for checking when the prices were *actually updated*
        print(f"Prices updated at {datetime.datetime.now()} (Epoch: {datetime.datetime.now().timestamp()})")



    #the loop itself; repeats the function at an interval
    @tasks.loop(hours=2.0) #updates the prices every 2 hours
    async def refreshprices_loop(self):
        self.refreshprices_func()
    
    #ensures the bot is ready before the loop starts
    @refreshprices_loop.before_loop
    async def before_refreshprices(self):
        await self.bot.wait_until_ready()


    #command that manually updates prices
    @commands.command()
    async def refreshprices(self, ctx):
        self.refreshprices_func()
        await ctx.send('Prices updated!')


def setup(bot):
    bot.add_cog(call_APIs(bot))
    print('Cog call_APIs loaded!')