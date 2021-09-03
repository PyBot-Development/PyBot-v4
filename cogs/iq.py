from discord.ext import commands
import discord
from resources import checks, support
from discord.ext.commands import cooldown, BucketType
import random
from datetime import datetime
class command(commands.Cog, name="hello"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def iq(self, ctx, *,user: discord.User=None):
        iq_size = random.uniform(0.00, 200.00)
        if user is None: user = ctx.message.author
        if user.id in [846298981797724161, 818236132578820126]:
            iq_size = 200.00
        colour_hex = '%02x%02x%02x' % ( int((iq_size/2)*2.55), int((iq_size/2)*2.51), int((iq_size/2)*1.91) )
        colour = int(colour_hex, 16)
        embed=discord.Embed(description=f"{user} IQ is {iq_size:.2f}.", color=colour)
        embed.set_footer(text=f"""Requested by: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(command(bot))