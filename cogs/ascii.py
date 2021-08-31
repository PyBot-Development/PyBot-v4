from discord.ext import commands
import discord
from resources import checks, support
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="ascii"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def ascii(self, ctx, *, arg):
        font = support.get_font()
        await ctx.send(f"```{font.renderText(arg)}```")

def setup(bot):
    bot.add_cog(command(bot))