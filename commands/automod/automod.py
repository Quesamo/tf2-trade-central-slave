"""
This cog handles everything related to automation of
moderation:

-Telling people to include links when pinging the
trading advice role
-Warning against the risks of cash trades in the ad channels
-Automatically assigning the member role upon reacting
to the rules message
"""

import discord
from discord.ext import commands
from discord.utils import get

class automod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        #ID of the member role
        self.member_role_id = 708034263559438427

        self.ping_help_message = "Remember to include links to all items in question when pinging for advice! Read the channel description for more info."
        self.ping_required_phrases = ['backpack.tf/stats', 'backpack.tf/item']

        self.cash_help_message = "Paypal/cash trades are a risk. Please take precautions before sending items to avoid being scammed. Such precautions include, but are not limited to, checking user's backpack.tf, steamrep, rep.tf, asking for screenshots of previous cash trades and asking other people who have worked with the user for legitimacy. Stay safe!"
        self.listing_channels = [332221029382488065, 375800525054148609, 332221993724411944, 672620604683321375] #the channel IDs of all the server's listing channels (#low-tier-listings, #high-tier-listings, #unusual-listings, #non-tf2-listings)
        self.cash_trigger_words = ['paypal', ' pp', 'cash', 'money', 'btc', 'bitcoin']


    #gives all members in the server the member role
    #only used for setup, here cause it relates to automodding
    @commands.command()
    @commands.check(lambda ctx: ctx.author.id == 226441515914756097) #checks if the user is a dev (ques)
    async def giveall_memberrole(self, ctx):
        for member in ctx.guild.members:
            if self.member_role_id not in [y.id for y in member.roles]: #does not try to add the role if the user already has it
                await member.add_roles(get(ctx.guild.roles, id=self.member_role_id))
                print('Gave role to', member.name)
        print('Finished giving every member the role!')

    
    #assigns the member role to anyone who reacts to the rules
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx): #triggers on every single reaction
        #print(ctx.message_id)
        if ctx.message_id == 708299272193441922: #if message being reacted to is the rules message
            member = get(self.bot.get_all_members(), id=ctx.user_id) #needs to be a Member object, not a User object
            await member.add_roles(get(member.guild.roles, id=self.member_role_id))
            #print('Gave role to', member.name)



    #cash help and ping help in the same listener to avoid 2 on_message() functions, which gives an error
    @commands.Cog.listener()
    async def on_message(self, message):

        """
        Tells people to include links with their trading advice pings if they haven't already.
        """
        #the message is sent in the trading advice channel, and contains an advice ping
        if message.channel.id == 332750180283711488 and '@&440193726669651968' in message.content:
            if all(phrase not in message.content.lower() for phrase in self.ping_required_phrases):
                await message.channel.send(self.ping_help_message)


        """
        Warns against the risks of cash trading when certain trigger words are used in the ad channels.
        """
        #message is not sent by the bot, and is sent in a listing channel
        if message.author.id != 603734708450361364 and message.channel.id in self.listing_channels:
            if any(trigger_word in message.content.lower() for trigger_word in self.cash_trigger_words):
                await message.channel.send(self.cash_help_message)
    


def setup(bot):
    bot.add_cog(automod(bot))
    print('Cog automod loaded!')