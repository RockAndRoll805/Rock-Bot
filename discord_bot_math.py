from discord.ext import commands
from math import sqrt, pow, degrees, radians, pi, e, log, factorial

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        message_in = message.content
        if message_in.lower().startswith('what is'):
            try:
                reply = eval(message_in.lower().split('what is')[1],{'sqrt':sqrt, 'pow':pow, 'degrees':degrees, 'radians':radians, 'pi':pi, 'e':e, 'log':log, 'factorial':factorial})
                await message.channel.send(reply)
            except NameError:
                pass
            except SyntaxError:
                pass
            except ZeroDivisionError:
                pass