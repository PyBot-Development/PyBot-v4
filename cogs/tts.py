from discord.ext import commands
import discord
from resources import checks, support
from discord.ext.commands import cooldown, BucketType
from gtts import gTTS

class command(commands.Cog, name="tts"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def tts(self, ctx, *, text):
        def tts(txt, languag):
            speech = gTTS(text = u'{}'.format(txt), lang = languag, slow = False)
            speech.save(f"{support.path}/data/temp/tts.mp3")
            return(f"{support.path}/data/temp/tts.mp3")
        text = text.split("--language")
        try: text = text.split("-l")
        except: pass
        text.append("en")
        async with ctx.typing():
            await ctx.send(file=discord.File(tts(f"{text[0]}", f"{text[1]}".replace(" ", ""))), content="Text To Speech")

def setup(bot):
    bot.add_cog(command(bot))