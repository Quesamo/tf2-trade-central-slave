import discord
from discord.ext import tasks, commands #these are all for discord stuff
import datetime

import requests #for communicating with APIs (primarily backpack.tf's)
import json #used for formatting json, usually returned from APIs


print(discord.__version__)
print("\n") #cause linesplits are cool
command_prefix = '$' #can be edited for quick changing of the prefix

bot = commands.Bot(command_prefix = command_prefix)
bot.remove_command('help')

#loading extensions
bot_extensions = [
    'commands.unupc.unupc', #unusual price check command
    'commands.randomoutputs', #flip and roll commands
    'commands.pin.pin', #pin command
    'commands.tf_currency', #commands for converting tf2 currencies

    'commands.automod.automod', #assigns member roles, auto-responds to certain messages to aid moderation
    'commands.welcomes.welcomes', #sends a custom welcome message on member join
    'commands.call_APIs.call_APIs', #automatically calls APIs at certain intervals

    'commands.presence.presence', #alternates the bot's presence
    'commands.key_price_display' #displays the current key price as a channel name
]

for extension in bot_extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'Bot started running at {datetime.datetime.now()}')


#HANDY FUNCTIONS 'N SHIT

def checkifmod(ctx): #checks if the sender of the message is a moderator
        for role in ctx.author.roles:
            if role.id == 334151916756008961: #role matches with 
                return True
        return False

def checkifbotowner(ctx): #checks if the sender of the message is the owner of the bot
    if ctx.author.id == 226441515914756097:
        return True



#COMMANDS


"""
stops the bot, the bat/sh file it's launched from ensures it's rebooted
"""
@bot.command()
async def crash(ctx):
    if checkifbotowner(ctx) == True:
        await ctx.send("Bot stopped, rebooting")
        raise SystemExit
    else: #if the user isn't the bot owner
        await ctx.send("Only the bot owner (Ques) can use this")


"""
If the user is the bot owner, iterates through
the loaded extensions and see if the last part
(that being the actual name of the extension file) matches
the given extension name. If so, reloads the bot extension
"""
@bot.command()
async def reload(ctx, extension):
    if checkifbotowner(ctx) == True: #checks if the user is the bot owner
        for bot_extension in bot_extensions:
            if extension == bot_extension.split('.')[-1]:
                bot.reload_extension(bot_extension)
                return
        await ctx.send(f"Can't find extension '{extension}''")
    else:
        await ctx.send("Only the bot owner (Ques) can use this")


#sends help message
@bot.command()
async def help(ctx): #sends a help message
    embed = discord.Embed(title="Command list", description=f"Prefix: {command_prefix}", color=0xc40e26)

    embed.add_field(name=f"{command_prefix}help", value="Lists all bot commands (duh)")
    embed.add_field(name=f"{command_prefix}pin", value="``[MOD COMMAND]`` Include a message ID to save it to a special channel")
    embed.add_field(name=f"{command_prefix}unupc", value="Price checks an unusual. Syntax is ``effectname.hatname``. (This command is under construction and has been known to not work with certain effects. Report any bugs to the bot owner)")
    embed.add_field(name=f"{command_prefix}refreshprices", value=f"Updates the prices used by {command_prefix}unupc. This will soon be done automatically every 2 hours")
    embed.add_field(name=f"{command_prefix}flip", value="Simulates a coinflip. Custom coin sides can be set (ex.: ``$flip black, white``)")
    embed.add_field(name=f"{command_prefix}roll", value="Simulates a die roll. Upper limit can be set (ex.: ``$roll 10``), as well as amount + upper limit (ex.: ``$roll 2d6``)")
    embed.set_footer(text="TF2 Trade Central Slave version -497, created by ya boi Quesamo (patent pending)")
    await ctx.send(embed=embed)


with open('discord_api_key.txt', 'r') as discord_api_key:
    discord_api_key = discord_api_key.read() #reads the file
    bot.run(discord_api_key)