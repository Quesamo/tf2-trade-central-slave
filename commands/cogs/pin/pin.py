import discord
from discord.ext import tasks, commands

class pin(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
    
    @commands.command()
    @commands.has_role(334151916756008961) #checks if the user is a mod
    async def pin(self, ctx, messageID):

        #targetMessage = bot. #gets the target message 
        pinsChannel = self.bot.get_channel(603785272815124480) #gets the channel that it's gonna send the message to (#pins)
        
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

        embed=discord.Embed(color=0xc40e26)
        embed.add_field(name=f"{targetMessage.author.name}#{targetMessage.author.discriminator} at {targetMessage.created_at.date()}  {targetMessage.created_at.hour}:{targetMessage.created_at.minute} UTC in #{targetMessage.channel.name}", value=targetMessage.content, inline=True)
        embed.set_thumbnail(url=targetMessage.author.avatar_url)
        embed.set_footer(text=f"Pinned by {ctx.author.name}#{ctx.author.discriminator} at {ctx.message.created_at.date()}  {ctx.message.created_at.hour}:{ctx.message.created_at.minute}. \nGo to original message: {ctx.message.jump_url}") #bottom text

        for attachment_url in attachment_urls: #for every attachment url, sets the embed image to the attachment
            embed.set_image(url=attachment_url)
        
        await pinsChannel.send(embed=embed)


def setup(bot):
    bot.add_cog(pin(bot))
    print('Cog pin loaded!')