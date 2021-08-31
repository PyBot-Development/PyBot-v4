from discord.ext import commands
import discord
from resources import checks
from resources import art as artstuff
from discord.ext.commands import cooldown, BucketType
from resources import support

class command(commands.Cog, name="arts"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["arts"])
    async def art(self, ctx, *, arg=None):
        theart = artstuff.get_art(arg)
        await ctx.send(f"```{theart}```")

def setup(bot):
    bot.add_cog(command(bot))