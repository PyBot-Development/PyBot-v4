from discord import permissions
from discord.ext import commands
import discord
from discord.ext.commands.core import dm_only
from resources import checks, support
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="hello"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @commands.guild_only()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def whois(self, ctx, *, user: discord.Member=None):
        if user is None:
            user=ctx.message.author
            
        roles = "None"
        if len(user.roles) > 1:
            roles = "".join(f"{i.mention} " for i in user.roles[1:])

        embed = discord.Embed(title=f"{user}",
        description=f"""
User: {user.mention}
Id: `{user.id}`
Created at: `{user.created_at}`
Bot: `{user.bot}`

Joined at: `{user.joined_at}`
Nick: `{user.nick}`
Boosting since: `{user.premium_since}`

Roles:
{roles}
""", color=user.color)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(command(bot))