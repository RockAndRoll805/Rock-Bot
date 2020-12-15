from discord.ext import commands
import os
import time

class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def restart(self, message):
        if message.author.id != 184426815367020544:
            return
        await message.channel.send('Restarting...')
        time.sleep(1)
        os.execv('/home/jacob/DiscordBot/discord.py/examples/rockbot.py', [' '])
        exit()

    @commands.command(pass_context=True)
    async def terminate(self, message):
        if message.author.id != 184426815367020544:
            return
        exit()