from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="unban"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def unban(self, ctx, user:discord.Member):
        if await database_driver.UNBAN_USER(user):
            await ctx.send(embed=discord.Embed(description=f"✔️ Unbanned user {user.mention}.", color=colours.green))
            try:
                channel = await user.create_dm()
                await channel.send(embed=discord.Embed(description=f"""You've been unbanned by {ctx.message.author.mention}.""",color=colours.blue))
            except:
                pass
        else:
            await ctx.send(embed=discord.Embed(description=f"❔ User {user.mention} is not banned.", color=colours.red))
            return

def setup(bot):
    bot.add_cog(command(bot))