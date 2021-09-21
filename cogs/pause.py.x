from discord.ext import commands
import discord
from resources import checks, support, processing, colours
from discord.ext.commands import cooldown, BucketType
import os

class command(commands.Cog, name="tts"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="pauses music")
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send(embed=discord.Embed(description="Paused ⏸️", color=colours.blue))

def setup(bot):
    bot.add_cog(command(bot))