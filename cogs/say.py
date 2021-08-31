from discord.ext import commands
import discord
from resources import checks
from discord.ext.commands import cooldown, BucketType
from resources import support

class command(commands.Cog, name="say"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["tell", "sudo"])
    async def say(self, ctx, *, arg):
        await ctx.send(arg)

def setup(bot):
    bot.add_cog(command(bot))