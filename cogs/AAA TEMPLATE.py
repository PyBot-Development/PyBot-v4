from discord.ext import commands
import discord
from resources import checks, support
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="hello"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def hello(self, ctx, *, arg=None):
        await ctx.send('Hello {0.display_name}.'.format(ctx.author))

def setup(bot):
    bot.add_cog(command(bot))