import asyncio

import discord
import youtube_dl

from discord.ext import commands

import time

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Queue:
    def __init__(self):
        self.song_queue = []
        self.skip_count = 0
        self.currently_playing = False

    async def queue_play(self, ctx, player, bot):
        if not self.currently_playing:  # if nothing is playing, start
            self.currently_playing = True
            await ctx.send('Now playing: {}'.format(player.title))
            await bot.change_presence(activity=discord.Game(name=player.title))
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await asyncio.sleep(int(player.data['duration']) + 1)   # wait until song is over
            await bot.change_presence(status=None)
            self.currently_playing = False
            if len(self.song_queue) == 0:
                await ctx.voice_client.disconnect()
                self.skip_count = 0
                return
            await self.queue_play(ctx, self.song_queue.pop(0), bot)
        else:
            if self.skip_count > 0:
                self.skip_count -= 1
                return
            await ctx.send('Added to queue: {}'.format(player.title))
            self.song_queue.append(player)

    async def skip(self, ctx, bot):
        ctx.voice_client.stop()
        await ctx.send('Song skipped')
        await bot.change_presence(status=None)
        self.currently_playing = False
        if len(self.song_queue) == 0:
            self.skip_count = 0
            return
        self.skip_count += 1
        await self.queue_play(ctx, self.song_queue.pop(0), bot)

    async def queue(self, ctx):
        str_out = ''
        counter = 1
        for song in self.song_queue:
            str_out += str(counter) + '. ' + song.title + '\n'
            counter += 1
        if len(str_out) == 0:
            await ctx.send('Nothing in queue')
            return
        await ctx.send(str_out)
    
    async def remove(self, ctx, num):
        self.song_queue.pop(int(num) - 1)

    async def clear(self, ctx):
        self.song_queue = []
        await ctx.send('Song queue cleared')

    async def queue_debug(self, ctx):
        await ctx.send(str(self.song_queue) + '\n' + str(self.skip_count) + '\n' + str(self.currently_playing))
    
queue_obj = Queue()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def play(self, ctx, *, query): # Plays a file from the local filesystem

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        print(source.original)
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url): # Plays from a url (almost anything youtube_dl supports)
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
        global queue_obj
        await queue_obj.queue_play(ctx, player, self.bot)

    @commands.command()
    async def stream(self, ctx, *, url): # Streams from a url (same as yt, but doesn't predownload)
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int): # Changes the player's volume
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx): # Stops and disconnects the bot from voice
        await ctx.voice_client.disconnect()
        global queue_obj
        await queue_obj.clear(ctx)
        await queue_obj.skip(ctx, self.bot)

    @commands.command()
    async def skip(self, ctx):
        global queue_obj
        await queue_obj.skip(ctx, self.bot)

    @commands.command()
    async def queue(self, ctx):
        global queue_obj
        await queue_obj.queue(ctx)

    @commands.command()
    async def remove(self, ctx, *, num):
        global queue_obj
        await queue_obj.remove(ctx, num)

    @commands.command()
    async def clear(self, ctx):
        global queue_obj
        await queue_obj.clear(ctx)

    @commands.command()
    async def queue_debug(self, ctx):
        global queue_obj
        await queue_obj.queue_debug(ctx)

    @play.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")