from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="banned"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def banned(self, ctx):
        banlist = await database_driver.GET_BANNED()
        b_list = ""
        for item in banlist:
            b_list += (f"<@{item}>, ")

        await ctx.send(embed=discord.Embed(
            title="Banned Users.",
            description=f"{b_list[:-2]}.",
            color=colours.blue
        ))

def setup(bot):
    bot.add_cog(command(bot))