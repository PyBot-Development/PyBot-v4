from discord.ext import commands
import discord
from resources import checks, support, GLOBAL_DATABASE
from discord.ext.commands import cooldown, BucketType
import random
from datetime import datetime

class command(commands.Cog, name="pp"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["dick", "penis", "cock"])
    async def pp(self, ctx, *, user: discord.User=None):
        if user is None: user = ctx.message.author
        ids = [609551301730369547, 818236132578820126, 484170415720235009, 824324885379416106, 760602301790158868, 846298981797724161]
        if user.id in ids:
            ppsize = "∞"
            ppsize_inch = "∞"
            colour_hex = '%02x%02x%02x' % ( int(231), int(145), int(255) )
        elif await GLOBAL_DATABASE.ADMIN_CHECK(user):
            ppsize = random.uniform(0.00, 200000.00); ppsize_inch = ppsize/2.54; colour_hex = '%02x%02x%02x' % ( int((ppsize/2000)*2.31), int((ppsize/2000)*1.45), int((ppsize/2000)*2.55) )
        else:
            ppsize = random.uniform(0.00, 200.00); ppsize_inch = ppsize/2.54; colour_hex = '%02x%02x%02x' % ( int((ppsize/2)*2.31), int((ppsize/2)*1.45), int((ppsize/2)*2.55) )
        colour = int(colour_hex, 16)
        try:
            embed=discord.Embed(description=f"{user} pp size is {ppsize:.2f}cm/{ppsize_inch:.2f}inch.", color=colour)
        except:
            embed=discord.Embed(description=f"{user} pp size is {ppsize}cm/{ppsize_inch}inch.", color=colour)
        embed.set_footer(text=f"""Requested by: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(command(bot))