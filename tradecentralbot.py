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
bot.load_extension('commands.cogs.unupc.unupc') #unusual price check command
bot.load_extension('commands.cogs.pphelp.pphelp') #contains a listener that gives help regarding paypal trading when certain trigger words are detected in given channels, and a command that does the same manually
bot.load_extension('commands.cogs.welcomes.welcomes') #contains a listener that sends a custom welcome message whenever a member joins the server
bot.load_extension('commands.cogs.presence.presence') #contains the code that alternates the bot's presence
bot.load_extension('commands.cogs.pinghelp.pinghelp') #sends a message if the trading advice role is pinged without links

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


@bot.command()
async def pin(ctx, messageID):

    if checkifmod(ctx) == True:
        #targetMessage = bot. #gets the target message 
        pinsChannel = bot.get_channel(603785272815124480) #gets the channel that it's gonna send the message to (#pins)
        
        try:
            targetMessage = await ctx.channel.fetch_message(messageID) #gets the message from the channel in which the command was used
        except: #if it can't fetch the message from the ID
            print(f"\nERROR: {ctx.author.name} tried to pin using an invalid ID") #console error message
            await ctx.send("Only valid message IDs can be used for pinning")
            return #leaves the function

        #continues if it gets a valid message ID
        attachment_urls = []
        for attachment in targetMessage.attachments: #cycles through each attachment in the message, and gets the link for each one
            attachment_urls.append(attachment.url) #appends the url of any potential attachments to a list

        embed=discord.Embed(title=f"{targetMessage.author.name}#{targetMessage.author.discriminator} ``at {targetMessage.created_at.date()}  {targetMessage.created_at.hour}:{targetMessage.created_at.minute} UTC in #{targetMessage.channel.name}``", description=f"\n{targetMessage.content}", inline=False, color=0xc40e26)
        embed.set_thumbnail(url=targetMessage.author.avatar_url)
        embed.set_footer(text=f"Pinned by {ctx.author.name}#{ctx.author.discriminator} at {ctx.message.created_at.date()}  {ctx.message.created_at.hour}:{ctx.message.created_at.minute}. \nGo to original message: {ctx.message.jump_url}") #bottom text

        for attachment_url in attachment_urls: #for every attachment url, sets the embed image to the attachment
            embed.set_image(url=attachment_url)
        
        await pinsChannel.send(embed=embed)

    else: #if the user isn't a moderator/higher
        await ctx.send('Sorry, this is for moderators only')



@bot.command()
async def crash(ctx): #stops the bot, the bat file it's launched from ensures it's rebooted
    if checkifbotowner(ctx) == True:
        await ctx.send("Bot stopped, rebooting")
        raise SystemExit
    else: #if the user isn't the bot owner
        await ctx.send("Only the bot owner (Ques) can use this")



@bot.command()
async def reload(ctx, extension): #reloads the given extension
    if checkifbotowner(ctx) == True: #checks if the user is the bot owner
        try: #tries the primary command folder first, then the cog folder
            bot.reload_extension(f'commands.{extension}.{extension}')
        except:
            bot.reload_extension(f'commands.cogs.{extension}.{extension}')
    else:
        await ctx.send("Only the bot owner (Ques) can use this")



@bot.command()
async def help(ctx): #sends a help message
    embed = discord.Embed(title="Command list", description=f"Prefix: {command_prefix}", color=0xc40e26)

    embed.add_field(name=f"{command_prefix}help", value="Lists all bot commands (duh)")
    embed.add_field(name=f"{command_prefix}pin", value="``[MOD COMMAND]`` Include a message ID to save it to a special channel") #PIN
    embed.add_field(name=f"{command_prefix}unupc", value="Price checks an unusual. Syntax is ``effectname.hatname``. (This command is under construction and has been known to not work with certain effects. Report any bugs to the bot owner)")
    embed.add_field(name=f"{command_prefix}refreshprices", value=f"Updates the prices used by {command_prefix}unupc. This will soon be done automatically every 2 hours")
    embed.set_footer(text="TF2 Trade Central Slave version -497, created by ya boi Quesamo (patent pending)")
    await ctx.send(embed=embed)


with open('discord_api_key.txt', 'r') as discord_api_key:
    discord_api_key = discord_api_key.read() #reads the file
    bot.run(discord_api_key)