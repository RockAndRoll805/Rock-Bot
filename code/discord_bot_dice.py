from discord.ext import commands

from random import randrange

from discord_bot_send_message import SendMessage

async def RollDice(self, ctx, dice_in):
    dice = dice_in.split('d')
    output = ''
    die_sum = 0
    for x in range(int(dice[0])): #pylint: disable=unused-variable
        randint = randrange(0, int(dice[1])) + 1
        output += str(randint) + ' '
        die_sum += randint 
    if int(dice[0]) > 1:
        # await ctx.send(output + '\nSum of all dice rolls: ' + str(die_sum))
        await SendMessage(output + '\nSum of all dice rolls: ' + str(die_sum), ctx.channel)
    else:
        # await ctx.send(output)
        await SendMessage(output, ctx.channel)

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def r(self, ctx, *, dice):
        await RollDice(self, ctx, dice)

    @commands.command(pass_context=True)
    async def roll(self, ctx, *, dice):
        await RollDice(self, ctx, dice)