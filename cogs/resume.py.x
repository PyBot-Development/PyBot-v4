from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType
import os

class command(commands.Cog, name="tts"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="resumes music")
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send(embed=discord.Embed(description="Resuming ⏯️", color=colours.blue))

def setup(bot):
    bot.add_cog(command(bot))