from discord.ext import commands

class pinghelp(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        self.main_message = "Remember to include links to all items in question when pinging for advice! Read the channel description for more info."
        self.required_phrases = ['backpack.tf/stats', 'backpack.tf/item']

        if message.author.id != 603734708450361364 and message.channel.id == 332750180283711488 and '@&440193726669651968' in message.content: #makes sure the listener isn't triggered by its own messages & only in the trading advice channel
            if all(phrase not in message.content.lower() for phrase in self.required_phrases):
                await message.channel.send(self.main_message)
                return

def setup(bot):
    bot.add_cog(pinghelp(bot))
    print('Cog pinghelp loaded!')