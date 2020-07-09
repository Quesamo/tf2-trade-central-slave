#this cog is responsible for everything related to the member role:
#
#-giving every member in the server the role (primarily for initial setup of the system)
#-assigning the member role to anyone who reacts to the rules message

import discord
from discord.ext import commands
from discord.utils import get

class member_role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.member_role_id = 708034263559438427

    #gives all members in the server the member role
    #only used for setup
    @commands.command()
    @commands.check(lambda ctx: ctx.author.id == 226441515914756097) #checks if the user is a dev (ques)
    async def giveall_memberrole(self, ctx):
        for member in ctx.guild.members:
            if self.member_role_id not in [y.id for y in member.roles]: #does not try to add the role if the user already has it
                await member.add_roles(get(ctx.guild.roles, id=self.member_role_id))
                print('Gave role to', member.name)
        print('Finished giving every member the role!')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload): #triggers on every single reaction
        #print(payload.message_id)
        if payload.message_id == 708299272193441922: #if message being reacted to is the rules message
            member = get(self.bot.get_all_members(), id=payload.user_id) #needs to be a Member object, not a User object
            await member.add_roles(get(member.guild.roles, id=self.member_role_id))
            #print('Gave role to', member.name)


def setup(bot):
    bot.add_cog(member_role(bot))
    print('Cog member_role loaded!')