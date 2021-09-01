from discord.ext import commands
import discord
from resources import checks, support
from discord.ext.commands import cooldown, BucketType
from gtts import gTTS
from datetime import datetime
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
            date = str(datetime.utcnow()).replace(":", "-")
            def tts(txt, languag):
                speech = gTTS(text = u'{}'.format(txt), lang = languag, slow = False)
                speech.save(f"{support.path}/data/temp/{date}.mp3")
                return(f"{support.path}/data/temp/{date}.mp3")

            text = text.split("-l")
            text.append("en")
            file = tts(f"{text[0]}", f"{text[1]}".replace(" ", ""))
            await ctx.send(file=discord.File(file), content="Text To Speech")
            os.remove(file)

def setup(bot):
    bot.add_cog(command(bot))