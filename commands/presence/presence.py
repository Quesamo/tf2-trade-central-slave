import discord
from discord.ext import tasks, commands
from itertools import cycle


class presence(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
        self.status_list = cycle(['$help', 'scrapbanking in 2020'])

        self.changepresence.start() # pylint: disable=no-member 
        #gives an error if pylint isn't told to ignore the line, even though the code runs just fine
    
    @tasks.loop(seconds=15.0)
    async def changepresence(self):
        await self.bot.change_presence(activity=discord.Game(next(self.status_list)))    

    #assures the task isn't started before the bot is ready
    @changepresence.before_loop
    async def before_changepresence(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(presence(bot))
    print('Cog presence loaded!')