from discord.ext import commands
import discord
from resources import checks
from discord.ext.commands import cooldown, BucketType
from resources import support, colours

class command(commands.Cog, name="alt"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, 300, BucketType.user)
    @commands.command()
    async def alt(self, ctx):
        async with ctx.typing():
            alt = support.get_alt()
            channel = await ctx.message.author.create_dm()
            await channel.send(embed=discord.Embed(description=f"||{alt}||", color=colours.blue))
            
def setup(bot):
    bot.add_cog(command(bot))