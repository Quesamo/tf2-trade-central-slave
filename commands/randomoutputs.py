import discord, random
from discord.ext import commands

"""
This cog contains commands that give random outputs,
such as coin flips and dice rolls.
"""


class randomoutputs(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
    
    """
    Randomly picks one of two options, simulating a coin flip.
    Default names of the coin sides are 'heads' and 'tails'
    Optional argument allows for changing the names of the coin sides.
    Sides names are initially treated as one string because it seemed logical lol
    """

    @commands.command()
    async def flip(self, ctx, *, side_names="heads, tails"):
        side_names_split = side_names.split(", ")
        
        #prevents anything else than 2 side names from being given
        #obviously does not trigger if no optional argument is given
        if len(side_names_split) != 2:
            await ctx.send("Exactly 2 side names required")
            return
        
        await ctx.send(f"Coinflip result: **{random.choice(side_names_split)}**!")

    
    """
    Generates a random number to simulate a dice roll.
    Defaults values are 1-6.
    Giving an argument will set an upper limit for the result.
    Putting a 'd' in between two numbers (i.e. 2d6) will roll
    that amount of dice with the given upper limit
    (2d6 -> 2 6-sided dice)
    Rolling multiple dice will also give the sum of those dice.
    """
    @commands.command() 
    async def roll(self, ctx, config="6"):
        #if no amount of dice is specified, rolls one
        if 'd' not in config:
            await ctx.send(f"You rolled **{random.randint(1, int(config))}**")
            return

        #splits the config string into two vars
        config_split = config.split('d')
        dice_amount = int(config_split[0])
        dice_sides = int(config_split[1])
        
        #contains the result for each dice rolled
        roll_results = []
        for _ in range(1, dice_amount+1): #range() 2nd argument is exclusive
            roll_results.append(random.randint(1, dice_sides))
    
        result_string = "" #string to be used for sending the results
        results_total = 0 #total of all rolls
        
        #loop modifies both of these vars for efficiency
        for count, result in enumerate(roll_results, start=1):
            """
            if statement in string prevents ', ' from being added
            after the last result.
            """
            result_string += f"**{str(result)}**{', ' if count < len(roll_results) else ''}"
            results_total += int(result) 
        
        await ctx.send(f"You rolled {result_string} \n\n Total: {results_total}")




def setup(bot):
    bot.add_cog(randomoutputs(bot))
    print('Cog randomoutputs loaded!')