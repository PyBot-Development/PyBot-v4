from discord.ext import commands, tasks
import discord
from resources import support, GLOBAL_DATABASE

class loop(commands.Cog, name="loop"):
    def __init__(self, client):
        self.client = client 
        self.autotempunban.start()
    @tasks.loop(minutes=2)
    async def autotempunban(self):
        for i in await GLOBAL_DATABASE.GET_BANNED():
            user = await self.client.fetch_user(i)
            await GLOBAL_DATABASE.CHECK_TEMPBAN(user)
    
    @autotempunban.before_loop
    async def before_presence(self):
        await self.client.wait_until_ready() 

def setup(bot):
    bot.add_cog(loop(bot))