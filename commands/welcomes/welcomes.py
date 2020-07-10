import discord
from discord.ext import commands
import random

class welcomes(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        welcome_messages = [
            "Welcome. Welcome to TF2 Trade Central, {}",
            "Hey look, it's {}!",
            "How- how'd you get in here, {}!?",
            "{} just joined. This guy is hilarious.",
            "Welcome to the server, {}. Remember, posting dead memes is grounds for execution",
            "Ah, if it isn't comrade {}. Glory to TF2 Trade Central",
            "{} just arrived. Got the goods?",
            "{} joined the server, you should buy his hats",
            "Beep bloop bleep, {} joined the server",
            "Wow, look at that! It's that guy! You know, {}!",
            "I'm just pinging you to piss you off {}",
            "{} showed up. About time",
            "Oh hey, {}. Beer's by the couch.",
            "{} is in a cat",
            "{} just joined. Don't ask where #buy-orders went",
            "Welcome to TF2 Trade Central, {}. We're the only server that's completely and 100% definitely not affiliated with anything interesting",
            "{} just joined. We're all fucked.",
            "Make yourself at home, {}.",
            "Welcome to the server, {}. Watch out for sharks",
            "{} Hello, and again, welcome to TF2 Trade Central. we hope your brief detention in the relaxation vault has been a pleasant one.",
            "{} joined. Be nice",
            "oh god oh fuck, {} arrived",
            "{} came into the server. What on earth have you walked in on",
            "hey its me ur brother, {}",
            "Beware of the Cereal Man, {}",
            "TF2 Trade Central has acquired {} in a trade",
            "Selling {}, 20 keys",
            "{}? That's a pretty name."
        ]

        welcome_channel = member.guild.system_channel
        welcome_message = random.choice(welcome_messages)
        await welcome_channel.send(welcome_message.format(member.mention)) #inserts the user mention into the {} of the strings


def setup(bot):
    bot.add_cog(welcomes(bot))
    print('Cog welcomes loaded!')