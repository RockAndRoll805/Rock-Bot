import discord
from discord.ext import commands

import asyncio
import re
import datetime
import time
import string 
import random 
import os

async def resume_timer(channel, text, time, filename):
    await asyncio.sleep(time)
    await channel.send(('{} '.format(text)))
    os.remove('reminders/' + filename)

async def create_timer(ctx, text, time):
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 50))
    timer_date = datetime.datetime.now() + datetime.timedelta(seconds=time+1)
    fwrite = open('reminders/' + filename + '.txt', 'w+')
    fwrite.write(str(ctx.channel.id) + '\n' + str(timer_date) + '\n' + text)
    fwrite.close()
    await ctx.channel.send('Reminder set')
    await asyncio.sleep(time)
    await ctx.channel.send(('{} '.format(text)))
    os.remove('reminders/' + filename + '.txt')

def parse_clock(regex, reminder):
    if(regex.group(5) !=  None):              # if time of day is specified, parse it
        if (':' in regex.group(5)):           # if minutes are specified, parse it
            reminder = reminder.replace(minute=int(regex.group(5).split(':')[1]))
            reminder = reminder.replace(hour=int(regex.group(5).split(':')[0]))
        else:
            reminder = reminder.replace(hour=int(regex.group(5)))
        if(regex.group(6) != None):           # if am/pm is specified, parse it
            if(regex.group(6).startswith('pm')):
                reminder = reminder.replace(hour=reminder.hour+12)
    elif(regex.group(5) == None and regex.group(2) != None):    # edge case for when someone says 'remind me at X'
        reminder = reminder.replace(hour=int(regex.group(2)))
        if(regex.group(6).startswith('pm')):
            reminder = reminder.replace(hour=reminder.hour+12)
    return reminder

class AsyncTimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for filename in os.listdir(os.getcwd() + '/reminders'):
            with open(os.path.join(os.getcwd() + '/reminders', filename), 'r') as f:
                channel = self.bot.get_channel(int(f.readline().rstrip()))
                datetime_obj = datetime.datetime.strptime(f.readline().rstrip(), '%Y-%m-%d %H:%M:%S.%f')
                timer_length = int((datetime_obj - datetime.datetime.now()).total_seconds()) + 1
                await resume_timer(channel, f.readline().rstrip(), timer_length, filename)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return
        
        if ctx.content.lower().startswith('remind'):
            # group 1: user or role to ping
            # group 2: amount of time (optional)
            # group 3: unit of time
            # group 4: day number (optional)
            # group 5: specified time of reminder (optional)
            # group 6: am or pm (optional)
            # group 7: text
            timer_regex = re.search('(<[<>0-9@&! ]+>|me) ?(?:in|an|a|on|next|at)? ?([0-9]+)? (second|day|minute|hour|week|month|year|today|tonight|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|march|april|may|june|july|august|september|october|november|december)?s? ?([0-9]+th|2?3rd|[12]?2nd|[23]?1st)? ?(?:at)? ?([0-9:]+)? ?(pm |am )?(.*)', ctx.content.lower())

            timer_length = 0
            time_dict = {'second':1, 'minute':60, 'hour':3600, 'day':86400, 'week':604800, 'month':2592000, 'year':31536000}
            weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

            if('@everyone' in timer_regex.group(7) or '@here' in timer_regex.group(7)):
                await ctx.channel.send('Nice try')
                return

            if timer_regex.group(3) in time_dict:
                timer_length = time_dict[timer_regex.group(3)]
                if timer_regex.group(2) != None:
                    timer_length *= int(timer_regex.group(2))

            elif timer_regex.group(3) in weekdays:
                reminder_time = datetime.datetime.now() + datetime.timedelta(days=(time.strptime(timer_regex.group(3), "%A").tm_wday - datetime.datetime.today().weekday())%7)
                reminder_time = reminder_time.replace(hour=10, minute=0, second=0, microsecond=0)
                reminder_time = parse_clock(timer_regex, reminder_time)
                if (time.strptime(timer_regex.group(3), "%A").tm_wday == datetime.datetime.today().weekday()
                and datetime.datetime.now() > reminder_time):    # it's possible to say 'Tuesday at 10 am when its tuesday at 11 am, this would mean next week
                    reminder_time = reminder_time + datetime.timedelta(days=7)
                timer_length = int((reminder_time - datetime.datetime.now()).total_seconds())

            elif timer_regex.group(3) in months:
                reminder_time = datetime.datetime.now().replace(month=time.strptime(timer_regex.group(3), "%B").tm_mon, hour=10, minute=0, second=0, microsecond=0)
                if (timer_regex.group(5) != None and timer_regex.group(4) == None):
                    reminder_time = reminder_time.replace(day=int(timer_regex.group(5)))
                elif (timer_regex.group(4) != None):
                    reminder_time = reminder_time.replace(day=int(timer_regex.group(4)[:-2]))
                reminder_time = parse_clock(timer_regex, reminder_time)
                if reminder_time < datetime.datetime.now():
                    reminder_time = reminder_time.replace(year=reminder_time.year+1)
                timer_length = int((reminder_time - datetime.datetime.now()).total_seconds())

            elif timer_regex.group(3) == None or timer_regex.group(3) == 'today' or timer_regex.group(3) == 'tomorrow' or timer_regex.group(3) == 'tonight':
                reminder_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                reminder_time = parse_clock(timer_regex, reminder_time)
                if timer_regex.group(3) == 'tomorrow':
                    reminder_time = reminder_time + datetime.timedelta(days=1)
                if(timer_regex.group(3) == 'tonight' and reminder_time.hour < 12
                or timer_regex.group(3) == None and reminder_time.hour < 12 and datetime.datetime.now().hour > 12):
                    reminder_time = reminder_time.replace(hour=reminder_time.hour+12)
                if reminder_time > datetime.datetime.now():
                    timer_length = int((reminder_time - datetime.datetime.now()).total_seconds())

            if timer_length != 0:
                timer_user_mention = ctx.author.mention
                if timer_regex.group(1) != 'me':
                    timer_user_mention = timer_regex.group(1)
                await create_timer(ctx, timer_user_mention + ' ' + timer_regex.group(7), timer_length)