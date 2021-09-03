from discord.ext import commands
import discord
from resources import checks
from discord.ext.commands import cooldown, BucketType
from resources import support
import urllib
import re

class command(commands.Cog, name="yt"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["youtube", "video"])
    async def yt(self, ctx, *, search):
        async with ctx.typing():
            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
            await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

def setup(bot):
    bot.add_cog(command(bot))