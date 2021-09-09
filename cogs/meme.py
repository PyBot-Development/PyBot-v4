from discord.ext import commands
import discord
from resources import checks
from discord.ext.commands import cooldown, BucketType
from resources import support, colours
import random
import asyncpraw
import os

class command(commands.Cog, name="meme"):
    def __init__(self, client):
        self.client = client
        self.topics =  ["dankmemes",
                  "memes",
                  "me_irl",
                  "ComedyCemetery",
                  "terriblefacebookmemes",
                  "shitposting"]
        self.reddit = asyncpraw.Reddit(client_id=support.config.get("Client_Id"),
                     client_secret=support.config.get("Client_Secret"),
                     user_agent=support.config.get("User_Agent"), 
                     check_for_async=False
                     )
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def meme(self, ctx, *, subredd=None):
        msg = await ctx.send("Please wait.. It may take a while. Because reddit api shit.")
        async with ctx.typing():
            topic = random.choice(self.topics) if subredd is None else subredd
            subreddit = await self.reddit.subreddit(topic)
            await subreddit.load()
            meme = await subreddit.random()
            if subreddit.over18:
                await ctx.send(embed=discord.Embed(description=f"🔞 Subreddit is 18+", color=colours.red), delete_after=10)
                return
            await ctx.send(embed=discord.Embed(
                title=f"{meme.title}",
                url=meme.shortlink,
                description=f"""
                u/{meme.author.name}""",
                color=colours.blue
            ).set_image(url=meme.url).set_footer(text=f"Requested by: {ctx.message.author} • ⬆️ {meme.ups} | r/{topic}"))
            await msg.delete()
            
def setup(bot):
    bot.add_cog(command(bot))