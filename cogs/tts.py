from discord.ext import commands
import discord
from resources import checks, support, processing
from discord.ext.commands import cooldown, BucketType
import os

class command(commands.Cog, name="tts"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def tts(self, ctx, *, text):
        async with ctx.typing():
            text = text.split("-l")
            text.append("en")
            file = await processing.tts(f"{text[0]}", f"{text[1]}".replace(" ", ""))
            await ctx.send(file=discord.File(file), content="Text To Speech")
            os.remove(file)

def setup(bot):
    bot.add_cog(command(bot))