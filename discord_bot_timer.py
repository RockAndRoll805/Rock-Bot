import discord
from discord.ext import commands

import threading
import asyncio
import re

async def timer_reply(channel, text):
        await channel.send('timer complete')

class AsyncTimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        if message.content.lower().startswith('remind'):
            timer_regex = re.search('(<@[!&]?[0-9]+>.*|me) in +([0-9]+|an|a) +(second|day|minute|hour|week|month|year)s? +(.*)', message.content)
            
            if(timer_regex == None or timer_regex.group(2) == None or timer_regex.group(3) == None or timer_regex.group(4) == None):
                print('regex error')
                return

            timer_length = 0
            if(timer_regex.group(2) == 'a' or timer_regex.group(2) == 'an'):
                timer_length = 1
            else:
                timer_length = int(timer_regex.group(2))

            if(timer_regex.group(3) == 'minute'):
                timer_length = timer_length * 60
            elif(timer_regex.group(3) == 'hour'):
                timer_length = timer_length * 3600
            elif(timer_regex.group(3) == 'day'):
                timer_length = timer_length * 86400
            elif(timer_regex.group(3) == 'week'):
                timer_length = timer_length * 604800
            elif(timer_regex.group(3) == 'month'):
                timer_length = timer_length * 2592000
            elif(timer_regex.group(3) == 'year'):
                if(timer_length > 5):
                    await message.channel.send('No')
                    return
                else:
                    timer_length = timer_length * 31536000

            timer_message = timer_regex.group(4)
            if(timer_message.startswith('to ')):
                timer_message = timer_message[3:]
            if('@everyone' in timer_message or '@here' in timer_message):
                await message.channel.send('Nice try')
                return

            timer_user_mention = message.author.mention
            if timer_regex.group(1) != 'me':
                timer_user_mention = timer_regex.group(1)

            await message.channel.send('Reminder set')
            
            await asyncio.sleep(timer_length)
            await message.channel.send(('{} '.format(timer_user_mention) + timer_message))