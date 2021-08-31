from discord.ext import commands
import discord
from resources import checks
from discord.ext.commands import cooldown, BucketType
from resources import support, colours, can_generator

class command(commands.Cog, name="can"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def can(self, ctx, text, bottom_text=""):
        async with ctx.typing():
            img = await can_generator.generate(text, bottom_text)
            if not img:
                await ctx.send(embed=discord.Embed(description="❔ Text and Bottom Text max lenght is 20.", color=colours.red))
                return
            else:
                file = discord.File(img)
                await ctx.send(embed=discord.Embed(description="Can.", color=colours.blue).set_image(url="attachment://can.png"), file=file)
            
def setup(bot):
    bot.add_cog(command(bot))