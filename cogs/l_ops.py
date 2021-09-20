from discord.ext import commands
import discord
from resources import checks, support, LOCAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="ops"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def ops(self, ctx):
        await LOCAL_DATABASE.GUILD_CHECK(ctx.message.guild)
        banlist = await LOCAL_DATABASE.GET_OPS(ctx.message.guild)
        b_list = "".join(f"<@{item}>, " for item in banlist)
        await ctx.send(embed=discord.Embed(
            title="Opped Users.",
            description=f"{b_list[:-2]}.",
            color=colours.blue
        ))

def setup(bot):
    bot.add_cog(command(bot))