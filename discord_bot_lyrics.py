from discord.ext import commands
import requests

async def SendLyrics(self, channel, content):
    song = ''
    if content.lower().startswith('!lyrics'):
        song = content[8:].replace(' ', '%20')
    elif content.lower().startswith('what'):
        song = content[23:].replace(' ', '%20')

    request = requests.get('https://some-random-api.ml/lyrics?title=' + song)
    data = request.json()
    await channel.send(data['links']['genius'])

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        message_in = message.content
        if message_in.lower().startswith('what are the lyrics') or message_in.lower().startswith('!lyrics'):
            await SendLyrics(self, message.channel, message.content)