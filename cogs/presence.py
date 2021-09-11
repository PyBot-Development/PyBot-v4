from discord.ext import commands, tasks
import discord
from resources import support
import os
import psutil
import datetime
from run import __version__
class loop(commands.Cog, name="loop"):
    def __init__(self, client):
        self.client = client 
        self.presence.start()
        self.alts = len(support.alts)
        self.startup_timestamp = datetime.datetime.utcnow().timestamp()
    @tasks.loop(seconds=10.0)
    async def presence(self):
        current_timestamp = datetime.datetime.utcnow().timestamp()
        online_for = current_timestamp-self.startup_timestamp

        if support.config.get("debug"):
            print(f"Changed Rich Presence: CPU - {psutil.cpu_percent(2)}%, RAM - {psutil.virtual_memory().percent}%, {datetime.timedelta(seconds=int(online_for))}")
            return

        await self.client.change_presence(activity=discord.Game(name=f"""
        Cpu Usage: {psutil.cpu_percent(2)}%,
        Ram Usage: {psutil.virtual_memory().percent}%
        Servers: {len(self.client.guilds)},
        Online For: {datetime.timedelta(seconds=int(online_for))}
        Version: {__version__}"""))
    
    @presence.before_loop
    async def before_presence(self):
        await self.client.wait_until_ready()
        

def setup(bot):
    bot.add_cog(loop(bot))