from discord.ext import commands, tasks
import discord
from resources import support
import datetime
from run import __version__
import requests
from resources import GLOBAL_DATABASE
class loop(commands.Cog, name="loop"):
    def __init__(self, client):
        self.client = client 
        if support.config.get("Run-Server"):
            self.server_status.start()
        self.alts = len(support.alts)
        self.startup_timestamp = datetime.datetime.utcnow().timestamp()
    @tasks.loop(minutes=1)
    async def server_status(self):
        key = support.config.get("Server-Key")
        port = support.config.get("Server-Port")
        date = datetime.datetime.utcnow()
        status = {
            "last_update": f"{date} UTC",
            "last_update_timestamp": f"{date.timestamp()}",

            "startup_date": f"{support.startup_date}",
            "startup_date_timestamp": f"{support.startup_timestamp}",

            "guilds": f"{len(self.client.guilds)}",
            "commands_count": f"{len(self.client.commands)}",

            "global_admins": f"{len(await GLOBAL_DATABASE.GET_ALL_ADMINS())}",
            "global_banned": f"{len(await GLOBAL_DATABASE.GET_ALL_BANNED())}",
            "global_badwords_count": f"{len(await GLOBAL_DATABASE.GET_BADWORDS())}",
            "global_badwords": f"{await GLOBAL_DATABASE.GET_BADWORDS()}",
            "global_disabled_commands_count": f"{len(await GLOBAL_DATABASE.GET_DISABLED_COMMANDS())}",
            "global_disabled_commands": f"{await GLOBAL_DATABASE.GET_DISABLED_COMMANDS()}",
            
            "version": f"{__version__}",
        }
        requests.post(url=f"http://localhost:{port}/set-status?key={key}", data=status, json=status)
    
    @server_status.before_loop
    async def before_server_status(self):
        await self.client.wait_until_ready()
        

def setup(bot):
    bot.add_cog(loop(bot))