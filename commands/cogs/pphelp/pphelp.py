from discord.ext import commands

class pphelp(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self, message):

        self.main_message = "Paypal/cash trades are a risk. Please take precautions before sending items to avoid being scammed. Such precautions include, but are not limited to, checking user's backpack.tf, steamrep, rep.tf, asking for screenshots of previous cash trades and asking other people who have worked with the user for legitimacy. Stay safe!"
        self.listing_channels = [332221029382488065, 375800525054148609, 332221993724411944, 672620604683321375] #the channel IDs of all the server's listing channels (#low-tier-listings, #high-tier-listings, #unusual-listings, #non-tf2-listings)
        self.trigger_words = ['paypal', 'pp', 'cash', 'money', 'btc', 'bitcoin']

        if message.author.id != 603734708450361364: #makes sure the listener isn't triggered by its own messages
            for channel_id in self.listing_channels: #cycles through each of the listing channels and sees if the message was sent in any of them
                if message.channel.id == channel_id: #if the channel IDs match
                    for trigger_word in self.trigger_words: #cycles through the list of trigger words to see if the message contains any of them
                        if trigger_word in message.content.lower(): #converts the entire message to lowercase and sees if it finds the trigger words within it
                            await message.channel.send(self.main_message) #send the automated paypal help message in the channel
                            return #exits the function to prevent the bot from sending more messages the more trigger words are used

def setup(bot):
    bot.add_cog(pphelp(bot))
    print('Cog pphelp loaded!') 