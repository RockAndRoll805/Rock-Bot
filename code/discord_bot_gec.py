import discord
from discord.ext import commands
import asyncio
from random import randint

async def update_name(member):
    sleep_time = randint(1, 7200)
    await asyncio.sleep(sleep_time)
    gec = open('gec.txt', 'r')
    gec_num = int(str(gec.read())) + 1
    gec.close()
    gec = open('gec.txt', 'w')
    gec.write(str(gec_num))
    gec.close()
    gec_name = (str(gec_num) + ' gecs')
    await member.edit(nick = gec_name)
    
    await update_name(member)

class Gec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(436783009258143744)
        for member in guild.members:
            if member.id == 141376195756425216:
                await update_name(member)
                break