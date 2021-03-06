import discord
from discord.ext import commands
import requests
import urllib.request
import re

from discord_bot_send_message import SendMessage

def GetDefinition(word, entry):
    r = requests.get('https://dictionaryapi.com/api/v3/references/collegiate/json/' + word.replace(' ', '%20') + '?key=KEY GOES HERE')
    data = r.json()

    count = 0
    for x in data:
        if x['meta']['id'].startswith(word + ':'):
            count += 1

    if entry >= count:
        entry = 0

    if count == 0:
        count = 1
    title = word + ', ' + data[entry]['fl'] + ' (definition ' + str(entry + 1) + ' of ' + str(count) + ' )'

    description = ''
    for x in data[entry]['shortdef']:
        description += x + '\n'

    return discord.Embed(title = title.capitalize(), description = description)
    

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        message_in = message.content
        if message_in.startswith('!word') or message_in.startswith('!wotd'):
            wotd=''
            with urllib.request.urlopen('https://www.merriam-webster.com/word-of-the-day') as response:
                for line in response:
                    line = line.decode('utf-8')
                    if '<title>Word of the Day' in line:
                        word_split = line.split('Word of the Day')
                        wotd = word_split[1][2:word_split[1][2:].find(' ')+2]
            # await message.channel.send(embed = GetDefinition(wotd.lower(), 0))
            await SendMessage(GetDefinition(wotd.lower(), 0), message.channel)

        elif message_in.lower().startswith('define') or message_in.lower().startswith('!define'):
            word = message_in

            entry = 0
            if word[-1].isdigit():
                entry = int(word.split(' ')[-1]) - 1
                word = word[word.find(' ') + 1:[x.isdigit() for x in word].index(True) - 1]
            else:
                word = word[word.find(' ') + 1:]

            # await message.channel.send(embed = GetDefinition(word, entry))
            await SendMessage(GetDefinition(word, entry), message.channel)
    
    @commands.command()
    async def ud(self, ctx, *, word):
        entry = 0
        if word[-1].isdigit():
            entry = int(word.split(' ')[-1]) - 1
            word = word[:[x.isdigit() for x in word].index(True) - 1]
        response = urllib.request.urlopen('https://www.urbandictionary.com/define.php?term=' + word.replace(' ','%20'))
        response_read = response.read()
        page = response_read.decode("utf8")
        response.close()

        result = re.findall('name=\"[0-9]+\">(.*)</a> <a class=\"play-sound\".*<div class=\"meaning\">(.*)<div class=\"example\">(.*)?</div><div class=\"contributor\">', page)
        if 'Word of the Day</div></div>' in page:
            result.pop(1) # get rid of result for word of the day

        if entry >= len(result):
            entry = 0

        title = result[entry][0].capitalize() + ' (definition ' + str(entry + 1) + ' of ' + str(len(result)) + ')'
        description = re.sub(r'<[^>]+>', '', result[entry][1].replace('<br/>', '\n')).replace('&apos;',"'").replace('&quot;','"').replace('&lt;', '<')

        embed_out = discord.Embed(title = title, description = description)

        example = re.sub(r'<[^>]+>', '', result[entry][2].replace('<br/>', '\n')).replace('&apos;',"'").replace('&quot;','"').replace('&lt;', '<')

        if example.endswith('via giphy'):
            giphy_link = re.search(r'(https://[\w./]+.gif)\"', result[entry][2])
            embed_out.set_image(url = giphy_link.group(1))
            example = example.replace('via giphy', '')

        embed_out.add_field(name = 'Example:', value = example, inline=False)
        await ctx.send(embed = embed_out)