# This cog contains commands related to conversion of TF2 currencies,
# these being keys and refined metal.

import discord, random, json
from discord.ext import commands

class tf_currency(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot

    # Converts keys to ref
    # This might be the most cancerous thing I've ever written
    @commands.command()
    async def toref(self, ctx, keys_amount="0"): #optional argument for better error handling. for some reason, default keys_amount has to be a string. ValueError otherwise
        
        keys_amount = float(keys_amount) # Argument is given as str

        # Prevents tracebacks from no arguments/weird outputs from negative numbers
        if keys_amount < 0:
            await ctx.send("Invalid amount of keys")
            return
        
        with open('commands/call_APIs/api_responses/backpacktf_igetpricesv4_response.json') as api_response:
            response = json.load(api_response)
            current_key_price = response['response']['items']['Mann Co. Supply Crate Key']['prices']['6']['Tradable']['Craftable'][0]['value']
            
        ref_amount = keys_amount * current_key_price
        
        # This bit rounds the decimals of the initial ref amount to an amount
        # that can be represented using scrap (meaning the decimals are divisible by 11)

        ref_amount_rounded = round(ref_amount, 2) # Output will only have 2 decimals, need to round here
        ref_amount_decimals = round(ref_amount_rounded % 1, 8) # Gets only the decimals. Float-weirdness requires it to be done like this
        quotient = ref_amount_decimals // 0.11
        round_down_diff = ref_amount_decimals - (quotient * 0.11) # Distance from decimals of initial ref amount to those decimals rounded down
        round_up_diff = (quotient + 1) * 0.11 - ref_amount_decimals # Ditto, but rounded up
        
        #Rounds down/up depending on what's closest
        if round_down_diff < round_up_diff:
            ref_output_decimals = quotient * 0.11
        else:
            ref_output_decimals = (quotient + 1) * 0.11

        ref_output = f"{int(ref_amount_rounded // 1) + ref_output_decimals}"        
        await ctx.send(f"{keys_amount} keys = **{ref_output} ref**")

    
    # Converts ref to keys
    @commands.command()
    async def tokeys(self, ctx, ref_amount="0"): # Optional argument is str for same reason as in $toref

        ref_amount = float(ref_amount)

        if ref_amount <= 0:
            await ctx.send("Invalid amount of ref")
            return
        
        with open('commands/call_APIs/api_responses/backpacktf_igetpricesv4_response.json') as api_response:
            response = json.load(api_response)
            current_key_price = response['response']['items']['Mann Co. Supply Crate Key']['prices']['6']['Tradable']['Craftable'][0]['value']
        

        # Special case in which the output ref amount ends in .99, meaning it's an entire ref worth of scrap
        keys_amount_decimals = round(round(ref_amount, 2) % 1, 8)
        if keys_amount_decimals == 0.99:
            ref_amount = round(ref_amount, 0)

        await ctx.send(f"{ref_amount} ref = **{round(int(ref_amount) / current_key_price, 2)} keys**")
        # Rounding cause no one wants to see '3.29873593725927 keys' as output
        # This gives slightly different output compared to calculator.tf, but who cares lol

def setup(bot):
    bot.add_cog(tf_currency(bot))
    print('Cog tf_currency loaded!')