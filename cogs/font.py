from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="font"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def font(self, ctx, *, arg):
        if support.change_font(arg):
            await ctx.send(embed=discord.Embed(description=f"Changed font to `{arg}`", color=colours.blue))
        else:
            await ctx.send(embed=discord.Embed(description=f"Font `{arg}` not found.", color=colours.blue), delete_after=10)

def setup(bot):
    bot.add_cog(command(bot))