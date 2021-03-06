import discord
from discord.ext import commands

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np

class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def stocks(self, ctx):

        message_split = ctx.message.content.split(' ')
        if (len(message_split) <= 1):
            await ctx.send('Please follow the format: `!stocks [ticker] [time (optional)]`')
            return

        request = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + message_split[1].upper() + '&interval=5min&apikey=QCMINNI1UEEPB066')
        data = request.json()
        if ('Error Message' in data):
            await ctx.send('Invalid ticker')
            return

        time_arr = []
        value_arr = []

        for x in data['Time Series (5min)']:
            time_arr.insert(0, x[11:-3])
            value_arr.insert(0, float(data['Time Series (5min)'][x]['1. open']))
            # index -= 1

        value_max = max(value_arr)
        value_min = min(value_arr)

        fig, ax = plt.subplots() #pylint: disable=unused-variable
        plt.xticks(np.arange(len(time_arr)), time_arr)
        plt.yticks(np.arange(value_min - 1, value_max + 1, step=(value_max - value_min )/10))
        ax.set_ylim(ymin=value_min)
        ax.plot(value_arr)

        myLocator = mticker.MultipleLocator(len(time_arr)/10)
        ax.xaxis.set_major_locator(myLocator)

        plt.title(data['Meta Data']['2. Symbol'] + ' | Last refreshed: ' + data['Meta Data']['3. Last Refreshed'])
        plt.savefig('graph.png')

        await ctx.send('Daily max: ' + str(value_max) + '\nDaily min: ' + str(value_min), file=discord.File('graph.png'))