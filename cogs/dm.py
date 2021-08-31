from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="hello"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def dm(self, ctx, user, *,message):
        user = await commands.UserConverter().convert(ctx, user)
        channel = await user.create_dm()
        await channel.send(message)
        await ctx.send(embed=discord.Embed(description="Done", color=colours.blue), delete_after=10)

def setup(bot):
    bot.add_cog(command(bot))