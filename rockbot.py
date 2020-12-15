#!/usr/bin/python3.6

import discord
from discord.ext import commands

import discord_bot_voice
import discord_bot_8ball
import discord_bot_timer
import discord_bot_bash_shell
import discord_bot_purge
import discord_bot_maintenance
import discord_bot_trite_responses
import discord_bot_animals
import discord_bot_lyrics

import discord_bot_send_message


import os

# remove downloaded youtube videos on startup
for count, filename in enumerate(os.listdir('.')):
    if(filename.startswith('youtube-') or filename.startswith('generic-') or filename.startswith('soundcloud-')):
        print('Removed ' + filename)
        os.remove(filename)


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description='default command operator')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

bot.add_cog(discord_bot_voice.Music(bot))
bot.add_cog(discord_bot_8ball.EightBall(bot))
bot.add_cog(discord_bot_timer.AsyncTimer(bot))
bot.add_cog(discord_bot_bash_shell.BashShell(bot))
bot.add_cog(discord_bot_purge.Purge(bot))
bot.add_cog(discord_bot_maintenance.Maintenance(bot))
bot.add_cog(discord_bot_trite_responses.TriteResponses(bot))
bot.add_cog(discord_bot_animals.Animals(bot))
bot.add_cog(discord_bot_lyrics.Lyrics(bot))
#bot.add_cog(discord_bot_music_test.Music(bot))

bot.add_cog(discord_bot_send_message.OutputListener(bot))

bot.run('KEY GOES HERE')