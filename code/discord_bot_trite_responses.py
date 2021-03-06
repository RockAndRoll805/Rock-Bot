from discord.ext import commands

class TriteResponses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == 'f':
            await message.channel.send('https://cdn.discordapp.com/attachments/184426996758085632/625037035433885716/F.mp4')