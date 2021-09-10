from discord.ext import commands
import discord
from resources import checks, support
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="embed"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def embed(self, ctx, description=None, color=None, title=None,):
        colour = int(color.replace("#", ""), 16)
        await ctx.send(embed=discord.Embed(title=title, description=description, color=colour))

def setup(bot):
    bot.add_cog(command(bot))