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
        for item in banlist:
            await database_driver.CHECK_TEMPBAN(item)
        b_list = "".join(f"<@{item}>, " for item in banlist)
        await ctx.send(embed=discord.Embed(
            title="Banned Users.",
            description=f"{b_list[:-2]}.",
            color=colours.blue
        ))

def setup(bot):
    bot.add_cog(command(bot))