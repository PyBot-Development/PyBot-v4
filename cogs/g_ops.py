from discord.ext import commands
import discord
from resources import checks, support, GLOBAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="ops"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def gops(self, ctx):
        banlist = await GLOBAL_DATABASE.GET_OPS()
        b_list = "".join(f"<@{item}>, " for item in banlist)
        await ctx.send(embed=discord.Embed(
            title="Global Opped Users.",
            description=f"{b_list[:-2]}.",
            color=colours.blue
        ))

def setup(bot):
    bot.add_cog(command(bot))