from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType
from resources.alt_checker import check

class command(commands.Cog, name="check"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def check(self, ctx, *, combo):
        await ctx.send(embed=discord.Embed(description=check(combo).result, color=colours.blue))

def setup(bot):
    bot.add_cog(command(bot))