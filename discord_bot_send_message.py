import discord
from discord.ext import commands

owoify = False

class OutputListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def owo(self, message):
        global owoify
        owoify = not owoify
        if owoify:
            await SendMessage('owo enabled', message.channel)
        else:
            await SendMessage('owo disabled', message.channel)



async def SendMessage(message_text, channel):
    global owoify
    
    if not owoify:
        if type(message_text) is discord.embeds.Embed:
            await channel.send(embed = message_text)
        else:
            await channel.send(message_text)
    else:
        if type(message_text) is discord.embeds.Embed:
            message_text.title = message_text.title.replace("I'm", 'I').replace("I'll", 'I').replace('l', 'w').replace('r', 'w')
            message_text.description = message_text.description.replace("I'm", 'I').replace("I'll", 'I').replace('l', 'w').replace('r', 'w')
            await channel.send(embed = message_text)
        else:
            await channel.send(message_text.replace("I'm", 'I').replace("I'll", 'I').replace('l', 'w').replace('r', 'w'))