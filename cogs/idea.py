from re import I
from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType
import asyncio

class command(commands.Cog, name="idea"):
    def __init__(self, client):
        self.client = client
    async def get_channel(self):
        try:
            self.channel.id
        except:
            guild = self.client.get_guild(885976189049651200)
            for i in guild.text_channels:
                if i.id == 885986347234508840:
                    self.channel = i
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def idea(self, ctx, *, Text):
        await self.get_channel()
        await self.channel.send(content="<@846298981797724161>" ,embed=discord.Embed(
            title=ctx.message.author.id,
            description=Text,
            color=colours.green
        ).set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url))
    

def setup(bot):
    bot.add_cog(command(bot))