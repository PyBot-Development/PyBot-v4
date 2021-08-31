from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="nick"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def nick(self, ctx, *, nick=None):
        await ctx.message.guild.me.edit(nick=nick)
        await ctx.send(embed=discord.Embed(description="Done", color=colours.blue), delete_after=10)

def setup(bot):
    bot.add_cog(command(bot))