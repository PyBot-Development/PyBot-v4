from discord.ext import commands
import discord
from resources import checks, support, GLOBAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType
from datetime import datetime

class command(commands.Cog, name="ban"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def gtempban(self, ctx, user:discord.Member, stamp, *, reason="No Reason Specified."):
        stamp = stamp.replace("s", "").replace("m", "*60").replace("h", "*3600").replace("d", "*86400")
        stamp = int(eval(stamp))
        _stamp = int(datetime.timestamp(datetime.utcnow()) + int(stamp))
        duration = f"<t:{int(_stamp)}:f>"
        dt_object = datetime.fromtimestamp(_stamp)

        await GLOBAL_DATABASE.TEMPBAN_USER(user, reason, ctx.message.author, _stamp)
        await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Tempbanned user {user.mention} to {duration}/{dt_object} UTC.", color=colours.green))
        try:
            channel = await user.create_dm()
            await channel.send(embed=discord.Embed(description=f"""You've been banned from using bot by {ctx.message.author.mention}.
Reason: `{reason}`
To: {duration}
Or: {dt_object} UTC""",color=colours.blue))
        except:
            pass

def setup(bot):
    bot.add_cog(command(bot))