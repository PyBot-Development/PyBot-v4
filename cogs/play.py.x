from discord.ext import commands
import discord
from resources import checks
from discord.ext.commands import cooldown, BucketType
from resources import support, colours
import os
import asyncio
import youtube_dl
import datetime
import urllib
import re

class command(commands.Cog, name="play"):
    def __init__(self, client):
        self.client = client
        self.playing_in = []
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            current = await self.songs.get()
            current.start()
            await self.play_next_song.wait()

    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)

    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def play(self, ctx, *, search):
        if ctx.message.guild.id in self.playing_in:
            await ctx.send(embed=discord.Embed(description="Already Playing..", color=colours.blue))
            return
        def stop(guild_id, file):
            self.playing_in.remove(guild_id)
            os.remove(file)
        async with ctx.typing():
            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
            video = 'http://www.youtube.com/watch?v=' + search_results[0]

            out = support.path + f'/data/temp/{datetime.datetime.utcnow().timestamp()}.mp3'
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True,
                'extractaudio': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': out,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                msg = await ctx.send(embed=discord.Embed(description="Downloading Please Wait...", color=colours.blue))
                ydl.download([video])
                await msg.delete()
            self.playing_in.append(ctx.message.guild.id)
            voiceChannel = discord.utils.get(ctx.guild.voice_channels)
            await voiceChannel.connect()
            await ctx.send(embed=discord.Embed(description=f"Playing {video}", color=colours.green))
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio(out), after=lambda x: stop(ctx.message.guild.id, out))

def setup(bot):
    bot.add_cog(command(bot))

    """@commands.command()
    async def play(self, ctx, *, search):
        if ctx.message.guild.id in self.playing_in:
            await ctx.send(embed=discord.Embed(description="Already Playing..", color=colours.blue))
            return
        def stop(guild_id, file):
            self.playing_in.remove(guild_id)
            os.remove(file)
        async with ctx.typing():
            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
            video = 'http://www.youtube.com/watch?v=' + search_results[0]

            out = support.path + f'/data/temp/{datetime.datetime.utcnow().timestamp()}.mp3'
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True,
                'extractaudio': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': out,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                msg = await ctx.send(embed=discord.Embed(description="Downloading Please Wait...", color=colours.blue))
                ydl.download([video])
                await msg.delete()
            self.playing_in.append(ctx.message.guild.id)
            voiceChannel = discord.utils.get(ctx.guild.voice_channels)
            await voiceChannel.connect()
            await ctx.send(embed=discord.Embed(description=f"Playing {video}", color=colours.green))
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio(out), after=lambda x: stop(ctx.message.guild.id, out))"""