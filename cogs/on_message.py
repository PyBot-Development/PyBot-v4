from discord.ext import commands
from discord import Embed
from datetime import datetime
from resources import colours, database_driver, support
import asyncio

class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_sent = False
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id or await database_driver.ADMIN_CHECK(message.author):
            return True
        def _check(m):
            return (m.author == message.author 
            and (datetime.utcnow()-m.created_at).seconds < 1.2)
        if await support.antispam():
            if len(list(filter(lambda m:_check(m), self.bot.cached_messages))) >= 3 and not self.already_sent:
                await message.channel.send(embed=Embed(description=f"Hey! {message.author.mention} stop spamming you fucking cunt!", color=colours.red), delete_after=10)
                self.already_sent = True
                await asyncio.sleep(3)
                self.already_sent = False
        badwords = await database_driver.GET_BADWORDS()
        msg = message.content
        for letter in [".", ",", ";", ":", "\\", "/", "-", "_", "​", " ", " ", " ", " ", " ", " ", " ", " ", " ", "⠀", " ", f"{support.prefix}"]:
            msg = msg.replace(letter, "")
        if any(item.lower() in msg.lower() for item in badwords) and not await database_driver.ADMIN_CHECK(message.author):
            await message.add_reaction("😠")
            await message.channel.send(embed=Embed(description=f"❌ Watch your language {message.author.mention}!", color=colours.red), delete_after=10)
def setup(bot):
    bot.add_cog(command(bot))