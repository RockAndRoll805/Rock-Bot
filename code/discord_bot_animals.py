from discord.ext import commands
import requests

class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dog(self, message):
        request = requests.get('https://random.dog/woof.json')
        data = request.json()
        await message.channel.send(data['url'])

    @commands.command()
    async def bird(self, message):
        request = requests.get('https://shibe.online/api/birds')
        data = request.json()
        await message.channel.send(data[0])

    @commands.command()
    async def cat(self, message):
        request = requests.get('https://shibe.online/api/cats')
        data = request.json()
        await message.channel.send(data[0])

    @commands.command()
    async def shibe(self, message):
        request = requests.get('https://shibe.online/api/shibes')
        data = request.json()
        await message.channel.send(data[0])

    @commands.command()
    async def fox(self, message):
        request = requests.get('https://randomfox.ca/floof/')
        data = request.json()
        await message.channel.send(data['image'])