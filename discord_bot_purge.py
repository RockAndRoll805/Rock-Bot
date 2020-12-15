import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, arg):
        if(int(arg) > 100):
            await ctx.send("Entered value too large")
        elif(int(arg) > 0):
            await ctx.channel.purge(limit=int(arg))