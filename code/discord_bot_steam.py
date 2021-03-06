from discord.ext import commands
import urllib
from os import path
from random import randrange
import re
import time

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def steam(self, ctx, *, link):
        if link.endswith('/') != True:
            link += '/'
        if('/games/' not in link):
            link += 'games/?tab=all&sort=name'
        fwrite = open('steam_profiles/' + str(ctx.author.id) + '.txt', 'w')
        fwrite.write(link)
        await ctx.send('Steam URL added')

    @commands.command(pass_context=True)
    async def steamurl(self, ctx):
        if not path.exists('steam_profiles/' + str(ctx.author.id) + '.txt'):
            await ctx.send('No Steam URL found')
        else:
            fopen = open('steam_profiles/' + str(ctx.author.id) + '.txt', 'r')
            await ctx.send(fopen.read())

    @commands.command(pass_context=True)
    async def wsipos(self, ctx):
        if not path.exists('steam_profiles/' + str(ctx.author.id) + '.txt'):
            await ctx.send('No Steam URL found')
            return
        fopen = open('steam_profiles/' + str(ctx.author.id) + '.txt', 'r')
        response = urllib.request.urlopen(fopen.read()).read().decode("utf8")
        result = re.findall('{\"appid\":([0-9]+)', response)
        if result == []:
            await ctx.send('No games found. Try checking your set Steam URL with `!steamurl` or your privacy settings on Steam.')
            return
        timeout = time.time() + 20
        while True:
            url = 'https://store.steampowered.com/app/' + result[randrange(1,len(result))]
            response = urllib.request.urlopen(url).read().decode("utf8")
            if 'This content requires the base game' not in response or 'This is additional content for' not in response:
                await ctx.send(url)
                return
            if time.time() > timeout:
                await ctx.send('Request timed out')
                return