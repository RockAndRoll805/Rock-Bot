import discord
from discord.ext import commands
import subprocess

direc = '/home/jacob/DiscordBot/discord.py/examples'

class BashShell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('$') and message.author.id == 184426815367020544:
            global direc
            user_input = message.content[1:].split(' ')
            if message.content.endswith('$'):   # if the message ends with $ then remove it and delete the message as the command is preformed
                user_input[len(user_input)-1] = user_input[len(user_input)-1][:-1]
                await message.delete()
            if user_input[0] == 'cd':
                if user_input[1] == '..':
                    direc = direc[:direc.rfind('/')]
                else:
                    direc = direc + user_input[1]
            else:
                await message.channel.send(subprocess.run(user_input, stdout=subprocess.PIPE, cwd=direc).stdout.decode('utf-8'))